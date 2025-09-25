from flask import Flask, request, jsonify, render_template, g, url_for, redirect
from passlib.hash import sha256_crypt
from sqlmodel import Field, SQLModel, create_engine, Relationship, Session, select
from sqlalchemy import func
from typing import List, Optional
from dotenv import load_dotenv
from datetime import datetime, timezone
import os
import json
import random

load_dotenv('.env')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
db = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))

quote_machine = [
    {
      'quote' : 'Fear is ugly because it makes you irrational. Fear makes you jump to conclusions. Fear makes you reactionary.',
      'author' : 'DHH'
    },
    {
      'quote' : 'SPAM SPAM..such a great song',
      'author' : 'Guido Van Rossum'
    },
    {
      'quote' : 'When you don’t create things, you become defined by your tastes rather than ability. Your tastes only narrow and exclude people. so create',
      'author' : '_why'
    }
]

class Utilities:
    def date_filter(value, format='%b, %d %Y'):
        if isinstance(value, datetime):
            return value.strftime(format)
        return value

class Admin(SQLModel, table=True):
    admin_id: int = Field(default=None, primary_key=True)
    username: str = Field()
    password: str = Field(max_length=150)
    last_active: datetime = Field(default=datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    glossary_terms: List['Glossary'] = Relationship(back_populates="admin")
    quotes: List['Quote'] = Relationship(back_populates="admin")

class Glossary(SQLModel, table=True):
    glossary_id: int = Field(default=None, primary_key=True)
    term: str = Field()
    definition: str  = Field()
    initial: str = Field(index=True)
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), exclude=True)
    admin_id: Optional[int] = Field(default=1, foreign_key='admin.admin_id', exclude=True)
    admin: Optional[Admin] = Relationship(back_populates="glossary_terms")

    def add_entry(entry):
        with Session(db) as session:
            session.add(entry)
            session.commit()

    def get_all_terms():
         with Session(db) as session:
             return session.exec(select(Glossary)).all()

    def glossary_limit(glossary_count):
        with Session(db) as session:
           return session.exec(select(Glossary).limit(glossary_count)).all()

    def random_entry():
        glossary = Glossary.get_all_terms()
        return random.choice([
            glossary_item.model_dump(exclude={'glossary_id'}) for glossary_item in glossary
        ])

    def search(column, term):
        with Session(db) as session:
            statement = ''
            if column == 'term':
               statement = select(Glossary).where(func.upper(Glossary.term) == term)
            elif column == 'initial':
               statement = select(Glossary).where(Glossary.initial == term)
            return session.exec(statement).all()

    def glossary_menu():
        with Session(db) as session:
            return session.exec(
                select(Glossary)
                .distinct(Glossary.initial)
                .group_by(Glossary.initial)
            ).all()


class Subscriber(SQLModel, table=True):
    __tablename__ = 'subscribers'
    subscriber_id: int = Field(default=None, primary_key=True)
    email: str = Field()
    status: str = Field(default='active')
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def save(subscriber):
        with Session(db) as session:
           session.add(subscriber)
           session.commit()
           session.close()

    def retrieve_subscribers():
        with Session(db) as session:
            return session.exec(select(Subscriber)).all()

    @classmethod
    def remove_subscriber(cls, subscriber_id):
        with Session(db) as session:
            statement = select(Subscriber).where(Subscriber.subscriber_id == subscriber_id)
            subscriber = session.exec(statement).first()
            session.delete(subscriber)
            session.commit()

    @classmethod
    def subscriber_count(cls):
        with Session(db) as session:
            return session.exec(select(func.count()).select_from(Subscriber)).one()

class Quote(SQLModel, table=True):
    __tablename__ = 'quotes'
    quote_id: int = Field(default=None, primary_key=True)
    author: str = Field()
    quote: str = Field()
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    admin_id: Optional[int] = Field(default=1, foreign_key='admin.admin_id', exclude=True)
    admin: Optional[Admin] = Relationship(back_populates="quotes")

    @classmethod
    def add(cls, quotes):
        with Session(db) as session:
            session.add(quotes)
            session.commit()


@app.before_request
def glossary_menu():
    g.menu = Glossary.glossary_menu()

@app.route('/')
def glossary_directory():
   glossary_results = Glossary.get_all_terms()
   glossary = [glossary.model_dump() for glossary in glossary_results]
   return render_template(
       'index.html',
       glossary_terms=glossary,
       glossary_menu=g.menu
   )

@app.route('/<letter>')
def glossary_search(letter):
    terms = Glossary.search('initial', letter.upper())
    return render_template(
        'tautogram.html',
        glossary_terms=terms,
        letter=letter.upper(),
        glossary_menu=g.menu
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        random_quote=random.choice(quote_machine),
        glossary_menu=g.menu
    )

@app.route('/contact')
def contact():
    pass

@app.route('/subscribe', methods=['POST'])
def email_subscription():
    referrer_url = request.referrer
    if request.method == 'POST':
        form_email = request.form.get('subscriber', 'Invalid e-mail')
        if form_email != 'Invalid e-mail':
            subscriber = Subscriber(email=form_email)
            Subscriber.save(subscriber)
        if referrer_url:
            return redirect(referrer_url)

@app.route('/documentation')
def documentation():
    return render_template('documentation.html',glossary_menu=g.menu)

@app.route('/api/list/all')
def glossary_terms():
    glossary_terms = Glossary.get_all_terms()
    return jsonify({
        'message' : [glossary.model_dump(exclude={'glossary_id'}) for glossary in glossary_terms],
        'status' : 200
    })

@app.route('/api/list/limit/<count>')
def glossary_entry_count(count):
    glossary_limit = Glossary.glossary_limit(count)
    return [glossary.model_dump(exclude={'glossary_id'}) for glossary in glossary_limit]

@app.route('/api/random-term')
def random_term():
    random_entry = Glossary.random_entry()
    return jsonify({'message' : random_entry, 'status' : 200})

@app.route('/api/search/<term>')
def search_term(term):
    search_result = Glossary.search('term', term.upper())
    return jsonify({
        'message' :  [search.model_dump(exclude={'glossary_id'}) for search in search_result],
        'status' : 200
    })

@app.route('/dashboard/sign-in')
def signin():
    return render_template('signin.html')

@app.route('/dashboard/sign-out')
def signout():
    pass

@app.route('/dashboard')
def dashboard():
    glossary_results = Glossary.get_all_terms()
    subscribed = Subscriber.retrieve_subscribers()
    app.jinja_env.filters['format_date'] = Utilities.date_filter
    return render_template(
        'dashboard.html',
        glossary_terms=[glossary.model_dump() for glossary in glossary_results],
        subscribers = [subscriber.model_dump() for subscriber in subscribed],
        subscriber_count = Subscriber.subscriber_count()
    )

@app.route('/dashboard/add-entry', methods=['POST'])
def add_entry():
    if request.method == 'POST':
        glossary_entry = Glossary(
            term=request.form.get('term'),
            definition=request.form.get('definition'),
            initial=request.form.get('term')[0].upper()
        )
        glossary_item = Glossary.add_entry(glossary_entry)
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html')

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

@app.route('/dashboard/subscriber/<subscriber_id>', methods=['POST'])
def subscriber(subscriber_id):
    if request.method == 'POST':
       Subscriber.remove_subscriber(subscriber_id)
       subscribed = Subscriber.retrieve_subscribers()
       subscribers = [subscriber.model_dump() for subscriber in subscribed]
       return subscribers

@app.route('/dashboard/add-quote', methods=['POST'])
def add_quotes():
    if request.method == 'POST':
        quote = Quote(
            author = request.form.get('author'),
            quote = request.form.get('quote')
        )
        Quote.add(quote)
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
