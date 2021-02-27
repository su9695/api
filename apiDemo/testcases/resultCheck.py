import os,sys,allure
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import oConfig,logs

logger = logs.Logger('check_result').getlog()


def check_result(rStatus, rText,getParam):
    '''
    :param rStatus: 接口请求返回的结果status
    :param rStatus: 接口请求返回的结果text
    :param getParam: 预期结果获取函数
    '''
    try:
        if rStatus == None and rText==None:
            logger.info('='*20+'返回的statuscode和response.text都是None'+'='*20)
            return False
        if not isinstance(rStatus,int):
            logger.error('='*20+f'返回的statuscode类型错误,为{str(type(rStatus))})'+'='*20)
        if not isinstance(rText,str):
            logger.error('='*20+f'返回的response.text类型错误,为{str(type(rText))})'+'='*20)
        logger.info('='*20+f'断言中的rStatus实际值为{rStatus},type为{str(type(rStatus))}'+'='*20)
        logger.info('='*20+f'断言中的rText实际值为{rText},type为{str(type(rText))}'+'='*20)
        logger.info(
            '='*20+f"断言中的rStatus预期值为{getParam['Expected_Status']},type为{str(type(getParam['Expected_Status']))}"+'='*20)
        logger.info(
            '='*20+f"断言中的rText预期值为{getParam['Expected_Text']},type为{str(type(getParam['Expected_Text']))}"+'='*20)
        if str(rStatus) == getParam['Expected_Status'] and getParam['Expected_Text'] in rText:
            return True 
        else:
            return False
    except Exception as e:
        logger.error('='*20+'接口返回结果断言异常'+'='*20)
        logger.error(e)


