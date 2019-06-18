from flask import Flask, jsonify, render_template, request, url_for
from learn import *
import os
from werkzeug.utils import secure_filename
import json
import time
import requests

__author__ = 'animesh'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# app.config['CELERY_BROKER_URL'] = os.environ.get('amqp://localhost//')
# app.config['CELERY_RESULT_BACKEND'] = ''
# celery = make_celery(app)

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/training')
# def training():
# 	learn.apply_async(countdown=3)
# 	return jsonify({'data': 'tarining'})

# @celery.task(name='app.learn')
# def learn():
# 	f = TrainModel()
# 	k = f.train()
# 	f.withImage()
# 	f.saveModel()
# 	return 'Completed'


@app.route('/getEpoch')
def tragetEpochining():
    f = open("log.txt", "r")
    return f.read()


@app.route('/test')
def test():
    f = TrainModel()
    f.loadModel()
    pred = f.predictImage()
    return pred


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        target = os.path.join(APP_ROOT, 'images/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)

        classifier = TrainModel()
        classifier.loadModel()

        for file in request.files.getlist('file'):
            print(file)
            filename = time.strftime("%Y%m%d-%H%M%S") + file.filename
            destination = "".join([target, filename])
            print(destination)
            file.save(destination)

        result = classifier.predictImage(destination)
        conv_curr = getValue(1, "USD")
        par = "The NRP " + str(1) + " is " + \
            conv_curr['amnt'] + " " + conv_curr['BaseCurrency']
        return jsonify({'paragraph': par})
    return render_template('upload.html')


def getValue(num, cur):
    url = 'https://nrb.org.np/exportForexJSON.php'
    r = requests.get(url=url)
    data = r.json()
    conv_curr = {}
    for i in data['Conversion']['Currency']:
        if i['BaseCurrency'] == cur:
            amnt = float(i['TargetBuy']) / float(i['BaseValue'])
            print(amnt)
            conv_curr = i
            print(conv_curr)
            converted = str(1 / amnt * num)
            conv_curr['amnt'] = converted
    return conv_curr

if __name__ == '__main__':
    app.run(debug=True)
