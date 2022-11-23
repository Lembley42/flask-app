from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_minify import Minify, decorators as minify_decorators


app = Flask(__name__)
CORS(app)

bp = Blueprint('fullbanner', __name__, url_prefix='/cms/<id>')
app.register_blueprint(bp)

@app.route('/cms/<id>', methods=['GET'])
@minify_decorators.minify(html=True, js=True, cssless=True)
def view(id):
    if id == '1': 
        return render_template('fullbanner_1.html')
    elif id == '2':
        return render_template('fullbanner_2.html')

if __name__ == '__main__':
    app.run(debug=True)


