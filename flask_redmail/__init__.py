
import smtplib
import warnings
from flask import current_app, _app_ctx_stack, Flask
from redmail import EmailSender, send_email

class RedMail:
    """Email sender for Flask

    Examples
    --------

        .. code-block::

            from flask import Flask
            from flask_redmail import RedMail

            app = Flask(__name__)
            app.config["EMAIL_HOST"] = "localhost"
            app.config["EMAIL_PORT"] = 0
            email = RedMail(app)

    Parameters
    ----------
    app : flask.Flask, optional
        Flask application
    **kwargs : dict
        Additional keyword arguments are passed to
        ``redmail.EmailSender`` as attributes.

    Attributes
    ----------
    kws_sender : dict
        Keyword arguments passed to ``redmail.EmailSender``.
        Read more from `Red Mail's documentation <https://red-mail.readthedocs.io/en/latest/references.html#redmail.EmailSender>`_
    """
    def __init__(self, app:Flask=None, **kwargs):
        self.app = app
        if app is not None:
            self.init_app(app)

        self.kws_sender = kwargs

    def init_app(self, app:Flask):
        if not ("EMAIL_HOST" in app.config and "EMAIL_PORT" in app.config):
            raise RuntimeError("Both EMAIL_HOST and EMAIL_PORT must be defined.")
        
        username = None
        if "EMAIL_USER" in app.config:
            warnings.warn("Configuration EMAIL_USER will be removed in the future. Please use EMAIL_USERNAME instead.", FutureWarning)
            username = app.config.get("EMAIL_USER")

        app.config.setdefault("EMAIL_USERNAME", username)
        app.config.setdefault("EMAIL_PASSWORD", None)

        app.config.setdefault("EMAIL_SENDER", None)

        app.config.setdefault("EMAIL_CLS_SMTP", smtplib.SMTP)
        app.config.setdefault("EMAIL_USE_STARTTLS", True)
        app.config.setdefault("EMAIL_SMTP_OPTIONS", {})
        
        app.teardown_appcontext(self.teardown)

    def send(self, **kwargs):
        """Send an email
        
        See `Red Mail's documentation <https://red-mail.readthedocs.io/en/latest/>`_ for more"""
        sender = self.sender
        return sender.send(**kwargs)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'redmail_sender'):
            # Pre v0.3.0 don't have contex management
            has_context = hasattr(ctx.redmail_sender, "close")
            if has_context and ctx.redmail_sender.is_alive:
                ctx.redmail_sender.close()

    @property
    def sender(self):
        "redmail.EmailSender: The sender object"
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'redmail_sender'):
                ctx.redmail_sender = self._create_sender()
                # Pre v0.3.0 don't have contex management
                has_context = hasattr(ctx.redmail_sender, "close")
                if has_context:
                    ctx.redmail_sender.connect()
            return ctx.redmail_sender

    def _create_sender(self) -> EmailSender:
        app_config = current_app.config
        email_sender = EmailSender(
            host=app_config['EMAIL_HOST'],
            port=app_config['EMAIL_PORT'],
            username=app_config["EMAIL_USERNAME"],
            password=app_config["EMAIL_PASSWORD"],

            cls_smtp=app_config["EMAIL_CLS_SMTP"],
            use_starttls=app_config["EMAIL_USE_STARTTLS"],
            **app_config["EMAIL_SMTP_OPTIONS"]
        )

        email_sender.sender = app_config.get('EMAIL_SENDER')

        email_sender.templates_html = current_app.jinja_env
        email_sender.templates_text = current_app.jinja_env

        for key, value in self.kws_sender.items():
            setattr(email_sender, key, value)

        return email_sender