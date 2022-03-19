
import pytest
from flask_redmail import RedMail
from flask import Flask
from redmail import EmailSender

def test_creation():
    app = Flask("pytest")
    app.config["EMAIL_HOST"] = "localhost"
    app.config["EMAIL_PORT"] = 1
    email = RedMail()
    assert email.app is None

    email.init_app(app)
    assert email.teardown in app.teardown_appcontext_funcs

    app = Flask("pytest")
    app.config["EMAIL_HOST"] = "localhost"
    app.config["EMAIL_PORT"] = 1
    email = RedMail(app)
    assert email.teardown in app.teardown_appcontext_funcs

def test_creation_missing():
    app = Flask("pytest")
    with pytest.raises(RuntimeError):
        RedMail(app)
    email = RedMail()
    with pytest.raises(RuntimeError):
        email.init_app(app)

def test_with_context(cls_dummy_smtp):
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
        assert email.sender.host == "localhost"
        assert email.sender.port == 0
        assert email.sender.user_name == "me@example.com"
        assert email.sender.password == "1234"

        assert email.sender.sender == "no-reply@example.com"
        assert email.sender.subject is None

        assert email.sender.templates_html is app.jinja_env
        assert email.sender.templates_text is app.jinja_env
        
    assert email.sender is None

def test_with_context_defaults(cls_dummy_smtp):
    app = Flask("pytest")
    app.config["EMAIL_HOST"] = "localhost"
    app.config["EMAIL_PORT"] = 0
    app.config["EMAIL_SENDER"] = "no-reply@example.com"
    app.config["EMAIL_CLS_SMTP"] = cls_dummy_smtp

    email = RedMail(sender="some-reply@example.com", subject="An example")
    email.init_app(app)
    assert email.sender is None

    with app.app_context():
        assert email.sender.host == "localhost"
        assert email.sender.port == 0
        assert email.sender.user_name == None
        assert email.sender.password == None

        assert email.sender.sender == "some-reply@example.com"
        assert email.sender.subject == "An example"

        assert email.sender.templates_html is app.jinja_env
        assert email.sender.templates_text is app.jinja_env
        
    assert email.sender is None