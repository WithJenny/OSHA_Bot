import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def showHomePage():

    return """
        This is a temporary home page, we'll be using this as an api, but for now it is a placeholder
    """
