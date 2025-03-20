# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 09:07:19 2022
Updated on Fri Okt 04 12:21:20 2024

@author: Mohamed
"""

import os
import sys
import logging
import inspect
import datetime
import threading
import time

class Rocklogger():
    def __init__(self, level='info', use_date_in_filename=True):
        self.use_date_in_filename = use_date_in_filename
        self.current_date = datetime.datetime.now().strftime("%Y%m%d")
        self.logger = self.__setup_logger(self.__get_level(level))
        self.__setup_exception_logging()
        self.__start_date_check_thread()
    
    def __setup_logger(self, log_lvl):
        caller_dirname, caller_filename = self.__get_caller()
        log_dir = os.path.join(caller_dirname, 'logs')
        log_file = self.__get_log_file_path(log_dir, caller_filename, '')
        error_log_file = self.__get_log_file_path(log_dir, caller_filename, '_error')
        os.makedirs(log_dir, exist_ok=True)
        
        # General log file handler
        logging.basicConfig(filename=log_file, filemode='a', 
                            format='%(asctime)s - %(filename)s - %(levelname)-8s:  %(message)s', 
                            datefmt='%Y-%m-%d %H:%M:%S', 
                            level=log_lvl, 
                            force=True)
        
        # Error log file handler
        error_handler = logging.FileHandler(error_log_file, mode='a')
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)-8s:  %(message)s', 
                                            datefmt='%Y-%m-%d %H:%M:%S')
        error_handler.setFormatter(error_formatter)
        logging.getLogger().addHandler(error_handler)
        
        # Console handler
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(log_lvl)
        console_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)-8s:  %(message)s', 
                                              datefmt='%Y-%m-%d %H:%M:%S')
        console.setFormatter(console_formatter)
        logging.getLogger().addHandler(console)
        
        logger = logging.getLogger(__name__)
        return logger
    
    def __get_log_file_path(self, log_dir, filename, suffix):
        if self.use_date_in_filename:
            return os.path.join(log_dir, f"{filename}{suffix}_{self.current_date}.log")
        else:
            return os.path.join(log_dir, f"{filename}{suffix}.log")
    
    def __get_level(self, log_level_str):
        levels = {
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'warning': logging.WARNING,
            'error': logging.ERROR
        }
        return levels.get(log_level_str.lower(), logging.INFO)
    
    def __get_caller(self):
        for frame_info in inspect.stack():
            module = inspect.getmodule(frame_info.frame)
            if module and module.__name__ != __name__:
                if module.__file__:
                    dir_name, file_name = os.path.split(module.__file__)
                    file_name = file_name.split('.')[0]
                    return dir_name, file_name
                else:
                    return os.getcwd(), 'interactive_shell'
        return os.getcwd(), 'unknown'
    
    def __setup_exception_logging(self):
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            self.logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        
        sys.excepthook = handle_exception
    
    def __start_date_check_thread(self):
        def check_date_change():
            while True:
                current_date = datetime.datetime.now().strftime("%Y%m%d")
                if current_date != self.current_date:
                    self.current_date = current_date
                    self.__update_log_file_paths()
                time.sleep(60)  # Check every 60 seconds
                
        date_check_thread = threading.Thread(target=check_date_change, daemon=True)
        date_check_thread.start()
    
    def __update_log_file_paths(self):
        caller_dirname, caller_filename = self.__get_caller()
        log_dir = os.path.join(caller_dirname, 'logs')
        log_file = self.__get_log_file_path(log_dir, caller_filename, '')
        error_log_file = self.__get_log_file_path(log_dir, caller_filename, '_error')
        
        # Update handlers
        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                self.logger.removeHandler(handler)
        
        self.__setup_logger(self.logger.level)
    
    def get_logger(self):
        return self.logger
    
    def close(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            self.logger.removeHandler(handler)
            handler.close()
            
    def __del__(self):
        self.close()
        

if __name__ == "__main__":
    # Initialize with date in filename
    # logger = Rocklogger(level='debug', use_date_in_filename=True).get_logger()
    # logger.debug('This is a debug message.')

    # Initialize without date in filename
    logger = Rocklogger(level='debug', use_date_in_filename=False).get_logger()
    logger.debug('This is a debug message.')

    # Example code to trigger an uncaught exception
    print("This will be logged.")
    raise Exception("This is an uncaught exception!")