.. _cookbook:

Cookbook
========

The basic use of Flask Red Mail was introduced in 
:ref:`tutorial`. This section covers some typical
use cases of the extension.


Verification Email
------------------

Pre-requisites:

- Basic undrestanding of Flask and Jinja templates
- JWT

First, we create a verification email template
``templates/email/verify.html``:

.. code-block:: console

    <h1>Hi,</h1>
    <p>
        in order to use our services, please click the link below:
        <br>
        <a href={{ url_for('verify_email', token=token, _external=True) }}>verify email</a>
    </p>
    <p>If you did not create an account, you may ignore this message.</p>

Next, we will create a route that creates

.. code-block:: python

    from flask import Flask, render_template, request
    from flask_redmail import RedMail
    import jwt

    app = Flask(__name__)
    email = RedMail(app)

    ...

    @app.route("/create-user", methods=["GET", "POST"])
    def create_user():
        if request.method == "GET":
            return render_template("create_user.html")
        elif request.method == "POST":
            form = request.form.to_dict()

            ... # Validate the form and the user doesn't exists

            email_address = form["email_address"]
            password = form["password"]
            token = jwt.encode(
                {
                    "email_address": email_address,
                    "password": password,
                }, current_app.config["SECRET_KEY"]
            )
            email.send(
                subject="Verify email",
                receivers=email_address,
                html_template="email/verify.html",
                body_params={
                    "token": token
                }
            )
            return render_template("verify_email.html")

Note that you also need to create ``create_user.html`` 
and ``verify_email.html`` templates. It may also help 
to use `Flask-WTF <https://flask-wtf.readthedocs.io/>`_.

Next, we will create a route to finalize the creation 
of the user when the user has verified the email:

.. code-block:: python

    @app.route("/verify-email/<token>")
    def verify_email(token):
        data = jwt.decode(token, current_app.config["SECRET_KEY"])
        email_address = data["email_address"]
        password = data["password"]
        ... # Create the user

.. note::

    You may also pass other information using the secure tokens.
    Alternatively, you may also actually create the user in the 
    route ``create_user`` and set, for example, a column 
    ``verified_email`` to False until the user has visited 
    ``verify_email`` route.