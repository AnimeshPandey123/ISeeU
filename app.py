from flask import Flask, jsonify, render_template
from check_celery import make_celery
from learn import *
import os

import json

app = Flask(__name__)

# app.config['CELERY_BROKER_URL'] = os.environ.get('amqp://localhost//')
# app.config['CELERY_RESULT_BACKEND'] = ''

# celery = make_celery(app)

stores = [
	{
		'name':'My Wonderful Store',
		'items': [
			{
				'name': 'My Item',
				'price': 15.99
			}
		]
	},
	{
		'name':'asd',
		'items': [
			{
				'name': 'sss',
				'price': 15.99
			}
		]
	}
]

# @app.route('/process/<name>')
# def process(name):
# 	reverse.apply_async(args=[name], countdown=3)
# 	return 'I sent an async request!'

# @celery.task(name='app.reverse')
# def reverse(string):
# 	f = open("mytext.txt", "a")
# 	f.write(string[::-1])
# 	f.close()
# 	return string[::-1]

@app.route('/')
def home():
	f = open("mytext.txt", "a")
	f.write("Now the file has more content!")
	f.close()
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
	f =  TrainModel()
	f.loadModel()
	pred = f.predictImage()
	return pred


# # POST /store data: {name:}
# @app.route('/store', methods=['POST'])
# def create_store():
# 	request_data = request.get_json()
# 	new_store = {
# 		'name': request_data['name'],
# 		'items': []
# 	}
# 	stores.append(new_store)
# 	return jsonify(new_store)

# @app.route('/store/<string:name>')
# def get_store(name):
# 	# Iterate over stores
# 	for i in stores:
# 		if i['name'] == name:
# 			return jsonify({'item':i});

# 	return jsonify({'error': 'Not Found'});

# @app.route('/store/')
# def get_stores():
# 	return jsonify({'stores': stores})

# @app.route('/store/<string:name>/item', methods=['POST'])
# def create_item_in_store(name):
# 	request_data = request.get_json()
# 	new_item = {
# 		'name': request_data['name'],
# 		'price': request_data['price']
# 	}
# 	for i in stores:
# 		if i['name'] == name:
# 			i['items'].append(new_item)
# 			return jsonify({'items': i});
# 	return jsonify({'error': 'Not Found'});

# @app.route('/store/<string:name>/item', methods=['GET'])
# def get_items_in_store(name):
# 	for i in stores:
# 		if i['name'] == name:
# 			return jsonify({'items':i['items']});
# 	return jsonify({'error': 'Not Found'});

if __name__ == '__main__':
	app.run()
