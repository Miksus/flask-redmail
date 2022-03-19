
import pytest
from flask_redmail import RedMail
from flask import Flask

def test_user(cls_dummy_smtp):
    app = Flask("pytest")
    app.config["EMAIL_HOST"] = "localhost"
    app.config["EMAIL_PORT"] = 0
    app.config["EMAIL_USER"] = "me@example.com"
    app.config["EMAIL_PASSWORD"] = "1234"
    app.config["EMAIL_SENDER"] = "no-reply@example.com"
    app.config["EMAIL_CLS_SMTP"] = cls_dummy_smtp

    email = RedMail()
    with pytest.warns(FutureWarning):
        email.init_app(app)
    assert app.config["EMAIL_USERNAME"] == "me@example.com"
    assert app.config["EMAIL_USER"] == "me@example.com"