#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   rdExcelData.py
@Time    :   2021/02/20 19:52:36
@Author  :   Su 
@Contact :   411649157@qq.com
'''
# here put the import lib
import os
import sys
import xlrd
import logs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dirs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logger = logs.Logger('getExcel').getlog()


class RdExcelData(object):
    def __init__(self, testDataPath=None):
        '''
        testDataPath默认使用系统给定的路径，也可自定义
        '''
        if testDataPath == None:
            self._testDataPath = dirs.EXCEL_DIR
        else:
            self._testDataPath = testDataPath
    def getData(self):
        '''
        1 循环每个excel
        2 将每个excel第一行作为key，其他行作为value 两两zip 生成字典后 添加到list中
        '''
        try:
            excelData=[]
            # 遍历所有excel
            excelfileNames = os.listdir(self._testDataPath)  # 当前excel路径下所有的excel文件，list格式
            if len(excelfileNames)==0:
                logger.error("empty filelist")
            for excelPath in excelfileNames:
                if os.path.splitext(excelPath)[1] not in ['.xls','.xlsx']:
                    logger.error('must be excel file')
                data = xlrd.open_workbook(self._testDataPath+'/'+excelPath)
                sheetData = data.sheet_names()
                # 遍历所有sheet
                for sht in sheetData: 
                    sheetTable=data.sheet_by_name(sht)
                    # 每个sheet下总行数
                    tRows=sheetTable.nrows
                    if tRows==0:
                        logger.error(excelPath+':'+sht+'first row empty')
                    # 第一行（行数下标为0）即标题行作为key
                    key=sheetTable.row_values(0)          
                    i=1
                    for j in range(tRows-1):
                        # 从第一行开始循环
                        values = sheetTable.row_values(i) 
                        for k in range(len(values)):
                            if len(values[k].strip()) == 0:
                                values[k] = None
                        excelData.append(dict(zip(key, values)))
                        i+=1
            logger.info('='*20+f'读取所有excel数据操作'+'='*20)
            return excelData
        except Exception as e:
            logger.error('='*20+f'读取所有excel数据操作异常'+'='*20)
            logger.error(e)
    def getDataByExcelNames(self,*excelNames):
        '''
        1 循环给定excel的所有sheet 获取数据
        2 将每个excel第一行作为key，其他行作为value 两两zip 生成字典后 添加到list中
        3 param : *excelNames 一个给定的excelname list

        '''
        try:
            excelData = []
            if len(excelNames)==0:
                logger.error('empty excelNameList')
            for excelName in excelNames:
                if os.path.splitext(excelName)[1] not in ['.xls', '.xlsx']:
                    logger.error('must be excel file')
                data = xlrd.open_workbook(self._testDataPath+'/'+excelName)
                sheetData = data.sheet_names()
                # 遍历所有sheet
                for sht in sheetData: 
                    sheetTable=data.sheet_by_name(sht)
                    # 每个sheet下总行数
                    tRows=sheetTable.nrows
                    if tRows == 0:
                        logger.error(excelName+':'+sht+'first row empty')
                    # 第一行（行数下标为0）即标题行作为key
                    key=sheetTable.row_values(0)
                    i=1
                    for j in range(tRows-1):
                    # 从第一行开始循环
                        values = sheetTable.row_values(i)
                        for k in range(len(values)):
                            if len(values[k].strip()) == 0:
                                values[k] = None
                        excelData.append(dict(zip(key, values)))
                        i+=1
                logger.info('='*20+f'根据给定的excel:{str(excelNames)}读取数据'+'='*20)
                return excelData
        except Exception as e:
            logger.error('='*20+f'根据给定的excel:{str(excelNames)}读取数据异常'+'='*20)
            logger.error(e)
    def getDataByExcelSheetNames(self,excelName,*sheetNames):
        '''
        1 循环给定excel的sheet 获取数据
        2 将sheet第一行作为key，其他行作为value 两两zip 生成字典后 添加到list中
        3 param : excelNames 一个给定的excelname,str类型
        4 param ：*sheetNames 一个给定的 sheetnames list 类型
        '''
        try:
            excelData=[]
            if os.path.splitext(excelName)[1] not in ['.xls', '.xlsx']:
                logger.error('must be excel file')
            if len(sheetNames) == 0:
                logger.error('empty sheet list')
            for sht in sheetNames:
                sheetTable = xlrd.open_workbook(self._testDataPath+'/'+excelName).sheet_by_name(sht)
                # sheet下总行数
                tRows = sheetTable.nrows
                if tRows==0:
                    logger.error(excelName+':'+sht+'first row empty')
                # 第一行（行数下标为0）即标题行作为key
                key = sheetTable.row_values(0)
                i = 1
                for j in range(tRows-1):
                    # 从第一行开始循环
                    values = sheetTable.row_values(i)
                    for k in range(len(values)):
                        if len(values[k].strip()) == 0:
                            values[k] = None
                    excelData.append(dict(zip(key, values)))
                    i += 1
                logger.info('='*20+f'根据给定的excel:{str(excelName)}和sheet:{str(sheetNames)}读取数据'+'='*20)
            return excelData
        except Exception as e:
            logger.error('='*20+f'根据给定的excel:{str(excelName)}和sheet:{str(sheetNames)}读取数据异常'+'='*20)
            logger.error(e)


