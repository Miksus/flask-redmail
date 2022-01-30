
from flask_redmail import RedMail
from flask import Flask
from redmail import EmailSender

def test_creation():
    app = Flask("pytest")
    email = RedMail()
    assert email.app is None

    email.init_app(app)
    assert email.teardown in app.teardown_appcontext_funcs

    app = Flask("pytest")
    email = RedMail(app)
    assert email.teardown in app.teardown_appcontext_funcs


def test_with_context():
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
        assert email.sender.host == "localhost"
        assert email.sender.port == 0
        assert email.sender.user_name == "me@example.com"
        assert email.sender.password == "1234"

        assert email.sender.sender == "no-reply@example.com"
        assert email.sender.subject is None

        assert email.sender.templates_html is app.jinja_env
        assert email.sender.templates_text is app.jinja_env
        
    assert email.sender is None