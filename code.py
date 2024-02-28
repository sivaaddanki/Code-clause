from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import shortuuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.String(22), primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clicks = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url']
    short_url = shortuuid.uuid()[:8]

    new_url = URL(id=short_url, original_url=original_url)
    db.session.add(new_url)
    db.session.commit()

    return render_template('shorten.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_original(short_url):
    url_entry = URL.query.filter_by(id=short_url).first_or_404()
    url_entry.clicks += 1
    db.session.commit()
    return redirect(url_entry.original_url)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
