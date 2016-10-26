#coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from conf import mail_conf


def send_mail(to_mail, title, content):
    username = mail_conf['username']
    password = mail_conf['password']
    smtp_server = mail_conf['smtp_server']
    from_mail = mail_conf['mail_address']

    smtp = smtplib.SMTP()
    smtp.connect(smtp_server)
    smtp.starttls()
    smtp.login(username, password)

    for mail in to_mail.split(','):
        msgRoot = MIMEMultipart('related')
        msgRoot['To'] = '<'+mail+'>'
        msgRoot['From'] = u'<%s>' % from_mail
        msgRoot['Subject'] = title
        msgText = MIMEText(content, 'html', 'utf-8')
        msgRoot.attach(msgText)

        smtp.sendmail(from_mail, mail, msgRoot.as_string())
        print 'Send To: %s' % (mail)

    smtp.quit()

if __name__ == '__main__':
    send_mail('649321688@qq.com', 'test', 'test')


