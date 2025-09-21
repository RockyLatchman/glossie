from flask import Flask, request, jsonify, render_template
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from dotenv import load_dotenv
from datetime import datetime, timezone
import os

load_dotenv('.env')
app = Flask(__name__)
app['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
db = SQLAlchemy(app)


class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    last_active = db.Column(db.DateTime(datetime.now(timezone.utc)))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    glossary_terms = db.relationship('Glossary', backref="admin", lazy=True)

class Glossary(db.Model):
    glossary_id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String, nullable=False)
    definition = db.Column(db.Text, nullable=False)
    acronym = db.Column(db.String)
    date_added = db.Column(db.DateTime(datetime.now(timezone.utc)))
    admin_id = db.Column(db.Integer, ForeignKey('admin.admin_id'), nullable=False)

class Subscribers(db.Model):
    pass




@app.route('/')
def index():
    pass

@app.route('/<alphabet>')
def glossary_search():
    pass

@app.route('/about')
def about():
    pass

@app.route('/contact')
def contact():
    pass

@app.route('/subscribe')
def email_subscription():
    pass

@app.route('/documentation')
def documentation():
    pass

@app.route('/api/list/all')
def glossary_terms():
    pass

@app.route('/api/random-term')
def random_term():
    pass

@app.route('/api/search/term/<id>')
def search_term():
    pass

@app.route('/dashboard/sign-in')
def signin():
    pass

@app.route('/dashboard/sign-out')
def signout():
    pass

@app.route('/dashboard')
def dashboard():
    pass

@app.route('/dashboard/add-entry')
def add_entry():
    pass

@app.route('/dashboard/edit/entry/<entry_id>')
def edit_entry():
    pass

@app.route('/dashboard/delete/entry/<entry_id>')
def delete_entry():
    pass

@app.route('/dashboard/view/entry/<entry_id>')
def view_entry():
    pass

@app.route('/dashboard/subscribers')
def view_subscribers():
    pass

@app.route('/dashboard/subscriber/')
def subscriber():
    #delete or view subscriber
    pass





if __name__ == '__main__':
    app.run(debug=True)
