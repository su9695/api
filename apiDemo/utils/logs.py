import os,sys
import logging
import oConfig
from oConfig import HandleConfig
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dirs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
class Logger(object):
    def __init__(self,logName):
        '''
        param logName: log的自定义名称
        '''
        self._logger=logging.getLogger(logName)
        self._logger.setLevel(level=logging.DEBUG)
        # all_log存放路径
        self.all_log_path = dirs.ALL_LOG_DIR
        #error_log存放路径
        self.error_log_path =dirs.ERROR_LOG_DIR
        # 不存在则创建文件夹
        if os.path.exists(self.all_log_path) and os.path.isdir(self.all_log_path):
            pass
        else:
            os.mkdir(self.all_log_path)
        if os.path.exists(self.error_log_path) and os.path.isdir(self.error_log_path):
            pass
        else:
            os.mkdir(self.error_log_path)

        #存放日志的txt文件 格式为 路径+时间戳.txt
        self.all_log_txt = os.path.join(self.all_log_path,HandleConfig().rdConfig('stamp','value')+'.txt')
        self.error_log_txt = os.path.join(self.error_log_path,HandleConfig().rdConfig('stamp','value')+'.txt')   
        if not self._logger.handlers:
            #创建handler 存储所有日志
            fh=logging.FileHandler(self.all_log_txt,encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            # 创建一个handler 写入错误日志
            eh = logging.FileHandler(self.error_log_txt, encoding='utf-8')
            eh.setLevel(logging.ERROR)
            # 创建一个handler 控制台输出
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)

            # 创建输出日志的格式
            # 时间-日志器名称-日志级别-日志信息
            all_log_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
            # 时间-日志器名称-日志级别-文件名-函数名-行号-日志信息
            error_log_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(module)s-%(funcName)s-%(lineno)s-%(message)s')

            # 输出形式添加
            fh.setFormatter(all_log_formatter)
            eh.setFormatter(error_log_formatter)
            sh.setFormatter(all_log_formatter)

            #给logger添加handler
            self._logger.addHandler(fh)
            self._logger.addHandler(eh)
            self._logger.addHandler(sh)
    def getlog(self):
        return self._logger

