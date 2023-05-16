from flask import render_template, current_app as app
from flask_mail import Message

from app import mail

def send_email(to, subject, template_name, **params):
    html = render_template(template_name, params=params)
    msg = Message(
        subject,
        recipients=[to],
        html=html,
        sender=app.config.get("MAIL_DEFAULT_SENDER"),
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False