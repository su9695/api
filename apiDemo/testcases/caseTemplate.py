import pytest 
import allure
import os,sys
import apiSend
import requests
import resultCheck
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import oYaml,rdExcelData
import dirs 

# 根据当前用例的名称获取相同名称的yaml文件
testYaml=os.path.basename((os.path.splitext(__file__))[0])+'.yaml'
# 获取excel:sheet 存在对应的测试testYaml下
excelName = oYaml.HandlerYaml().rdYml(testYaml,'excel')
sheetName = oYaml.HandlerYaml().rdYml(testYaml,'sheet')
testData = rdExcelData.RdExcelData().getDataByExcelSheetNames(excelName,*sheetName)

class TestKF(object):

    @pytest.mark.parametrize('getParam', testData, indirect=True)
    def test_kfGroupAdd(self, getParam,oSession):
        if getParam['isSkip'] == 'Y':
            pytest.skip('skip this time')
        else :
            allure.dynamic.feature(getParam['allure_feature'])
            allure.dynamic.story(getParam['allure_story'])
            allure.dynamic.title(getParam['allure_title'])
            allure.dynamic.testcase(getParam['allure_testCaseLink'])
            allure.dynamic.issue(getParam['allure_issue'])
            allure.dynamic.description(getParam['allure_description'])
            allure.dynamic.severity(getParam['allure_severity'])
            # 返回结果为tuple
            code, data = apiSend.send_request(testYaml, getParam, oSession)
            # 验证结果
            assert  True == resultCheck.check_result(code, data,getParam)

if __name__ == "__main__":
    pytest.main(
        ['-sv', r'C:\Users\Luke\Desktop\PythonLearn\StayAtHome\apiDemo\testcases\test_kfGroupAdd.py', '--alluredir', './apidemo/report/allure_raw', '--clean-alluredir'])
    allure_report = dirs.REPORTS_DIR
    cmd = f'allure serve {allure_report}' 
    os.system(cmd)
