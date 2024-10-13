import os

from flask import Flask
from twelvelabs import TwelveLabs

app = Flask(__name__)
API_KEY = os.environ['TWELVE_LABS_API_KEY']

client = TwelveLabs(api_key=API_KEY)

@app.route('/')
def showHomePage():

    return """
        This is a temporary home page, we'll be using this as an api, but for now it is a placeholder
    """


@app.route('/start')
def startRobotHandler():
    """Start robot and authenticate with TwelveLabs."""
    # TODO start robot

    return """
        robot started to record
    """
