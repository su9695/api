import os,sys
import shutil
import dirs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import oConfig, logs

logger =logs.Logger('case_Generate').getlog()

def caseGenerate():
    try:
        # 获取yaml路径下的所有测试用例yaml文件
        caseNames = [os.path.basename(os.path.splitext(x)[0]) for x in os.listdir(dirs.YML_DIR) if 'test' in x]
        for i in range(len(caseNames)):
            caseTemplate = os.path.join(dirs.TESTCASES_DIR, 'caseTemplate.py')
            caseFile = os.path.join(dirs.TESTCASES_DIR, caseNames[i]+'.py')
            if not os.path.isfile(caseFile):
                logger.info('='*20+f'执行测试用例文件{str(caseFile)}创建'+'='*20)
                with open(caseFile,'w',encoding='utf-8') as f:
                    f.close()
                logger.info('='*20+f'将用例模板数据复制到{caseFile}'+'='*20)
                shutil.copy(caseTemplate, caseFile)
            else:
                logger.info('='*20+f'yaml文件{str(caseNames)}对应的的测试用例文件{str(caseFile)}已存在'+'='*20)
    except Exception as e:
        logger.error('='*20+'生成用例文件异常'+'='*20)
        logger.error(e)

