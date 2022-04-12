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


def timeFormat(time_input):
    if isinstance(time_input, str):
        h, s = time_input.split(":")
        time_input = datetime.time(int(h), int(s))
    return time_input


def is_conflict(time_schedule1, time_schedule2):
    for h in time_schedule1:
        for c in time_schedule2:
            if c['start'].date() == h['start'].date():
                if not (h['end'] <= c['start'] or h['start'] >= c['end']):
                    return True
    return False


def get_time_schedule(startDate, numDaysRequested, daysRequested, startTime, endTime, flexibleTime):
    time_schedule = []
    if flexibleTime:
        s_h, s_m, s_s = 0, 0, 0
        e_h, e_m, e_s = 23, 59, 59
    else:
        startTime = datetime.datetime.strptime(startTime, "%H:%M")
        endTime = datetime.datetime.strptime(endTime, "%H:%M")
        s_h, s_m, s_s = startTime.hour, startTime.minute, startTime.second
        e_h, e_m, e_s = endTime.hour, endTime.minute, endTime.second
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    for x in range(numDaysRequested):
        _d = startDate + datetime.timedelta(x)
        if _d.weekday() + 1 in daysRequested:
            time_schedule.append({
                "start": datetime.datetime(_d.year, _d.month, _d.day, s_h, s_m, s_s),
                "end": datetime.datetime(_d.year, _d.month, _d.day, e_h, e_m, e_s)
            })
    return time_schedule


def get_work_date(startDate, numDaysRequested, daysRequested):
    dates = set()
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    for x in range(numDaysRequested):
        _d = startDate + datetime.timedelta(x)
        if _d.weekday() + 1 in daysRequested:
            dates.add(_d.strftime("%Y-%m-%d"))
    return dates


def popItem(array, key):
    new_array = []
    pop_one = None
    for item in array:
        if key(item):
            pop_one = item
        else:
            new_array.append(item)
    return pop_one, new_array
