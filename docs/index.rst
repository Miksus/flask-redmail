
.. meta::
   :description: Red Mail is an advanced email sender for Python. It is open source and well tested.
   :keywords: send, email, Python, Flask

Flask Red Mail: Email sending for Flask
===================================================

Flask Red Mail is a Flask extension for Red Mail.
Red Mail is a powerful email sending library which 
makes sending emails with attachments, embedded images
or templated HTML easy.

It makes easy to:

- Send verification emails to users
- Create email based *forgot password* functionality
- Create Flask based email news letters

Links:

- `Flask-Redmail's source code <https://github.com/Miksus/flask-redmail>`_
- `Flask-Redmail's documentation <https://flask-redmail.readthedocs.io/>`_
- `Flask-Redmail's releases (PyPI) <https://pypi.org/project/Flask-Redmail/>`_
- `Red Mail's source code <https://github.com/Miksus/red-mail>`_
- `Red Mail's documentation <https://red-mail.readthedocs.io/>`_
- `Red Mail's releases (PyPI) <https://pypi.org/project/redmail/>`_

Installation
------------

Install the package:

.. code-block:: console

    pip install flask-redmail


Example
-------

.. code-block:: python

    from flask import Flask
    from flask_redmail import RedMail

    app = Flask(__name__)
    email = RedMail(app)

Then set configurations:

.. code-block:: python

    app.config["EMAIL_HOST"] = "localhost"
    app.config["EMAIL_PORT"] = 0

    app.config["EMAIL_SENDER"] = "no-reply@example.com"

Then you may send emails:

.. code-block:: python

    @app.route("/send-email")
    def send_email():
        email.send(
            subject="Verify email",
            receivers=["you@example.com"],
            html="""
                <h1>Hi,</h1>
                <p>
                    this is an example.
                </p>
            """
        )

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorial
   cookbook

Indices and tables
==================

* :ref:`genindex`
