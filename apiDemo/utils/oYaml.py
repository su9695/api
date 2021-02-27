import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dirs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import  yaml
import logs


logger = logs.Logger('handerYml').getlog()

class HandlerYaml(object):
    def __init__(self,ymlPath=None):
        if ymlPath == None:
            self.ymlPath = dirs.YML_DIR  # YAML 文件路径
        else:
            self.ymlPath = ymlPath
    def rdYml(self,ymlFile,key=None,sKey=None):
        '''
        :param ymlFile: 读取的文件名称
        :param key: 根据传入的key值读取对于的内容,，如果默认则返回所有读取内容
        '''
        try:
            with open(os.path.join(self.ymlPath,ymlFile), 'r', encoding='utf-8') as f:
                if key:
                    if sKey:
                        logger.info('='*20+f'根据{key}:{sKey}读取{ymlFile}数据'+'='*20)
                        return yaml.load(f.read(),Loader=yaml.Loader)[key][sKey]
                    else:
                        logger.info('='*20+f'根据{key}读取{ymlFile}数据'+'='*20)
                        return yaml.load(f.read(),Loader=yaml.Loader)[key]
                else:
                    logger.info('='*20+f'读取{ymlFile}数据'+'='*20)
                    return yaml.load(f.read(), Loader = yaml.Loader)
        except Exception as e:
            logger.error('='*20+f'根据key:{key}读取{ymlFile}数据失败'+'='*20)
            logger.error(e)
    def wtYaml(self, ymlFile,ySection=None,k=None,v=None):
        '''
        传入 ySection:{k,v}的组合值进行写入或修改
        :param ymlFile: 写入的文件名称
        :param ySection: yaml最外项目
        :param k: 第二层的key
        :param v: 第二层的value
        '''
        try:
            if ySection !=None and k !=None and v!=None:
                if not isinstance(ySection,str):
                    logger.error('ySection must be str')
                if not isinstance(k,(str,int,float,bool)):    
                    logger.error('k must be 不可变类型')
                # 传入的ySection:{k,v} 组合成新的字典
                data = {ySection:{k:v}}
                # 读取 yaml 文件已存在的内容
                old_data = self.rdYml(ymlFile)
                # 若ySection和k都已存在，则直接修改
                if ySection in old_data:
                    if k in old_data[ySection]:
                        old_data[ySection][k] = v
                        with open(os.path.join(self.ymlPath, ymlFile), 'w', encoding='utf-8') as f:
                            yaml.dump(old_data,f,allow_unicode=True)
                            logger.info('='*20+f'{ymlFile}:{ySection}:{k}更新{v}'+'='*20)
                    else:
                        # 若ySection存在，k不存在，则直接追加
                        old_data[ySection][k] = v
                        with open(os.path.join(self.ymlPath, ymlFile), 'a', encoding='utf-8') as f:
                            yaml.dump(old_data,f,allow_unicode=True)
                            logger.info('='*20+f'{ymlFile}:{ySection}更新{k}:{v}'+'='*20)

                else :
                    # 若ySection和k都不存在，则直接添加
                    with open(os.path.join(self.ymlPath, ymlFile), 'a', encoding='utf-8') as f:
                        yaml.dump(data,f,allow_unicode=True)
                        logger.info('='*20+f'文件{ymlFile}写入{ySection}:{k}:{v}'+'='*20)
        except Exception as e:
            logger.error('='*20+f'文件{ymlFile}写入{ySection}:{k}:{v} 异常'+'='*20)
            logger.error(e)
    def wtDictYaml(self, ymlFile,yDict=None):
        '''
        直接写一个字典
        :param ymlFile: 写入的文件名称
        :param yDict: 写入的字典
        '''
        try:
            if yDict != None:
                if not isinstance(yDict,dict):
                 logger.error('yDict must be dict')
            with open(os.path.join(self.ymlPath, ymlFile), 'a', encoding='utf-8') as f:
                yaml.dump(yDict,f,allow_unicode=True)
                logger.info('='*20+f'文件{ymlFile}写入{yDict}数据'+'='*20)
        except Exception as e:
            logger.error('='*20+f'文件{ymlFile}写入{yDict} 异常'+'='*20)
            logger.error(e)

