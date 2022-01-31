
import pytest
from pathlib import Path
import os, sys

class DummySMTP:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_login = False

    def starttls(self):
        return

    def login(self, user=None, password=None):
        self.is_login = True
        return

    def send_message(self, msg):
        return

    def quit(self):
        return

@pytest.fixture()
def cls_dummy_smtp():
    return DummySMTP