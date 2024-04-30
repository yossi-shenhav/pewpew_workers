#!/usr/bin/env python
import requests
import smtplib
import email.mime.text
import os
#from upload import upload2_s3
from config1 import read_secret, GMAIL_ADDRESS, GMAIL_PASSWORD, BUCKET_URL, WEB_URL


from email.mime.text import MIMEText


def sendSMTP_old(to_email, subject, message):
	from_email = read_secret(GMAIL_ADDRESS)
	pwd = read_secret(GMAIL_PASSWORD)
	msg = MIMEText(message,'html')
	msg['Subject'] = subject
	msg['From'] = from_email
	msg['To'] = to_email
	try:
		s = smtplib.SMTP_SSL('smtp.gmail.com', '465')
		s.set_debuglevel(1)
		s.login(from_email, pwd)
		s.sendmail(from_email, to_email, msg.as_string())
		s.quit()
		print("Email sent successfully!")
	except Exception as e:
		print("Email sending failed:", e)
		#print(f'Email:={from_email},	PWD:={pwd}')		


def sendEmail(email, tid, scantype, success):

    subject = 'Scan results from PewPew'

    if success:
        message = f'<p>Scan results can be found on {BUCKET_URL}/{tid}</p><p>short reprt can be found on {WEB_URL}/reports/{tid}/{scantype}</p>' 
    else:
        print("{tid} Failed to upload file.")
        message = f'<p>Scan #{tid} did not suceeded </p>'

    sendSMTP(email, subject, message)

    return 1


def sendSMTP(email, subject, message):
    pwd = read_secret(GMAIL_PASSWORD)
    api_url = f"{WEB_URL}/sendmail"
    params = {
        "email": email,
        "subject": subject,
        "msg": message,
        "pwd": pwd
    }
    
    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to send email. Server responded with status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"An error occurred while sending email: {e}")
        return False

