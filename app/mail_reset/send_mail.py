import smtplib
#from app.config import MAIL_PASSWORD, MAIL_SERVER, MAIL_USERNAME, MAIL_PORT
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(mail_to, message, subject):
    
    msg = MIMEMultipart()
    msg['Subject'] = 'Réinitialisation'
    msg['From'] = os.environ.get('MAIL_USERNAME')
    msg['To'] = mail_to
    msg['CC'] = os.environ.get('MAIL_USERNAME')
    msg['BCC'] = os.environ.get('MAIL_USERNAME')  
    
    msg.attach(MIMEText(message, 'html'))
    try :
        with smtplib.SMTP(os.environ.get('MAIL_SERVER'), port= os.environ.get('MAIL_PORT')) as smtp:
            smtp.ehlo()
            smtp.starttls()
            
            smtp.login(os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD'))
            
            smtp.send_message(msg)
            flash('Mail envoyé')
    except Exception as e:
        return "error"