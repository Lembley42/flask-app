from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_minify import Minify, decorators as minify_decorators
import os, pymongo

app = Flask(__name__)
CORS(app)

mongo_username = os.environ.get('MONGO_USER', '')
mongo_pw = os.environ.get('MONGO_PW', '')

client = pymongo.MongoClient(f'mongodb+srv://{mongo_username}:{mongo_pw}@webscraper.73l0qzo.mongodb.net/?retryWrites=true&w=majority')
db = client['cookiebanner']
collection = db['domain']

bp = Blueprint('fullbanner', __name__, url_prefix='/cms/<id>')
createBanner = Blueprint('createBanner', __name__, url_prefix='/create/<id>')

app.register_blueprint(bp)
app.register_blueprint(createBanner)


@app.route('/cms/<id>', methods=['GET'])
def view(id):
    banner = collection.find_one({'_id': id})
    if banner: return banner
    else: return 'Invalid ID'


@app.route('/create/<id>', methods=['GET', 'POST'])
def create(id):
    # get json data from request
    data = request.get_json()

    template = render_template('fullbanner_custom.html', data=data)
    collection.insert_one({'_id': id, 'banner': template})
    print(f'Created banner {id}')
    return f'Sucessfully created the template and stored it with Id {id}'