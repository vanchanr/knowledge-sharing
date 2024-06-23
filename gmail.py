import configparser
from smtplib import SMTP
from email.message import EmailMessage
import mimetypes
import os

config = configparser.ConfigParser()
config.read('config.ini')

class Gmail:
    def __init__(self):
        gmailConfig = config['gmail']
        self.username = gmailConfig['username']
        self.password = gmailConfig['password']

    def __enter__(self):
        self.smtp = SMTP('smtp.gmail.com', 587)
        self.smtp.starttls()
        self.smtp.login(self.username, self.password)
        return self

    def sendmail(self, recipients, subject='', body='', attachments=[]):
        msg = EmailMessage()
        msg['From'] = self.username
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.set_content(body)
        for path in attachments:
            type_, _ = mimetypes.guess_type(path)
            maintype, subtype = type_.split('/')
            with open(path, 'rb') as f:
                msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=path.split('/')[-1])
        self.smtp.send_message(msg)

    def __exit__(self, *err):
        self.smtp.quit()

if __name__ == "__main__":
    with Gmail() as gmail:
        recipients = ["rahul.vanchanagiri@gmail.com"]
        subject = "Dummy Subject"
        body = "Dummy Body"
        directory = "/media/rahul/OS/Users/rahul/Downloads"
        pdfs = []
        for file_ in os.listdir(directory):
            path = os.path.join(directory, file_)
            if os.path.isfile(path) and path.endswith('.pdf'):
                pdfs.append(path)
        gmail.sendmail(recipients, subject, body, pdfs)
