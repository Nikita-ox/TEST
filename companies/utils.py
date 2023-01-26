from io import BytesIO

import qrcode
from django.core.mail import EmailMessage


def make_qr(data):
    qr_pilimage = qrcode.make(data)
    stream = BytesIO()
    qr_pilimage.save(stream, format="png")
    stream.seek(0)
    return stream.read()


def send_mail(data, to_email):
    mail = EmailMessage()
    mail.subject = 'QR-code'
    mail.to = [to_email]
    qr = make_qr(data)
    mail.attach('qr.png', qr, 'image/png')
    mail.send(fail_silently=False)
