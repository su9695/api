import pymssql
import json
from oConfig import HandleConfig
import os,sys
import logs

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logger = logs.Logger('dblog').getlog()

class DB(object):
    def __init__(self):
        '''
        从配置文件中读取各项数据库连接数据
        '''
        try:
            host=HandleConfig().rdConfig('db','server')
            username=HandleConfig().rdConfig('db','username')
            password=HandleConfig().rdConfig('db','password')
            dbname=HandleConfig().rdConfig('db','dbname')
            self.conn = pymssql.connect(host,username,password,dbname)
            logger.info('='*20+f'连接数据库{host}成功'+'='*20)
        except Exception as e:
            logger.error('='*20+f'连接数据库{host}失败'+'='*20)
            logger.error(e)
    def oSelect(self,selectSql):
        '''
        :param selectSql: sql查询语句，来源于excel select列
        :fecthone,fecthmany和fecthall:目前只用到fecthone
        '''
        try:
            # 返回结果为字典形式{}
            cursor=self.conn.cursor(as_dict=True)
            if not isinstance(selectSql,str):
                raise TypeError('selectSql must be str')
            cursor.execute(selectSql)
            rDict= cursor.fetchone() # 只返回一条记录
            '''
            查询返回的dict，key和value值转换为str类型存储在新的字典中
            '''
            sDict={}
            for k,v in rDict.items():
                sDict[str(k)]=str(v) 
            logger.info('='*20+f'数据库执行{selectSql}查询,结果为{str(sDict)}'+'='*20)
            return sDict
        except Exception as e:
            logger.error('='*20+f'数据库执行{selectSql}查询操作异常'+'='*20)
            logger.error(e)
        finally:
            self.conn.close()
    def oUpdate(self,updateSql):
        '''
        执行数据库update操作
        ：param updateSql: excel updatesql列的数据
        '''
        try:
            cursor=self.conn.cursor()
            if not isinstance(updateSql,str):
                raise TypeError('updateSql must be str')
            cursor.execute(updateSql)
            self.conn.commit()
            logger.info('='*20+f'数据库执行{updateSql}更新操作'+'='*20)
        except Exception as e:
            logger.error('='*20+f'数据库执行{updateSql}更新操作异常'+'='*20)
            logger.error(e)
            self.conn.rollback()
        finally:
            self.conn.close()
    def oDelete(self,deleteSql):
        '''
        执行数据库delete操作
        ：param deleteSql: excel deleteSql列的数据
        '''
        try:
            cursor=self.conn.cursor()
            if not isinstance(deleteSql,str):
                raise TypeError('deleteSql must be str')
            cursor.execute(deleteSql)
            self.conn.commit()
            logger.info('='*20+f'数据库执行{deleteSql}删除操作'+'='*20)
        except Exception as e:
            logger.info('='*20+f'数据库执行{deleteSql}删除操作异常'+'='*20)
            logger.error(e)
            self.conn.rollback()
        finally:
            self.conn.close()
