import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json
from datetime import datetime

PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(recipient_email, subject, body, attachment_path):
    sender_email = "jusfb18@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    try:
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment_path.split('/')[-1]}")
        msg.attach(part)
        attachment.close()
    except Exception as e:
        print(f"Error attaching file: {e}")
    
    # Set up the server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, PASSWORD)

        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()


with open('./monitor_api/correos.json', 'r') as file:
    data = json.load(file)
    
with open('./monitor_api/report.txt', 'r') as file:
    report = file.readlines()

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato de fecha y hora

for employee in data['email_recipients']:
    message = f"Saludos cordiales {employee['name']} ({employee['role']})"
    send_email(employee['email'], f"Reporte {current_time} - {employee['name']}", message ,"/monitor_api/report.txt")
