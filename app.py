from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv('.env')
app = Flask(__name__)
app['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
db = SQLAlchemy(app)


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
