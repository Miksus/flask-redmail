import re
from textwrap import dedent
from packaging import version

from flask_redmail import RedMail
from flask import Flask
from redmail import EmailSender
import redmail

def dummy_send(msg):
    pass

def remove_email_content_id(s:str, repl="<ID>"):
    return re.sub(r"(?<================)[0-9]+(?===)", repl, s)

def test_send(cls_dummy_smtp):
    app = Flask("pytest")
    app.config["EMAIL_HOST"] = "localhost"
    app.config["EMAIL_PORT"] = 0
    app.config["EMAIL_USERNAME"] = "me@example.com"
    app.config["EMAIL_PASSWORD"] = "1234"
    app.config["EMAIL_SENDER"] = "no-reply@example.com"
    app.config["EMAIL_CLS_SMTP"] = cls_dummy_smtp

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

def test_send_defaults(cls_dummy_smtp):
    app = Flask("pytest")
    app.config["EMAIL_HOST"] = "localhost"
    app.config["EMAIL_PORT"] = 0
    app.config["EMAIL_USERNAME"] = "me@example.com"
    app.config["EMAIL_PASSWORD"] = "1234"
    app.config["EMAIL_SENDER"] = "config@example.com"
    app.config["EMAIL_CLS_SMTP"] = cls_dummy_smtp

    email = RedMail(subject="Default subject", sender="default@example.com")
    email.init_app(app)
    assert email.sender is None

    with app.app_context():
        email.sender.send_message = dummy_send
        msg = email.send(
            subject="Subject",
            receivers=["me@example.com"],
            html="<h1>An example</h1>",
            sender="sender@example.com",
        )

        if version.parse(redmail.__version__) < version.parse("0.4.0"):
            assert remove_email_content_id(str(msg)) == dedent("""
            from: sender@example.com
            subject: Subject
            to: me@example.com
            Content-Type: multipart/alternative;
             boundary="===============<ID>=="

            --===============<ID>==
            Content-Type: text/html; charset="utf-8"
            Content-Transfer-Encoding: 7bit
            MIME-Version: 1.0

            <h1>An example</h1>

            --===============<ID>==--
            """)[1:]
        else:
            assert remove_email_content_id(str(msg)) == dedent("""
            from: sender@example.com
            subject: Subject
            to: me@example.com
            Content-Type: multipart/mixed; boundary="===============<ID>=="

            --===============<ID>==
            Content-Type: multipart/alternative;
             boundary="===============<ID>=="

            --===============<ID>==
            Content-Type: text/html; charset="utf-8"
            Content-Transfer-Encoding: 7bit
            MIME-Version: 1.0

            <h1>An example</h1>

            --===============<ID>==--

            --===============<ID>==--
            """)[1:]

        
    assert email.sender is None