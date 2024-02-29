import smtplib
from app.config import MAIL_PASSWORD, MAIL_SERVER, MAIL_USERNAME, MAIL_PORT
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(mail_to, message, subject):
    
    msg = MIMEMultipart()
    msg['Subject'] = 'Réinitialisation'
    msg['From'] = MAIL_USERNAME
    msg['To'] = mail_to
    msg['CC'] = MAIL_USERNAME
    msg['BCC'] = MAIL_USERNAME  
    
    msg.attach(MIMEText(message, 'html'))
    try :
        with smtplib.SMTP(MAIL_SERVER, port= MAIL_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            
            smtp.send_message(msg)
            flash('Mail envoyé')
    except Exception as e:
        return "error"