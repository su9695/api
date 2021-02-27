import os,sys
BASIC_DIR = os.path.dirname(__file__)
sys.path.append(BASIC_DIR)

# data 数据源目录
DATA_DIR = os.path.join(BASIC_DIR, 'testdata')
#excel 数据源路径
EXCEL_DIR = os.path.join(DATA_DIR,'excel')
#yaml 数据源路径
YML_DIR = os.path.join(DATA_DIR,'yaml')
#attch 数据源路径
ATT_DIR = os.path.join(DATA_DIR,'attchment')

# logs 日志大目录
LOGS_DIR = os.path.join(BASIC_DIR, 'logs')
# 所有日志信息
ALL_LOG_DIR = os.path.join(LOGS_DIR, 'all_logs')
ERROR_LOG_DIR = os.path.join(LOGS_DIR, 'error_logs')

# testcases测试用例目录
TESTCASES_DIR = os.path.join(BASIC_DIR, 'testcases')

# reports报告目录
REPORTS_DIR = os.path.join(BASIC_DIR, 'report/allure_raw')

# conf.ini 路径
CONF_DIR =  os.path.join(BASIC_DIR, 'conf.ini')

