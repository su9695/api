import sys,os
import allure
import apiMethod
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import oConfig,logs,dbsql,oYaml,sqlsub,randomly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


logger = logs.Logger('send_request').getlog()


def send_request(testYaml,testExcel,session): 
    '''
    :param  testYaml: 对于用例的yaml测试文件名称
    :param  testExcel: 对于用例的Excel测试数据(根据conftest的getParam获取)
    :param session: s=requests.session() 可跨请求保持参数
    '''
    # 获取各项测试信息
    try:
        # 获取conf.ini 下公用的信息
        obphost = oConfig.HandleConfig().rdConfig('hosts', 'obphost')  # obphost
        logger.info('='*20+f'obphost值为:{obphost}'+'='*20)
        omphost = oConfig.HandleConfig().rdConfig('hosts', 'omphost')  # obphost
        logger.info('='*20+f'omphost值为:{omphost}'+'='*20)
        osphost = oConfig.HandleConfig().rdConfig('hosts', 'osphost')  # obphost
        logger.info('='*20+f'osphost值为:{osphost}'+'='*20)
        # basic.yaml 中的默认 headers
        basicheaders = oYaml.HandlerYaml().rdYml('basic.yaml', 'headers')  # basic headers
        logger.info('='*20+f'headers默认值为:{str(basicheaders)}'+'='*20)
        # testYaml：获取是否需要使用不同于basic的headers
        testheaders = oYaml.HandlerYaml().rdYml(testYaml, 'headers')
        logger.info('='*20+f'测试用例自己需要的headers值为:{str(testheaders)}'+'='*20)
        # testYaml: 本次请求是否为上传附件
        mime_type =  oYaml.HandlerYaml().rdYml(testYaml,'attchUpload','mime_type')# 上传附件的请求类型
        logger.info('='*20+f'上传附件的请求类型为:{str(mime_type)}'+'='*20)
        files = oYaml.HandlerYaml().rdYml(testYaml,'attchUpload','files') # 上传的文件内容
        logger.info('='*20+f'上传附件的文件内容为:{str(files)}'+'='*20)
        # 获取Excel的数据
        system = testExcel['System'] # 所属系统
        logger.info('='*20+f'所属系统为:{system}'+'='*20)
        method = testExcel['Method'] # 请求method
        logger.info('='*20+f'请求方法为:{method}'+'='*20)
        subUrl = testExcel['Api']  # 请求名称
        logger.info('='*20+f'请求subUrl为:{subUrl}'+'='*20)
        data = testExcel['Body'] # 请求数据
        logger.info('='*20+f'请求data为:{str(data)}'+'='*20)
        nCookies = testExcel['nCookies'] # 是否需要cookies
        logger.info('='*20+f'请求是否需要cookies:{nCookies}'+'='*20)
        sCookies = testExcel['sCookies'] # 是否需要保存cookies  
        logger.info('='*20+f'请求是否需要保存cookies:{sCookies}'+'='*20)
        selectSql = testExcel['selectSql'] # 查询语句
        logger.info('='*20+f'请求需要执行的查询语句为:{selectSql}'+'='*20)
        updateSql = testExcel['updateSql'] # 更新语句
        logger.info('='*20+f'请求需要执行的更新语句为:{updateSql}'+'='*20)
        deleteSql = testExcel['deleteSql']  # 删除语句
        logger.info('='*20+f'请求需要执行的删除语句为:{deleteSql}'+'='*20)
        # 组合dict 传给 apiMethod
        caseYmldata = {'nCookies':nCookies,'sCookies': sCookies, 'mime_type': mime_type, 'files': files}
        logger.info('='*20+f'传递给caseYmldata的值为:{str(caseYmldata)}'+'='*20)
        logger.info('='*20+'执行获取基本信息操作完成'+'='*20)
    except Exception as e:
        logger.error('='*20+'执行获取基本信息操作异常'+'='*20)
        logger.error(e)
    # 处理data:替换sql查询结果
    try:
        if deleteSql:
            logger.info('='*20+f'执行用例前置delete:{deleteSql}语句'+'='*20)
            for desql in deleteSql.split(';'):
                dbsql.DB().oDelete(desql)
        if updateSql:
            logger.info('='*20+f'执行用例前置update:{updateSql}语句'+'='*20)
            for upsql in updateSql.split(';'):
                dbsql.DB().oUpdate(upsql)
        if  selectSql:
            logger.info('='*20+f'执行用例前置查询{selectSql}且替换参数{data}操作'+'='*20)
            for sesql in selectSql.split(';'):
               # 查询结果返回后依次替换接口data中的变量
                data = sqlsub.oRpl(data, dbsql.DB().oSelect(sesql))
    except Exception as e:
        logger.error('='*20+'执行用例前置sql 异常'+'='*20)
        logger.error(e)
    # 替换data里的guid
    try:
        logger.info('='*20+'执行guid参数替换操作'+'='*20)
        data = sqlsub.oRpl(data, randomly.uuid())
    except Exception as e:
        logger.error('='*20+'执行guid参数替换操作异常'+'='*20)
        logger.error(e)
    # 执行请求
    try:
        if  method == 'post':
            if system == 'omp':
                s = session['ompsession']
                url = ''.join([omphost,subUrl])
                logger.info('='*20+f'执行{url}的post请求'+'='*20)
                logger.info('='*20+f'请求的s为{str(s)}'+'='*20)
                logger.info('='*20+f'data数据为:{str(data)}'+'='*20)
                logger.info('='*20+f'caseYmldata数据为:{str(caseYmldata)}'+'='*20)
                if testheaders:
                    headers = testheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)            
                    result = apiMethod.post(s, caseYmldata,url,headers,data)
                else:
                    headers = basicheaders   
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)     
                    result = apiMethod.post(s, caseYmldata,url,headers,data)
            elif system == 'obp':
                s = session['obpsession']
                url = ''.join([obphost, subUrl])
                logger.info('='*20+f'执行{url}的post请求'+'='*20)
                logger.info('='*20+f'data数据为:{str(data)}'+'='*20)
                logger.info('='*20+f'caseYmldata数据为:{str(caseYmldata)}'+'='*20)
                if testheaders:
                    headers = testheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)     
                    result = apiMethod.post(s, caseYmldata,url,headers,data)
                else:
                    headers = basicheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)     
                    result = apiMethod.post(s, caseYmldata,url,headers,data)
            else:
                s = session['ospsession']
                url = ''.join([osphost, subUrl])
                logger.info('='*20+f'执行{url}的post请求'+'='*20)
                logger.info('='*20+f'data数据为:{str(data)}'+'='*20)
                logger.info('='*20+f'caseYmldata数据为:{str(caseYmldata)}'+'='*20)
                if testheaders:
                    headers = testheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)    
                    result = apiMethod.post(s, caseYmldata,url,headers,data)
                else:
                    headers = basicheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)    
                    result = apiMethod.post(s, caseYmldata,url,headers,data)
        elif method == 'get':
            if system == 'omp':
                s = session['ompsession']
                url = ''.join([omphost, subUrl])
                logger.info('='*20+f'执行{url}的post请求'+'='*20)
                logger.info('='*20+f'data数据为:{str(data)}'+'='*20)
                if testheaders:
                    headers = testheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)   
                    result = apiMethod.get(s, url, headers, data)
                else:
                    headers = basicheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)   
                    result = apiMethod.get(s, url, headers, data)
            elif system == 'obp':
                s = session['obpsession']
                url = ''.join([obphost, subUrl])
                logger.info('='*20+f'执行{url}的post请求'+'='*20)
                logger.info('='*20+f'data数据为:{str(data)}'+'='*20)
                if testheaders:
                    headers = testheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)   
                    result = apiMethod.get(s, url, headers, data)
                else:
                    headers = basicheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)   
                    result = apiMethod.get(s, url, headers, data)
            else:
                s = session['ospsession']
                url = ''.join([osphost, subUrl])
                logger.info('='*20+f'执行{url}的post请求'+'='*20)
                logger.info('='*20+f'data数据为:{str(data)}'+'='*20)
                if testheaders:
                    headers = testheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)   
                    result = apiMethod.get(s, url, headers, data)
                else:
                    headers = basicheaders
                    logger.info('='*20+f'headers数据为:{str(headers)}'+'='*20)   
                    result = apiMethod.get(s, url, headers, data)
        else:
            result = {'code': None, 'data': None}
        logger.info('='*20+f'获取的接口请求结果为{str(result)}'+'='*20)   
        return result
    except Exception as e:
        logger.error('='*20+f'接口请求异常'+'='*20)   
        logger.error(e)




       
