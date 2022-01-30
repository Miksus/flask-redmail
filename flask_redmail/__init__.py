
from flask import current_app, _app_ctx_stack, Flask
from redmail import EmailSender, send_email

class RedMail(object):
    """Email sender for Flask

    Examples
    --------

        .. code-block::

            from flask import Flask
            from flask_redmail import RedMail

            app = Flask(__name__)
            app.config.from_pyfile('the-config.cfg')
            email = RedMail(app)

    Parameters
    ----------
    app : flask.Flask, optional
        Flask application
    """
    def __init__(self, app:Flask=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app:Flask):
        #app.config.setdefault('SQLITE3_DATABASE', ':memory:')
        app.teardown_appcontext(self.teardown)

    def send(self, **kwargs):
        sender = self.sender
        return sender.send(**kwargs)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'redmail_sender'):
            if hasattr(ctx.redmail_sender, "close"):
                # Red Mail >= 0.3.0
                ctx.redmail_sender.close()

    @property
    def sender(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'redmail_sender'):
                ctx.redmail_sender = self._create_sender()
                if hasattr(ctx.redmail_sender, "close"):
                    # Red Mail >= 0.3.0
                    ctx.redmail_sender.connect()
            return ctx.redmail_sender

    def _create_sender(self) -> EmailSender:
        app_config = current_app.config
        email_sender = EmailSender(
            host=app_config['SMTP_HOST'],
            port=app_config['SMTP_PORT'],
            user_name=app_config.get("SMTP_USER"),
            password=app_config.get("SMTP_PASSWORD")
        )
        email_sender.sender = app_config.get('SMTP_SENDER')

        email_sender.templates_html = current_app.jinja_env
        email_sender.templates_text = current_app.jinja_env
        return email_sender