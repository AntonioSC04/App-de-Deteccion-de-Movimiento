import smtplib
import os
import mimetypes
from email.message import EmailMessage

password = os.getenv("EMAIL_PASSWORD")
sender = "josantoniosc04@gmail.com"
receiver = "jantoniosc2004@gmail.com"

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Movimiento Identificado"
    email_message.set_content("Parece que el sistema identificó un objeto o persona en movimiento")

    with open(image_path, "rb") as file:
        content = file.read()

    mime_type, _ = mimetypes.guess_type(image_path)
    main_type, sub_type = mime_type.split('/')

    email_message.add_attachment(content, maintype=main_type, subtype=sub_type)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.starttls()
    gmail.login(sender, password)
    gmail.send_message(email_message)
    gmail.quit()

if __name__ == '__main__':
    send_email("imagenes/19.png")