from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_minify import Minify, decorators as minify_decorators
import redis, os

app = Flask(__name__)
CORS(app)

redis_host = os.environ.get('REDIS_HOST', '')
redis_port = os.environ.get('REDIS_PORT', '')
redis_pw = os.environ.get('REDIS_PW', '')

redis_db = redis.StrictRedis(host=redis_host, port=int(redis_host), password=redis_pw, ssl=True)
redis_db.ping()

bp = Blueprint('fullbanner', __name__, url_prefix='/cms/<id>')
create = Blueprint('create', __name__, url_prefix='/create/<id>')


app.register_blueprint(bp)
app.register_blueprint(create)


@app.route('/cms/<id>', methods=['GET'])
def view(id):
    return redis_db.get(id)


@app.route('/create/<id>', methods=['GET'])
def create(id):
    headline = request.args.get('headline')

    template = render_template('fullbanner_custom.html', headline=headline)
    redis_db.set(id, template)
    print(f'Created banner {id} with headline {headline}')
    return f'Sucessfully created the template and stored it with Id {id}'


if __name__ == '__main__':
    app.run()

