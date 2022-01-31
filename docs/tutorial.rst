.. _tutorial:

Tutorial
========

This section covers basic tutorials of 
Flask Red Mail. It is advised to consult
`Red Mail's documentation <https://red-mail.readthedocs.io/en/latest/>`_
for more advanced use of sending emails.

initiation
----------

To initiate Flask Red Mail, simply:

.. code-block:: python

    from flask import Flask
    from flask_redmail import RedMail

    app = Flask(__name__)
    email = RedMail(app)

In case you prefer lazy initiation, you may 
also use ``init_app`` method:

.. code-block:: python

    from flask import Flask
    from flask_redmail import RedMail

    app = Flask(__name__)
    email = RedMail()
    email.init_app(app)

Configuration
-------------

Flask Red Mail reads the configurations
from the ``app.config``. You may pass 
these simply:

.. code-block:: python

    app.config["EMAIL_HOST"] = "<SMTP HOST>"
    app.config["EMAIL_PORT"] = 587
    app.config["EMAIL_USER"] = "me@example.com"
    app.config["EMAIL_PASSWORD"] = "<PASSWORD>"

    # Set default sender
    app.config["EMAIL_SENDER"] = "no-reply@example.com"

Note that you don't have to specify ``EMAIL_USER`` and
``EMAIL_PASSWORD`` if your SMTP server does not require
those.

Full list of configurations:

================== =============== ============================================
Configuration      Optional        Description
================== =============== ============================================
**EMAIL_HOST**     No              Host address of the SMTP server.
**EMAIL_PORT**     No              Port of the SMTP server. Often 587.
**EMAIL_USER**     Yes             User to authenticate to the SMTP server.
**EMAIL_PASSWORD** Yes             Password to authenticate to the SMTP server.
**EMAIL_SENDER**   Yes             Default sender address for emails.
================== =============== ============================================


Sending Emails
--------------

After configuring, you may send emails simply using the
``send`` method:

.. code-block:: python

    @app.route("/send-email")
    def send_email():
        email.send(
            subject="An example",
            receivers=["you@example.com"],
            html="""
                <h1>Hi,</h1>
                <p>This is an example message</p>
            """
        )

Method ```RedMail.send`` is simply a wrapper of the 
method ``redmail.EmailSender.send``. Please read more
`Red Mail's documentation <https://red-mail.readthedocs.io/en/latest/>`_.

.. note::

    You may also create HTML body templates to the ``template/``
    folder (or where you store your HTML Jinja templates) and 
    pass the relative path of the template as ``html_template``
    argument.

Defaults
--------

In some cases it may be useful to create several instances of ``RedMail``
for various purposes and set default subjects, receivers, senders, bodies etc.:

.. code-block:: python

    newsletter = RedMail(
        subject="News letter",
        sender="news@example.com",
        html_template="email/news.html"
    )

    @app.route("/send-news")
    def send_news():
        newsletter.send(
            receivers=["you@example.com"]
        )

The keyword arguments passed to :class:`.RedMail` are set as attributes to 
``redmail.EmailSender`` when creating the sender. These are stored as a dict in attribute 
``kws_sender`` in RedMail instance. 
Please read more from `Red Mail's documentation <https://red-mail.readthedocs.io/>`_.

Note that the default values passed to initiation of ``RedMail`` overrides the 
configurations from ``app.config`` and the arguments passed to ``email.send``
overrides both ``app.config`` and ``email.kws_sender``.

What's Next?
------------

See more examples from :ref:`cookbook`.