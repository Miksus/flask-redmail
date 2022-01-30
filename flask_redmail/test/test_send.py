
from flask_redmail import RedMail
from flask import Flask
from redmail import EmailSender

def dummy_send(msg):
    pass

def test_send():
    app = Flask("pytest")
    app.config["EMAIL_HOST"] = "localhost"
    app.config["EMAIL_PORT"] = 0
    app.config["EMAIL_USER"] = "me@example.com"
    app.config["EMAIL_PASSWORD"] = "1234"
    app.config["EMAIL_SENDER"] = "no-reply@example.com"

    email = RedMail()
    email.init_app(app)
    assert email.sender is None

    with app.app_context():
        email.sender.send_message = dummy_send
        email.send(
            subject="An example",
            receivers=["me@example.com"],
            html="<h1>An example</h1>"
        )
        
    assert email.sender is None