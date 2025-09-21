from flask import Flask, request, jsonify, render_template
from passlib.hash import sha256_crypt
from sqlmodel import Field, SQLModel, create_engine, Relationship, Session, select
from typing import List, Optional
from dotenv import load_dotenv
from datetime import datetime, timezone
import os

load_dotenv('.env')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
db = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))

class Admin(SQLModel, table=True):
    admin_id: int = Field(default=None, primary_key=True)
    username: str = Field()
    password: str = Field(max_length=150)
    last_active: datetime = Field(default=datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    glossary_terms: List['Glossary'] = Relationship(back_populates="admin")

class Glossary(SQLModel, table=True):
    glossary_id: int = Field(default=None, primary_key=True)
    term: str = Field()
    definition: str  = Field()
    initial: str = Field(index=True)
    date_added: datetime = Field(default_factory=datetime.now(timezone.utc))
    admin_id: Optional[int] = Field(default=None, foreign_key='admin.admin_id')
    admin: Optional[Admin] = Relationship(back_populates="glossary_terms")

    def get_all_terms():
         with Session(db) as session:
             return session.exec(select(Glossary)).all()

    def search_by_letter(letter):
        with Session(db) as session:
            statement = select(Glossary).where(Glossary.initial == letter)
            return session.exec(statement).all()

    def glossary_menu():
        with Session(db) as session:
            return session.exec(
                select(Glossary)
                .distinct(Glossary.initial)
                .group_by(Glossary.initial)
            ).all()


class Subscriber(SQLModel, table=True):
    subscriber_id: int = Field(default=None, primary_key=True)
    email: str = Field()
    status: str = Field(default='active')
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))


@app.route('/')
def glossary_directory():
   glossary_results = Glossary.get_all_terms()
   menu = Glossary.glossary_menu()
   glossary = [glossary.model_dump() for glossary in glossary_results]
   return render_template('index.html', glossary_terms=glossary, glossary_menu=menu)

@app.route('/<alphabet>')
def glossary_search(alphabet):
    terms = Glossary.search_by_letter(alphabet)
    return render_template('', glossary_terms=terms)

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
