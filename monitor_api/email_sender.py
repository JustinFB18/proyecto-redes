import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(recipient_email, subject, body):
    sender_email = "jusfb18@gmail.com"
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

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

send_email("academicodiana08@gmail.com", "hola", "hola")