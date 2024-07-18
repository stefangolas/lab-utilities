# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:18:59 2023

@author: stefa
"""

from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def get_last_tracefile():
    dirpath = "C:\\Program Files (x86)\\Hamilton\\LogFiles"
    dirfiles = os.listdir(dirpath)

    files_times = [(f, os.path.getmtime(os.path.join(dirpath, f))) for f in dirfiles if '_Trace.trc' in f]
    files_times.sort(key=lambda s:s[1])
    last_trc_file = files_times[-1][0]

    last_trc_path = os.path.join(dirpath, last_trc_file)
    return last_trc_path


def send_email(sender_email, sender_password, recipient_emails, subject, body, file_path = None):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ', '.join(recipient_emails)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))
        
        if file_path:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
        
            encoders.encode_base64(part)

            filename = os.path.basename(file_path)
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            message.attach(part)

        server.sendmail(sender_email, recipient_emails, message.as_string())
        print('Email sent successfully')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        server.quit()

def set_email_env_variables():
    bat_filename = 'set_email_env_vars.bat'
    package_path = os.path.dirname(__file__)
    script_path = os.path.join(package_path, bat_filename)
    subprocess.call([script_path])


def get_email_env_variables():
    email = os.environ.get('lab_utilities_email')
    password = os.environ.get('lab_utilities_email_password')

    return email, password


def email_error(recipients, subject, error, file):
    email_address, password = get_email_env_variables()
    send_email(email_address, password, recipients, subject, error, file)
