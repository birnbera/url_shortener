#!/usr/bin/python3
"""URL web application"""

import base62
from urllib.parse import urlparse
from datetime import datetime
from flask import Flask, request, redirect, render_template, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name___)
CORS(app, resources="/*", origins="0.0.0.0")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://flask:f1ask@localhost/url_db'
db = SQLAlchemy(app)

class Url(db.Model):
    short = db.Column(db.String(256), primary_key=True)
    original = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __repr__(self):
        return '<Short URL: {}\nActual URL: {}>'.format(self.short,
                self.actual)

db.create_all()

#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('web_static/404.html'), 404

@app.route('/', strict_slashes=False, methods=['GET', 'POST'])
def add_url():
    """ validates url and returns shortend url """
    if request.method == 'POST':
        originalUrl = request.form.get('ogUrl')
        if urlparse(originalUrl).scheme == '':
            originalUrl = 'http://' + originalUrl

        shortUrl = base62.encode(originalUrl)

        newurl = Url(short=shortUrl, original=originalUrl)
        db.session.add(newurl)
        db.session.commit()

        return jsonify({'shortUrl': shortUrl}), 201
    return render_template('web_static/index.html'), 200

@app.route('/<url>', strict_slashes=False)
def uri_handle(url):
    """servers actual webpage based on url"""
    shortUrl = base62.decode(url)
    originalUrl = Url.query.filter_by(short=shortUrl).first()
    if originalUrl is None:
        abort(404)
    return redirect(originalUrl)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
