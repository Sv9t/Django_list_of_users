# -*- coding: utf-8 -*-

from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64


def send_email(link, name_pdf):
    """ 
    SEND PDF FILE for SMTP
    """

    recipients = ['users@mail.com', 'users2@mail.com']
    # body = f"Прикрепил pdf"

    server = 'HOST_SERVER_MAIL'
    username = 'USERNAME_OF_AUTH'
    password = "PASSWORD_OF_AUTH"
    sender = "MAIL_SENDER"

    to = ",".join(recipients)
    # charset = "utf-8"

    # msg = MIMEMultipart()
    # message = f'Send from Hostname'
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = name_pdf

    # msg.attach(MIMEText(message, "plain"))

    with open(link, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
    name_pdf = to_base64(name_pdf)
    attach.add_header('Content-Disposition', 'attachment',
                      filename=name_pdf)
    msg.attach(attach)

    s = SMTP(server, 25)
    try:
        s.connect(server, 25)
    except:
        print(f"Не могу подключится к smtp серверу: {server}")
        return False

    s.login(username, password)
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()
    return True


def to_base64(s):
    """
    decode in UTF-8
    """
    b = s.encode("UTF-8")
    e = base64.b64encode(b)
    s1 = e.decode("UTF-8")
    s2 = '=?utf-8?b?%s?=' % (s1)
    return s2
