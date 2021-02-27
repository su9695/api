#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   apiMehod.py
@Time    :   2021/02/23 10:43:04
@Author  :   Su 
@Contact :   411649157@qq.com
'''
# here put the import lib
from requests_toolbelt import MultipartEncoder
import sys,os,json
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import oConfig,logs,oYaml
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


logger = logs.Logger('basicAPImenthod').getlog()


def post(s, caseYmldata, url, headers, data, cookies=None, files=None, verify=False, allow_redirects=True, timeout=1):
    '''
    post请求
    :param caseYmldata:测试yml文件中的cookies和attchUpload 信息
    :param url: 请求地址
    :param headers: 请求头
    :param data: 请求 body
    :param cookies: 请求cookies
    :param files: 文件
    :param verify: SSL忽略
    :param allow_redirect: 默认允许重定向
    :param timeout： 超时时间
    :其他参数暂未用到:
    '''
    global response
    # 如果用例yaml中维护的mime_type有form_data的值，则执行附件上传的post
    if 'form_data' in caseYmldata['mime_type']:
        newFile={}
        for k, v in caseYmldata['files'].items():
            newFile[k] = eval(v)  
        m = MultipartEncoder(fields=newFile)
        headers['Content-Type'] = m.content_type
        # 需要使用cookies，则从basic的cookies中取值
        if caseYmldata['nCookies']:
            cookies = oYaml.HandlerYaml().rdYml('basic.yaml','cookies')
            logger.info('='*20+f'从basic.yaml 读取cookies：{str(cookies)}操作'+'='*20)
            response = s.post(url=url,headers={'Content-Type': m.content_type},data=m,cookies=cookies,verify=verify, allow_redirects=allow_redirects, timeout=timeout)  
        else:
            response = s.post(url=url,headers={'Content-Type': m.content_type},data=m,cookies=cookies,verify=verify, allow_redirects=allow_redirects, timeout=timeout)  

    else:
        # 需要使用cookies，则从basic的cookies中取值
        if caseYmldata['nCookies'] == 'Y':
            cookies = oYaml.HandlerYaml().rdYml('basic.yaml','cookies')
            logger.info('='*20+f'从basic.yaml 读取cookies：{str(cookies)}操作'+'='*20)
            response = s.post(url=url,headers=headers,data=data,cookies=cookies, files=files, verify=verify, allow_redirects=allow_redirects, timeout=timeout)
        else:
            response = s.post(url=url, headers=headers, data=data, cookies=cookies, files=files, verify=verify, allow_redirects=allow_redirects, timeout=timeout)
    try :
        if response.status_code != 200 :
            logger.info('='*20+f'接口返回状态为{str(response.status_code)}'+'='*20)
            return response.raise_for_status, response.text
        else :
            logger.info('='*20+f'接口返回状态为{str(response.status_code)}'+'='*20)
            # 需要使用存储cookies，则将cookies更新至basic的cookies下
            if caseYmldata['sCookies'] == 'Y':
                logger.info('='*20+'执行cookies保存操作'+'='*20)
                cookies=requests.utils.dict_from_cookiejar(response.cookies)
                logger.info('='*20+f'cookies信息为{str(cookies)}'+'='*20)
                ymlCookies = {'cookies': cookies}
                oYaml.HandlerYaml().wtDictYaml('basic.yaml',ymlCookies)
                logger.info('='*20+'cookies保存操作完成'+'='*20)
            return response.status_code, response.text
    except Exception as e:
        logger.error('='*20+' PostMethod Send Fail'+'='*20)
        logger.error(e)
def get(s,url, headers, data=None, timeout=1):    
    '''
    :param url: 请求地址
    :param headers: 请求头
    :param data: 请求参数
    :param timeout: 超时时间
    '''
    response = s.get(url=url, headers=headers, data=data, timeout=timeout)
    try :
        if response.status_code in [301,302]:
            logger.info('='*20+f'重定向{str(response.status_code)},地址为{str(response.headers["Location"])}'+'='*20)
            return  response.status_code, response.text
        elif response.status_code != 200:
            logger.info('='*20+f'接口返回状态为{str(response.status_code)}'+'='*20)
            return response.status_code, response.text
        else :
            logger.info('='*20+f'接口返回状态为{str(response.status_code)}'+'='*20)
            return response.status_code, response.text          
    except Exception as e:
        logger.error('='*20+' GetMethod Send Fail'+'='*20)
        logger.error(e)










