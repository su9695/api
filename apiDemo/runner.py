import pytest 
import os,sys
import caseGenerate
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import oConfig,logs,randomly
import dirs 

logger = logs.Logger('startup').getlog()

if __name__ == "__main__":

    # 生成本次运行的时间戳
    logger.info('='*20+'生成本次用例运行的时间戳'+'='*20)
    timestamp = randomly.timeStamp()
    logger.info('='*20+f'时间戳为{str(timestamp)}'+'='*20)
    logger.info('='*20+'执行测试用例自动生成操作'+'='*20)
    caseGenerate.caseGenerate()
    logger.info('='*50)
    # 执行时的参数
    n = oConfig.HandleConfig().rdConfig('startup','n')
    reruns = oConfig.HandleConfig().rdConfig('startup', 'reruns')
    maxfail = oConfig.HandleConfig().rdConfig('startup', 'maxfail')
    args_list = ['-vs', dirs.TESTCASES_DIR,
                 '-n', str(n),
                 '--reruns', str(reruns),
                 '--maxfail', str(maxfail),
                 '--alluredir', './apidemo/report/allure_raw',
                 '--clean-alluredir']
    # 执行测试
    pytest.main(args_list)
    #生成Allure测试报告
    cmd = f'allure serve {dirs.REPORTS_DIR}'
    os.system(cmd)
