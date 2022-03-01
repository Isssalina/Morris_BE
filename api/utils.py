import smtplib
from email.mime.text import MIMEText


def sent_email(receiver, username, password):
    host = 'smtp.163.com'
    port = 465
    sender = 'hiringagency@163.com'
    pwd = 'LKELETHVEIEPFWXZ'
    body = f"""<h1>Welcome to Hiring Agency!</h1>
Your account information is as follows:<br>
Username: <strong>{username}</strong><br>
Password: <strong>{password}</strong>
"""
    # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html')
    msg['subject'] = 'Welcome to Hiring Agency!'
    msg['from'] = sender
    msg['to'] = receiver
    try:
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
        return True
    except smtplib.SMTPException:
        return False

