from email import message
import random
import string
from django.core.mail import send_mail
from email.message import EmailMessage
import smtplib

def generate_otp(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_otp_email(email,otp):
    print(f"sending otp to {email} with values {otp}")
    subject = 'your OTP For Register'
    from_email = 'raijocraj@gmail.com'
    recipient_list = [email]
    body = "OTP For firstcry webisite login is :"+otp
    msg = EmailMessage()
    msg['From'] = from_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.set_content(body)

    with smtplib.SMTP("sandbox.smtp.mailtrap.io",587) as server:
        server.starttls()
        server.login("1cc9807fe1da31","6b80a89906eeee")
        server.send_message(msg)
