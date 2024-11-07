import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json
from datetime import datetime

PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(recipient_email, subject, body):
    sender_email = "jusfb18@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    html_start = "<html><body><h2>Estimado/a,</h2>"
    html_end = "<p>Atentamente, <br>Su equipo de soporte</p></body></html>"
    
    # Combina el formato inicial, el cuerpo y el formato final
    full_body = html_start + str(body) + html_end

    msg.attach(MIMEText(str(full_body), 'html'))
    
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
    report = file.read()

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato de fecha y hora

for employee in data['email_recipients']:
    message = f"Saludos cordiales {employee['name']} ({employee['role']})\n"+report
    send_email(employee['email'], f"Reporte {current_time} - {employee['name']}", message)
