from colorama import Fore, Back, Style
from colorama import init as colorama_setup
from threading import RLock, Thread

import threading
import datetime
import os

from utilities.definitions import *

colorama_setup()

prefix_color = {'n': Fore.BLUE, 's': Fore.GREEN, 'w': Fore.YELLOW, 'e': Fore.RED, 'd': Fore.BLUE}
content_color = {'n': Fore.WHITE, 's': Fore.WHITE, 'w': Fore.WHITE, 'e': Fore.WHITE, 'd': Fore.LIGHTBLACK_EX}

prefix_map = {'n': '##', 's': '>>', 'w': '**', 'e': '!!', 'd': '..'}

class logger_instance:
    def __init__(self):
        self.kill = False
        self.verbose = True

        self.file_name = f'log_{datetime.datetime.timestamp(datetime.datetime.now())}.txt'
        self.file_path = os.path.join(os.getcwd(), 'logs')
        self.mutex = RLock()

        self.queue = list()

    def __create_file(self):
        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)

        try:
            open(os.path.join(self.file_path, self.file_name), 'r').close()
        except:
            open(os.path.join(self.file_path, self.file_name), 'w').close()

    def append_timestamp(self, content):
        return f'[{datetime.datetime.now()}] {content}'

    def push_to_file(self, content):
        self.__create_file()

        with open(os.path.join(self.file_path, self.file_name), 'a') as handle:
            handle.write(f'{content.replace("[37m", "").replace("[96m", "")}\n')
            handle.close()

    def update_verbose(self, verbose):
        self.verbose = verbose; return self
    
    # n = normal
    # s = success
    # w = warning
    # e = error
    # d = debug
    def apply_color(self, content, type):
        return f'{prefix_color[type]}[{prefix_map[type]}] {content_color[type]}{content}{Style.RESET_ALL}'
    
    def output(self, content, type):
        print(self.apply_color(content, type))

    def push_to_queue(self, content, type):
        with self.mutex:
            self.queue.append([content, type])

    def log(self, content, type):
        self.push_to_file(self.append_timestamp(content))

        if type == 'd' and not self.verbose: return

        self.output(content, type)

    def flush_queue(self):
        print('initializing logger')

        while not self.kill:
            if len(self.queue) <= 0:
                continue

            with self.mutex:
                for entry in self.queue:           
                    self.log(entry[0], entry[1])

                self.queue.clear()

logger = logger_instance()
logger_thread = threading.Thread(name='logger', target=logger.flush_queue)

def log(content, type='n'):
    logger.push_to_queue(content, type)

def success(content):
    log(content, 's')
def warn(content):
    log(content, 'w')
def error(content):
    log(content, 'e')
def debug(content):
    log(content, 'd')