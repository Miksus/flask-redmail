
.. meta::
   :description: Red Mail is an advanced email sender for Python. It is open source and well tested.
   :keywords: send, email, Python, Flask

Flask :red:`Red` Mail: Email sending for Flask
===================================================

Red Mail is an advanced Python library for sending emails. 

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

    app.config["SMTP_HOST"] = "localhost"
    app.config["SMTP_PORT"] = 0

    app.config["SMTP_SENDER"] = "no-reply@example.com"

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


Indices and tables
==================

* :ref:`genindex`
