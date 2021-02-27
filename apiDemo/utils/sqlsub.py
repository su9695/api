import re,os,sys,logs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
'''
背景：接口传参时，参数值可能依赖于之前的数据，此类数据可以通过数据库查询，替换到接口参数中的变量
regex='\${.+?}'  替换 接口str中此类型的数据
re.sub(regex,repl,text)  返回 sql查询结果(dict) 匹配KEY 的value值
例子： 
sql 查询结果为 {'name':'su'}, 
接口body为{'name:${name}','password:abc123'},替换后为{'name:su','password:abc123'}

'''
logger=logs.Logger('paramSub').getlog()
def oRpl(text, adict, regex='\${.*?}', start_index=2, end_index=-1):
    '''
    param: text 准备替换变量的接口body
    param: adict sql查询结果，形式为{}，用于替换变量
    param: regex 替换的正则格式
    param: start_index  开始索引
    param: end_index  结束索引
    '''
    try:
        if not isinstance(text, str):
            raise TypeError('text must be str!')
        if not isinstance(adict, dict):
            raise TypeError('adict must be dict!')
        def rpl(match_obj):
            logger.info('替换变量参数成功')
            return adict.get(match_obj.group()[start_index:end_index])
        return re.sub(regex, rpl, text)
    except Exception as e:
        logger.error('替换变量参数时失败')
        logger.error(e)

