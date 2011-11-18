# -*- coding: utf-8 -*-

import smtplib

from email.mime.text import MIMEText


class Email(object):

    def __init__(self, server, user, password, mailto, mailfrom):
        self.server = server
        self.user = user
        self.password = password
        self.mailto = mailto
        self.mailfrom = mailfrom

    def send(self, message):
        msg = MIMEText(message, _charset="utf-8")

        msg["Subject"] = "ParcelWatch notification"
        msg["To"] = self.mailto
        msg["From"] = self.mailfrom
        msg["User-Agent"] = "smtplib"

        smtp = smtplib.SMTP(self.server)
        #smtp.set_debuglevel(1)
        smtp.login(user=self.user, password=self.password)
        smtp.sendmail(from_addr=self.mailfrom, to_addrs=self.mailto,
            msg=msg.as_string())
        smtp.quit()

        