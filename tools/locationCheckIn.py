import logging
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import requests
import time
from tools.lib.readConfig import getConfig

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main_handler(event):
    logger.info('got event{}'.format(event))
    sender = getConfig("Email", "sender-account")  # 修改1：填写发件人的邮件
    pass_ = getConfig("Email", "sender-password")  # 修改2：发件人邮箱授权码
    user = getConfig("Email", "addressee")  # 修改3：收件人的邮件

    getheaders = {
        "Host": "student.wozaixiaoyuan.com",
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": f"{getConfig('Settings','user-agent')}",  # 修改4：User-Agent
        "Referer": f"{getConfig('Settings','referer')}",  # 修改5：Referer
        "Content-Length": "500",
        "JWSESSION": f"{getConfig('Settings','jwsession')}",  # 修改6：JWSESSION
    }
    first = 'page=1&size=5'
    getapi = "http://student.wozaixiaoyuan.com/sign/getSignMessage.json"
    getdata = requests.post(getapi, headers=getheaders, data=first, ).json()
    time.sleep(1)
    getdata = getdata['data']
    a = str(getdata).replace("[", "")
    b = str(a).replace("]", "")
    c = b
    d = re.findall(r"{(.+?)}", c)
    e = "{" + d[0] + "}"
    e = eval(e)
    Fid = e['id']
    Lid = e['logId']
    realdata = '{"id":' + Lid + "," + '"signId":' + Fid + "," + f'''
    "latitude":{float(getConfig("Position", "latitude"))},
    "longitude":{float(getConfig("Position", "longitude"))},
    "country":{getConfig("Position", "country")},
    "province":{getConfig("Position", "province")},
    "city":{getConfig("Position", "city")},
    "district":{getConfig("Position", "district")},
    "township":{getConfig("Position", "township")}''' + "}"  # 修改7：打卡位置

    api = "http://student.wozaixiaoyuan.com/sign/doSign.json/"
    signheaders = {
        "Host": "student.wozaixiaoyuan.com",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": f"{getConfig('Settings','user-agent')}",  # 修改8：User-Agent(相同)
        "Referer": f"{getConfig('Settings','referer')}",  # 修改:7：Referer（相同）
        "Content-Length": "500",
        "Cookie": "",
        "JWSESSION": f"{getConfig('Settings','jwsession')}",  # 修改8：JWSESSION（相同）
    }
    res = requests.post(api, headers=signheaders, data=realdata.encode(), ).json()
    time.sleep(1)
    if res['code'] == 0:
        return '打卡成功'
    else:
        msg = MIMEText("打卡失败", 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr([f"{getConfig('Email', 'sender-name')}", sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([f"{getConfig('Email', 'addressee-name')}", user])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "打卡失败"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL(f"{getConfig('Email', 'smtp')}", 465)  # 发件人邮箱中的SMTP服务器
        server.login(sender, pass_)  # 发件人邮箱账号、邮箱授权码
        server.sendmail(sender, [user, ], msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        return '打卡失败'
