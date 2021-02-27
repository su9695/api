import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dirs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from configobj import ConfigObj


class HandleConfig(object):
    def __init__(self):
        '''
        导入conf.ini文件
        '''
        self.inipath=dirs.CONF_DIR
        self.cf=ConfigObj(self.inipath,encoding='utf-8')
    def rdConfig(self,section,option):
        '''
        param setcion: section名称
        param option: 子项名称
        '''
        try:
            return self.cf[section][option]
        except Exception as e:
            print(e)
    def setConfig(self,section,option,value):
        '''
        param section: 欲添加section名称
        param option: 欲添加option名称
        param value: 欲添加value值
        '''
        try:
            if not isinstance(section,str):
                raise TypeError('bad section type')
            if not isinstance(option,str):
                raise TypeError('bad option type')
            if not isinstance(value,str):
                raise TypeError('bad value type')
            #如果section-option 存在，则直接修改值
            if section in self.cf:
                if self.cf[section][option]:
                    self.cf[section][option] = value
            else:
            #不存在则新增并赋值
                self.cf[section] = {}
                self.cf[section][option] = value
            self.cf.write()
        except Exception as e:
            print(e)



