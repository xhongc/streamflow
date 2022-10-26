import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(title, msg, from_email, to_emails, smtp_host, smtp_port, from_email_pwd, from_email_alias):
    message = MIMEText(msg, 'html', 'utf-8')
    message['From'] = Header(from_email_alias, 'utf-8')
    message['Subject'] = Header(title, 'utf-8')

    try:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        server.login(from_email, from_email_pwd)
        server.sendmail(from_email, to_emails, message.as_string())
        return True
    except smtplib.SMTPException:
        return False


if __name__ == '__main__':
    send_email(title="标题",
               msg="<a href='#'>ceshi</a>",
               from_email="408737515@qq.com",
               to_emails=["2324369231@qq.com"],
               smtp_host="smtp.qq.com",
               smtp_port=465,
               from_email_pwd="",
               from_email_alias="charles"
               )
