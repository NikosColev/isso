# -*- encoding: utf-8 -*-

from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText


def format(comment, permalink, remote_addr):

    rv = []
    rv.append("%s schrieb:" % (comment["author"] or "Jemand"))
    rv.append("")
    rv.append(comment["text"])
    rv.append("")

    if comment["website"]:
        rv.append("Webseite des Kommentators: %s" % comment["website"])

    rv.append("IP Adresse: %s" % remote_addr)
    rv.append("Link zum Kommentar: %s" % permalink)

    return u'\n'.join(rv)


class Connection(object):

    def __init__(self, conf):
        self.conf = conf

    def __enter__(self):
        self.server = (SMTP_SSL if self.conf.getboolean('SMTP', 'ssl') else SMTP)(
            host=self.conf.get('SMTP', 'host'), port=self.conf.getint('SMTP', 'port'))

        if self.conf.get('SMTP', 'username') and self.conf.get('SMTP', 'password'):
            self.server.login(self.conf.get('SMTP', 'username'),
                              self.conf.get('SMTP', 'password'))

        return self.server

    def __exit__(self, exc_type, exc_value, traceback):
        self.server.quit()


class SMTPMailer(object):

    def __init__(self, conf):

        self.conf = conf
        self.from_addr = conf.get('SMTP', 'from')
        self.to_addr = conf.get('SMTP', 'to')

        with Connection(self.conf):
            pass

    def sendmail(self, subject, body):

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = "Ich schrei sonst! <%s>" % self.from_addr
        msg['To'] = self.to_addr
        msg['Subject'] = subject.encode('utf-8')

        with Connection(self.conf) as con:
            con.sendmail(self.from_addr, self.to_addr, msg.as_string())


class NullMailer(object):

    def sendmail(self, subject, body, retries=5):
        pass
