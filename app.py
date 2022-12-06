from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_cors import CORS
from flask_minify import Minify, decorators as minify_decorators
import os, pymongo, json

# Initialize Flask Components
app = Flask(__name__)
CORS(app)
Minify(app=app, passive=True)

# MongoDB connection
client = pymongo.MongoClient(os.environ.get('MONGO_CONN', ''))
db = client['cookiebanner']
collection = db['domain']

# Blueprints
getBanner = Blueprint('getBanner', __name__, url_prefix='/get/<id>')
createBanner = Blueprint('createBanner', __name__, url_prefix='/create/<id>')
testBanner = Blueprint('testBanner', __name__, url_prefix='/test')
previewBanner = Blueprint('previewBanner', __name__, url_prefix='/preview/<id>')
app.register_blueprint(getBanner)
app.register_blueprint(createBanner)
app.register_blueprint(testBanner)
app.register_blueprint(previewBanner)

# Routes 
@app.route('/get/<id>', methods=['GET'])
def view(id):
    banner = collection.find_one({'_id': id})['banner']
    if banner: return banner
    else: return 'Invalid ID'


@app.route('/create/<id>', methods=['GET', 'POST'])
@minify_decorators.minify(html=True, js=True, cssless=True)
def create(id):
    data = request.get_json()
    template = render_template('fullbanner_custom.html', d=data)
    collection.update_one({'_id': id}, {'$set': { 'id': id, 'banner': template, 'data': data}}, upsert=True)
    return f'Success'


@app.route('/test', methods=['GET'])
def test():
    data = json.load(open('customization.json'))
    return render_template('fullbanner_custom.html', d=data)


@app.route('/preview/<id>', methods=['GET'])
def preview(id):
    data = request.get_json()
    return render_template('fullbanner_custom.html', d=data)


if __name__ == '__main__':
    app.run(debug=True)