import os,sys,oConfig,time
from  oConfig import HandleConfig
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def timeStamp():
    '''
    获取一个时间戳放到ini文件中，后续本次运行都使用该时间戳
    每次运行前如果想要获取新增的日志文件，则需要运行本function更新ini文件中的stamp项
    '''
    timestamp = time.strftime('%Y%m%d_%H%M%S',time.localtime())
    HandleConfig().setConfig('stamp', 'value', timestamp)
    return timestamp
def uuid():
    '''
	基于MAC地址+时间戳+随机数来生成GUID
    '''
    import uuid
    return {'guid': str(uuid.uuid1())}


