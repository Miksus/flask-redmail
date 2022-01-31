
# Flask Red Mail: Email Sending for Flask
> Flask extension for Red Mail

---

[![Pypi version](https://badgen.net/pypi/v/flask_redmail)](https://pypi.org/project/flask_redmail/)
[![build](https://github.com/Miksus/flask-redmail/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Miksus/flask-redmail/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Miksus/flask-redmail/branch/master/graph/badge.svg?token=IMR1CQT9PY)](https://codecov.io/gh/Miksus/flask-redmail)
[![Documentation Status](https://readthedocs.org/projects/flask-redmail/badge/?version=latest)](https://red-mail.readthedocs.io/en/latest/)
[![PyPI pyversions](https://badgen.net/pypi/python/flask-redmail)](https://pypi.org/project/flask-redmail/)

## What is it?
Flask Red Mail is a Flask extension for [Red Mail](https://github.com/Miksus/red-mail).
Red Mail is a powerful email sender library capable of including
attachments from various formats, embedding images, parametrization
with Jinja etc. This library harness the power of Red Mail in order to 
make it trivial to:

- Send verification emails to users
- Create email based *forgot password* functionality
- Create Flask based email news letters
- Handle other needs for sending emails from a web application

Links:

- [Flask-Redmail's source code](https://github.com/Miksus/flask-redmail)
- [Flask-Redmail's documentation](https://flask-redmail.readthedocs.io/)
- [Flask-Redmail's releases (PyPI)](https://pypi.org/project/Flask-Redmail/)
- [Red Mail's source code](https://github.com/Miksus/red-mail)
- [Red Mail's documentation](https://red-mail.readthedocs.io/)
- [Red Mail's releases (PyPI)](https://pypi.org/project/redmail/)

## Installation

Install the extension from PyPI:

```console
pip install flask-redmail
```

## Example

Create a simple Flask application:

```python
import flask
from flask_redmail import RedMail

app = flask.Flask(__name__)
email = RedMail(app)

# Configure
app.config["EMAIL_HOST"] = "localhost"
app.config["EMAIL_PORT"] = 0

# Optional
app.config["EMAIL_USER"] = "me@example.com"
app.config["EMAIL_PASSWORD"] = "<PASSWORD>"
app.config["EMAIL_SENDER"] = "no-reply@example.com"
```

Use the extension:

```python
@app.route("/send")
def send_email():
    email.send(
        subject="An example",
        receivers=["you@example.com"],
        html="<h1>An example email.</h1>"
    )
```

---

## Author

* **Mikael Koli** - [Miksus](https://github.com/Miksus) - koli.mikael@gmail.com

