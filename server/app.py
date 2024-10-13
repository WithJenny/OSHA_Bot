import os
from flask import Flask, jsonify, redirect
from twelvelabs import TwelveLabs
import cv2 as cv
import requests
import time
# from helpers import nod_yes, nod_no

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


@app.route('/start')
def start_robot():

    capture_duration = 10
    cap = cv.VideoCapture(0)
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
    query_list = [
        "person wearing glasses",
        # "person wearing bunny ears"
    ]

    for query in query_list:
        search_results = client.search.query(
            index_id=index_id,
            query_text=query,  # TODO update the query
            options=["visual"]
        )
        app.logger.info('=======================')
        app.logger.info(query)
        scores = [
          result.score for result in search_results.data if result.score > 65
        ]
        if len(scores) == 0:
            # TODO INSERT HEAD SHAKING FUNCTION HERE
            try:
                app.logger.info('nodding')
                # nod_no()
            except Exception as e:
                app.logger.error(f'cant nod, {e}')
                app.logger.error('cant shake')

            return jsonify(msg="Fail")
        app.logger.info(scores)
        app.logger.info('=======================')
        # TODO INSERT HEAD NODDING FUNCTION HERE
        try:
            # nod_yes()
            app.logger.info('nodding')
        except Exception as e:
            app.logger.error(f'cant nod, {e}')

    return jsonify(msg="Success")


if __name__ == '__main__':
    app.run(debug=True)
