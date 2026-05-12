import smtplib
from email.mime.text import MIMEText

def send_email(message):

    sender = "your_email@gmail.com"
    password = "app_password"
    receiver = "your_email@gmail.com"

    msg = MIMEText(message)
    msg["Subject"] = "IT Asset Update"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)

    server.sendmail(sender, receiver, msg.as_string())
    server.quit()