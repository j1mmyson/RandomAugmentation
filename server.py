import os
from flask import Flask, request, send_file, redirect, render_template, make_response
import imgaug.augmenters as iaa
from copy import deepcopy
import PIL
from PIL import Image
import numpy as np
from numpy import asarray
import zipfile
import io
from queue import Queue, Empty
import time
import threading


UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__, template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024*5

requests_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1


def handle_requests_by_batch():
    while True:
        requests_batch = []
        while not (len(requests_batch) >= BATCH_SIZE):
            try:
                requests_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue
            batch_outputs = []
            for request in requests_batch:
                batch_outputs.append(run(request['input'][0], request['input'][1]))

            for request, output in zip(requests_batch, batch_outputs):
                request['output'] = output


threading.Thread(target=handle_requests_by_batch).start()


def run(files, number):
    folder = 0
    zip_object = io.BytesIO()
    with zipfile.ZipFile(zip_object, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            folder = folder + 1
            image = Image.open(file).convert('RGB')
            result = list()
            images = asarray(image)
            for _ in range(number):
                temp = deepcopy(iaa.Sometimes(1, iaa.RandAugment(n=2, m=9))(image=images))
                temp = Image.fromarray(temp, 'RGB')
                result.append(temp)
                i = 0
                for img in result:
                    buf = io.BytesIO()
                    img.save(buf, 'jpeg')
                    img_name = str(folder) + "/aug_{:02d}.jpeg".format(i)
                    i = i + 1
                    print("Writing image {:s} in the archive".format(img_name))
                    zf.writestr(img_name, buf.getvalue())
    zip_object.seek(0)
    # img = base64.b64encode(img_io.getvalue())

    return zip_object.getvalue()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Web server

@app.route('/augment', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print('no file')
        return redirect(request.url)

    try:
        number = int(request.form['number'])
    except:
        return render_template('index.html', result = 'number must be integer'), 400
    
    number = int(request.form['number'])
    files = request.files.getlist('file')

    try:
        for f in files:
            PIL.Image.open(f).convert("RGB")
    except Exception:
        return render_template('index.html', result = 'Import image please'), 400

    if files[0].filename == '':
        print('no filename')
        return redirect(request.url)

    # stateless image
    if requests_queue.qsize() >= BATCH_SIZE:
        return render_template('index.html', result = 'TooMany requests try again'), 429

    req = {
        'input': [files, number]
    }
    requests_queue.put(req)

    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    byte_io = io.BytesIO(req['output'])
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='aug.zip', as_attachment=True)



@app.route('/healthz', methods=['GET'])
def checkHealth():
	return "Pong",200


@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('index.html', result = 'The image size is too large'), 413


if __name__ == '__main__':
    app.run(debug=False, port=8000, host='0.0.0.0')
