# market_data_monitor.py
import os
import sys
import time
import struct
import datetime
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import mmap
import ctypes
import platform
from l2data_reader import (
    MarketDataReader, MarketDataHeader, Envelope, TransactionEntrustData,
    SecuDepthMarketData, TransactionTradeData,
    MessageType, Direction, TrdType, OrdActionType, TransFlag, Envelope,
    time_to_milliseconds
)
from global_pb2 import Envelope
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union
from collections import defaultdict
from .callbacks import BaseCallback, Slice, Snapshot

class MarketDataFileHandler(FileSystemEventHandler):
    def __init__(self, logger, reader: MarketDataReader):
        super().__init__()
        self.logger = logger
        self.reader = reader

    def on_modified(self, event):
        """文件被修改时的处理函数"""
        if not event.is_directory and event.src_path == self.reader.index_file:
            try:
                # 更新文件大小
                self.reader.index_reader.get_size()
                self.logger.info(f"检测到索引文件修改: {event.src_path}")
            except Exception as e:
                self.logger.error(f"处理文件修改事件失败: {e}")

@dataclass
class MarketDataMonitor:
    def __init__(self, logger, data_dir: str, counter_name: str, callback: BaseCallback, slice_interval_ms: int = 5000):
        self.logger = logger
        self.data_dir = data_dir
        self.counter_name = counter_name
        self.callback = callback
        self.slice_interval_ms = slice_interval_ms
        self.reader = None
        self.observer = None
        self.running = False
        self.is_warmup = False
        
        # Slice management
        self.current_slice = defaultdict(lambda: Snapshot(Symbol="", Tick=None, Orders=[], Transactions=[]))
        self.slice_start_time = None  # Will be set when first message arrives
        self.last_msg_time = None
        
        # 添加全局缓存字典，用于存储每个symbol的最新行情数据
        self.global_ticks: Dict[str, SecuDepthMarketData] = {}
        
    def get_message_time(self, header: MarketDataHeader, market_data: Envelope) -> Optional[Tuple[int, int]]:
        """Extract date and time from market data message"""
        try:
            if header.msg_type == MessageType.SECU_DEPTH_MARKET_DATA:  # Tick data
                return (market_data.secu_depth_market_data.trade_date,
                       market_data.secu_depth_market_data.update_time)
            elif header.msg_type == MessageType.TRANSACTION_ENTRUST:  # Order data
                return (market_data.transaction_entrust_data.trade_date,
                       market_data.transaction_entrust_data.transact_time)
            elif header.msg_type == MessageType.TRANSACTION_TRADE:  # Trade data
                return (market_data.transaction_trade_data.trade_date,
                       market_data.transaction_trade_data.transact_time)
            elif header.msg_type == MessageType.SUBSCRIBE_OK:
                return None
            return None
        except Exception as e:
            self.logger.error(f"Failed to extract message time: {e}")
            return None

    def should_create_new_slice(self, msg_date: int, msg_time: int) -> bool:
        """
        判断是否应该创建新的时间片
        
        Args:
            msg_date: YYYYMMDD格式的日期
            msg_time: HHMMSSfff格式的时间
        
        Returns:
            bool: 是否应该创建新的时间片
        """
        if self.slice_start_time is None:
            return True
            
        start_date, start_time = self.slice_start_time
        
        # todo：当已经是实时行情时，根据本地时钟进行推送，不再取行情中时间。因为测试环境总是非当日行情
        if not self.is_warmup:
            current_time = int(datetime.datetime.now().strftime('%H%M%S%f')[:9])
        
            # 同一天内的时间差计算
            start_ms = time_to_milliseconds(start_time)
            msg_ms = time_to_milliseconds(current_time)
            time_diff = msg_ms - start_ms
            
            # 处理午夜零点跨天的特殊情况
            if time_diff < 0:
                time_diff += 24 * 3600 * 1000  # 加上一天的毫秒数
                
            return time_diff > self.slice_interval_ms
            

        # 如果日期不同
        if msg_date != start_date:
            # 检查是否是连续的交易日
            start_date_obj = datetime.datetime.strptime(str(start_date), '%Y%m%d')
            msg_date_obj = datetime.datetime.strptime(str(msg_date), '%Y%m%d')
            if (msg_date_obj - start_date_obj).days == 1:
                # 如果是下一个交易日
                start_ms = time_to_milliseconds(start_time)
                msg_ms = time_to_milliseconds(msg_time)
                # 计算跨日时间差
                time_diff = (24 * 3600 * 1000 - start_ms) + msg_ms
                return time_diff > self.slice_interval_ms
            else:
                # 如果不是连续的交易日，直接创建新片
                return True
        
        # 同一天内的时间差计算
        start_ms = time_to_milliseconds(start_time)
        msg_ms = time_to_milliseconds(msg_time)
        time_diff = msg_ms - start_ms
        
        # 处理午夜零点跨天的特殊情况
        if time_diff < 0:
            time_diff += 24 * 3600 * 1000  # 加上一天的毫秒数
            
        return time_diff > self.slice_interval_ms

    def process_message(self, header: MarketDataHeader, market_data: Envelope):
        """Process a single market data message"""
        if header.msg_type == MessageType.SUBSCRIBE_OK:
            # 不论是否warm up, 始终认为后台行情服务是一直在运行的，也要给策略回复on_symbol
            if not self.callback.is_subscribed(market_data.rtn_subscription_success.symbol):
                return
            self.callback.on_symbol(market_data.rtn_subscription_success.symbol)
            return
        
        msg_time = self.get_message_time(header, market_data)
        if not msg_time:
            return
            
        msg_date, msg_timestamp = msg_time
        if msg_date == 0:
            msg_time = self.get_message_time(header, market_data)
            if not msg_time:
                return
            msg_date, msg_timestamp = msg_time
            if msg_date == 0:
                return
        
        # Initialize or check slice timing
        if self.should_create_new_slice(msg_date, msg_timestamp):
            if self.current_slice:
                self.push_slice()
            if self.is_warmup:
                self.slice_start_time = (msg_date, msg_timestamp)
            else:
                pass # push_slice中已经设置了slice_start_time
            
        # Add message to current slice
        if header.msg_type == MessageType.SECU_DEPTH_MARKET_DATA:
            market_data.secu_depth_market_data.is_warmup = self.is_warmup
            self.add_tick(market_data.secu_depth_market_data)
        elif header.msg_type == MessageType.TRANSACTION_ENTRUST:
            market_data.transaction_entrust_data.is_warmup = self.is_warmup
            if market_data.transaction_entrust_data.biz_index == 0:
                market_data.transaction_entrust_data.biz_index = market_data.transaction_entrust_data.seq_no
            self.add_order(market_data.transaction_entrust_data)
        elif header.msg_type == MessageType.TRANSACTION_TRADE:
            market_data.transaction_trade_data.is_warmup = self.is_warmup
            if market_data.transaction_trade_data.biz_index == 0:
                market_data.transaction_trade_data.biz_index = market_data.transaction_trade_data.seq_no
            self.add_trade(market_data.transaction_trade_data)
            
        self.last_msg_time = (msg_date, msg_timestamp)

    def push_slice(self):
        """Push current slice to callback and wait for processing"""
        if not self.current_slice:
            return
            
        slice = Slice(Ticks=dict(self.current_slice))
        self.on_data(slice)  # Wait for callback to complete
        
        # Clear current slice
        self.current_slice.clear()
        current_time = int(datetime.datetime.now().strftime('%H%M%S%f')[:9])
        current_date = int(datetime.datetime.now().strftime('%Y%m%d'))
        self.slice_start_time = (current_date, current_time)

    def check_timeout(self):
        """Check if current slice should be pushed due to timeout"""
        if not self.current_slice or not self.last_msg_time or not self.slice_start_time:
            return
            
        last_date, last_time = self.last_msg_time
        current_time = int(datetime.datetime.now().strftime('%H%M%S%f')[:9])
        current_date = int(datetime.datetime.now().strftime('%Y%m%d'))
        
        #jsy if current_date != last_date or self.should_create_new_slice(current_date, current_time):
        #jsy todo 暂时不支持跨日场景的处理
        if self.should_create_new_slice(current_date, current_time):
            self.push_slice()

    def add_order(self, event: TransactionEntrustData):
        """Add order to current slice"""
        if not self.callback.is_subscribed(event.symbol):
            return
        
        self.current_slice[event.symbol].Symbol = event.symbol
        self.current_slice[event.symbol].Orders.append(event)
        
        # 如果该symbol在当前slice中还没有Tick数据，使用全局缓存的数据
        if self.current_slice[event.symbol].Tick is None and event.symbol in self.global_ticks:
            self.current_slice[event.symbol].Tick = self.global_ticks[event.symbol]

    def add_trade(self, event: TransactionTradeData):
        """Add trade to current slice"""
        if not self.callback.is_subscribed(event.symbol):
            return
        
        self.current_slice[event.symbol].Symbol = event.symbol
        self.current_slice[event.symbol].Transactions.append(event)
        
        # 如果该symbol在当前slice中还没有Tick数据，使用全局缓存的数据
        if self.current_slice[event.symbol].Tick is None and event.symbol in self.global_ticks:
            self.current_slice[event.symbol].Tick = self.global_ticks[event.symbol]

    def add_tick(self, event: SecuDepthMarketData):
        """Add market data tick to current slice"""
        if not self.callback.is_subscribed(event.symbol):
            return
        
        self.current_slice[event.symbol].Symbol = event.symbol
        self.current_slice[event.symbol].Tick = event
            
        # 更新全局缓存
        self.global_ticks[event.symbol] = event

    def on_data(self, slice: Slice):
        """处理时间片数据并打印详细日志"""
        self.logger.debug(f"\n{'='*100}\nTime Slice Data\n{'='*100}")
        self.callback.on_data(slice)

    def start(self):
        """Start monitoring market data"""
        self.running = True
        
        # Initialize files and reader
        index_file = os.path.join(self.data_dir, 
                                 f"market_data_md_{self.counter_name}_{self.get_current_date()}.idx")
        data_file = os.path.join(self.data_dir, 
                                f"market_data_md_{self.counter_name}_{self.get_current_date()}.bin")
        hdr_file = os.path.join(self.data_dir, 
                                f"market_data_md_{self.counter_name}_{self.get_current_date()}.hdr")

        if not os.path.exists(index_file) or not os.path.exists(data_file):
            self.logger.error(f"Market data files not found: {index_file}, {data_file}")
            return

        self.reader = MarketDataReader(self.logger, index_file, data_file, hdr_file)
        processed_msg_count = 12345678901234567890
        processed_msg_count = 0
        current_hist_count = self.reader.get_count()
        self.is_warmup = True if processed_msg_count<current_hist_count else False
        
        # Set up file monitoring
        self.observer = Observer()
        handler = MarketDataFileHandler(self.logger, self.reader)
        self.observer.schedule(handler, self.data_dir, recursive=False)
        self.observer.start()
        
        self.logger.info("Market data monitor started...")
        
        try:
            while self.running:
                try:
                    result = self.reader.read_next()
                    if result:
                        header, market_data = result
                        processed_msg_count += 1
                        self.is_warmup = True if processed_msg_count<=current_hist_count else False
                        self.process_message(header, market_data)
                    else:
                        # No new data, check timeout and wait
                        self.check_timeout()
                        time.sleep(0.1)
                except Exception as e:
                    self.logger.error(f"Error processing market data: {e}")
                    time.sleep(0.1)
        finally:
            self.stop()

    def get_current_date(self) -> str:
        return datetime.datetime.now().strftime('%Y%m%d')

    def stop(self):
        """停止监控"""
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
        if self.reader:
            self.reader.close()
        self.logger.info("Market data monitor stopped.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Market Data Monitor')
    parser.add_argument('--data-dir', required=True, help='Directory containing market data files, not including month dir.')
    parser.add_argument('--counter-name', required=True, help='Counter name')
    args = parser.parse_args()

    monitor = MarketDataMonitor(args.data_dir, args.counter_name)
    try:
        monitor.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        monitor.stop()
        
if __name__ == "__main__":
    main()