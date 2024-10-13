import os

from flask import Flask
import requests
from twelvelabs import TwelveLabs
# from twelvelabs.models.task import Task

app = Flask(__name__)

API_KEY = os.environ['TWELVE_LABS_API_KEY']

BASE_URL = (
    os.environ['TWELVE_LABS_BASE_URL'] +
    os.environ['TWELVE_LABS_VERSION']
)

client = TwelveLabs(API_KEY)
index_id = os.environ['INDEX_ID']


@app.route('/')
def show_homepage():

    return """
        <h1>OSHA_BOT<h1>
        <p>
            This is a temporary home page, we'll be using this as an api,
            but for now it is a placeholder
        <p>
        <a href="http://localhost:5000/indexes">List Indexes</a>
    """


@app.route('/indexes')
def list_indexes():

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }

    response = requests.get(f"{BASE_URL}/indexes", headers=headers)
    data = (response.json())['data']
    app.logger.info('=======================')
    for index in data:
        app.logger.info(f"Index id={index['_id']}, name={index['index_name']}")
        app.logger.info('=======================')

    return response.text


@app.route('/index')
def get_index():

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }

    response = requests.get(f"{BASE_URL}/indexes/{index_id}", headers=headers)

    return response.text


@app.route("/video/<video_id>")
def get_video(video_id):

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }

    response = requests.get(
        f"{BASE_URL}/indexes/videos/{video_id}",
        headers=headers,
    )

    return response.text

@app.route('/upload-video/<video_file>')
def handle_upload_video(video_file):

    task = client.task.create(
        index_id=index_id,
        file=video_file,
    )
    app.logger.info(f"Task id={task.id}")

    return """
        robot started to record
    """


if __name__ == '__main__':
    app.run(debug=True)
