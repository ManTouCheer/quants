from __future__ import annotations
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from log_helper import LogHelper
from configs.setting import email_cfg
from system.decorator import cost_time

logger = LogHelper(name ="quants.email_helper", level="INFO")


class EmailHelper(object):

    def __init__(self):
        self.address = email_cfg.user_name
        self.password = email_cfg.password
        self.server = email_cfg.server
        self.port = email_cfg.port

    @classmethod
    def create_form_email(cls, address: str, password: str, server: str, port: int) -> EmailHelper:
        email_cls = EmailHelper()
        email_cls.address = address
        email_cls.password = password
        email_cls.server = server
        email_cls.port = port
        return email_cls

    @cost_time
    def send_message(self, recipient_email: str, msg_text: str):
        # 登录服务器
        message = MIMEText(msg_text)

        message["From"] = formataddr(("发件人昵称", email_cfg.user_name))
        message["To"] = formataddr(("收件人昵称", recipient_email))
        message["Subject"] = u'测试email class'
        message['Accept-Language'] = 'zh-CN'
        message['Accept-Charset'] = 'ISO-8859-1,utf-8'
        try:
            self.smtp_connection = smtplib.SMTP(self.server, self.port)
            self.smtp_connection.login(self.address, self.password)
            # 发送邮件
            self.smtp_connection.sendmail(self.address, recipient_email, message.as_string())
            # 关闭连接
            self.smtp_connection.quit()
            print("发送邮件成功")
        except Exception as e:
            print("发送邮件失败", e)


if __name__ == "__main__":
    recipient_email = "lslishanls@163.com"
    email_helper = EmailHelper()
    email_helper.send_message(recipient_email, msg_text="测试发送纯文本")
    # logger.info("finish")
