import os
from flask import Flask, jsonify, redirect, render_template
from twelvelabs import TwelveLabs
import cv2 as cv
import requests
import time
from helpers import nod_yes, nod_no, thinking

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

    return render_template('index.html')


@app.route('/start')
def start_robot():
    try:
        nod_yes()
        app.logger.info('nodding')
    except Exception as e:
        app.logger.error(f'cant nod, {e}')

    capture_duration = 5
    cap = cv.VideoCapture(0)
    app.logger.info('=======================')
    app.logger.info('Video recording...')
    app.logger.info('=======================')

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)

    result = cv.VideoWriter(
        '../videos/filename.mp4',
        cv.VideoWriter_fourcc(*'mp4v'),
        10,
        size
    )
    start_time = time.time()
    while int(time.time() - start_time) < capture_duration:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        result.write(frame)
        if cv.waitKey(1) == ord('q'):
            break

        # return redirect here
    app.logger.info('=======================')
    app.logger.info('Video Captured... going to upload now')
    app.logger.info('=======================')
    try:
        thinking()
        time.sleep(2)
        app.logger.info('nodding')
    except Exception as e:
        app.logger.error(f'cant nod, {e}')

    return redirect('/upload-video')


@app.route('/index')
def get_index():

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }

    response = requests.get(f"{BASE_URL}/indexes/{index_id}", headers=headers)

    return jsonify(response.json())


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

    return jsonify(data)


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


@app.route('/upload-video')
def handle_upload_video():
    """Upload video to twelvelabs index."""
    task = client.task.create(
        index_id=index_id,
        file='../videos/filename.mp4',
    )

    app.logger.info(f"Task id={task.id}")
    task.wait_for_done(sleep_interval=5)

    return redirect('/query')


@app.route('/query')
def handle_check():
    query_text = "face wearing a fask mask"

    search_results = client.search.query(
        index_id=index_id,
        query_text=query_text,
        options=["visual"]
    )

    app.logger.info('=======================')

    scores = [
      result.score for result in search_results.data if result.score > 80
    ]
    app.logger.info(query_text)
    app.logger.info(scores)
    app.logger.info('=======================')

    if len(scores) == 0:
        # TODO INSERT HEAD SHAKING FUNCTION HERE
        try:
            app.logger.info('nodding no')
            nod_no()
        except Exception as e:
            app.logger.error(f'cant nod, {e}')
            app.logger.error('cant shake')

        app.logger.info('=======================')

        return jsonify(msg="Fail")

    try:
        nod_yes()
        app.logger.info('nodding yes')
    except Exception as e:
        app.logger.error(f'cant nod, {e}')

    return jsonify(msg="Success")


if __name__ == '__main__':
    app.run(debug=True)
