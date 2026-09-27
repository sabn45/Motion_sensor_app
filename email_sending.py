import smtplib
from email.message import EmailMessage
import filetype

password = "x"
sender = "x@gmail.com"
receiver = "x@gmail.com"

def send_email(image_path):
    email_message = EmailMessage()
    email_message["subject"] = "Hey, A new motion capture is detected"
    email_message.set_content("Please find the attached image of the motion capture that was detected")

    with open (image_path, "rb") as image_file:
        content = image_file.read()

    kind = filetype.guess(content)
    subtype = kind.extension if kind else "jpeg"

    email_message.add_attachment(content, maintype="image", subtype= subtype)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()

