import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json
from datetime import datetime

PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(recipient_email, subject, body):
    sender_email = "jusfb18@gmail.com"
    
    # Comienza el documento RTF
    rtf_header = r"{\rtf1\ansi\ansicpg1252\uc1 \deff0\nouicompat \pard\sa200\sl276\slmult1\cf1\lang9"
    
    # Comienza el cuerpo del texto RTF con formato (en este ejemplo usaremos colores)
    rtf_body = r"\cf2 "  # Color 2 (puedes mapear más colores según sea necesario)
    rtf_body += str(body).replace('\x1b[31m', r'\cf1 ')  # Reemplaza el rojo ANSI con color RTF 1
    rtf_body += r"\cf0 "  # Reset del color al final

    # Finaliza el documento RTF
    rtf_footer = r"\pard\nowidctlpar\hyphpar0\par}"
    
    # Junta todo el contenido RTF
    full_rtf_body = rtf_header + rtf_body + rtf_footer
    
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body as RTF
    msg.attach(MIMEText(full_rtf_body, 'rtf'))

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
    send_email(employee['email'], f"Reporte {current_time} - {employee['name']}", report)
