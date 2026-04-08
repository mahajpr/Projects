import smtplib
from email.message import EmailMessage
import qrcode
import os

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def generate_qr(data: str, filename: str):
    img = qrcode.make(data)
    img.save(filename)
    return filename

def send_confirmation_email(to_email: str, name: str, event:str):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    qr_file = os.path.join(BASE_DIR, f"{name}_qr.png")

    qr_text = f"{name}|{to_email}|event:{event}"
    generate_qr(qr_text, qr_file)

    msg = EmailMessage()
    msg["Subject"] = "Event Registration Confirmation"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    msg.set_content(f"""
Hello {name},

Your registration is confirmed.

Event: {event}

Please bring the attached QR code to the event for entry.

Thank you.""")

    with open(qr_file, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="image",
            subtype="png",
            filename="event_qr.png"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
        smtp.send_message(msg)

    os.remove(qr_file)
