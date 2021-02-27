import sys,os,logs
from oConfig import HandleConfig
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dirs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import smtplib
from email.mime.multipart import MIMEMultipart    
from email.mime.text import MIMEText    
from email.mime.image import MIMEImage 
from email.header import Header   

logger = logs.Logger('smtpEmail').getlog()
class Mail(object):
    '''
    读取配置文件中的mail数据
    '''
    def __init__(self):
        self.host = HandleConfig().rdConfig('smtp','host')
        self.port = HandleConfig().rdConfig('smtp','port')
        self.userName = HandleConfig().rdConfig('smtp','username')
        self.password = HandleConfig().rdConfig('smtp','password')
        self.sender = HandleConfig().rdConfig('smtp','sender')
        self.recivers = HandleConfig().rdConfig('smtp','recivers')
        self.subject = HandleConfig().rdConfig('smtp','subject')
    def sendMail(self,attchPath=None,reportPath=None):
        '''
        :param attchPath: 附件地址，如本次运行的日志地址
        :param reportPath:  报告地址
        '''
        msg=MIMEMultipart('mixed')
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = ";".join(self.recivers) 

        # 构造文字
        timeStamp = HandleConfig().rdConfig('stamp','value')
        text =  "hello ,当你看到这个邮件的时候，代表我们又一次执行了测试用例。timestamp is {0}, ".format(timeStamp)
        text_plain = MIMEText(text,'plain','utf-8')
        msg.attach(text_plain)

        # 构造附件
        attchPath = os.path.join(dirs.ALL_LOG_DIR,timeStamp+'.txt')
        sendFile = open(attchPath,'rb').read()
        text_att = MIMEText(sendFile, 'base64', 'utf-8') 
        text_att['Content-Type'] = 'application/octet-stream' 
        text_att.add_header('Content-Disposition', 'attachment', filename=timeStamp+'.txt')
        msg.attach(text_att)
        try:
            smtp=smtplib.SMTP()
            smtp.connect(self.host,self.port)
            smtp.login(self.userName,self.password)
            smtp.sendmail(self.sender,self.recivers,msg.as_string())
            logger.info('='*20+'执行邮件发送操作'+'='*20)
        except Exception as e:
            logger.error('='*20+'执行邮件发送操作异常'+'='*20)
            logger.error(e)



