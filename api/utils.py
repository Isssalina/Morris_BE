import smtplib
from email.mime.text import MIMEText
import datetime


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


def is_conflict(time_schedule1, time_schedule2):
    for h in time_schedule1:
        for c in time_schedule2:
            if c['start'].date() == h['start'].date():
                if not (h['end'] <= c['start'] or h['start'] >= c['end']):
                    return True
    return False


def get_time_schedule(startDate, numDaysRequested, daysRequested, startTime, endTime, flexibleTime):
    time_schedule = []
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    startTime = datetime.datetime.strptime(startTime, "%H:%M")
    endTime = datetime.datetime.strptime(endTime, "%H:%M")
    for x in range(numDaysRequested):
        _d = startDate + datetime.timedelta(x)
        if _d.weekday() + 1 in daysRequested:
            if flexibleTime:
                s_h, s_m, s_s = 0, 0, 0
                e_h, e_m, e_s = 23, 59, 59
            else:
                s_h, s_m, s_s = startTime.hour, startTime.minute, startTime.second
                e_h, e_m, e_s = endTime.hour, endTime.minute, endTime.second
            time_schedule.append({
                "start": datetime.datetime(_d.year, _d.month, _d.day, s_h, s_m, s_s),
                "end": datetime.datetime(_d.year, _d.month, _d.day, e_h, e_m, e_s)
            })
    return time_schedule
