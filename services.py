import smtplib
import os

from email.message import EmailMessage

def send_email(email_reciever,OTP):
    sender_email= os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")

    if not sender_email or not sender_password:
        raise ValueError("Sender email or password is missing")
    message = EmailMessage()
    message["Subject"] = "Password Reset OTP"
    message["From"] = sender_email
    message["To"] = email_reciever

    message.set_content("Your OTP is " + OTP + ". It will expire in 5 minutes.")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)

    
    
    
