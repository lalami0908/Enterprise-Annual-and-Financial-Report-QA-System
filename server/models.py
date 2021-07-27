# models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from server import db

#db = SQLAlchemy()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp/test.db"

# db = SQLAlchemy(app)
app = Flask(__name__)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(10), unique=False, nullable=False)
    records = db.relationship('Record', backref="user", lazy=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email)


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True, nullable=False)
    short_name = db.Column(db.String(10), nullable=False)
    full_name = db.Column(db.String(20), nullable=True)
    english_short = db.Column(db.String(30), nullable=True)
    english_full = db.Column(db.String(100), nullable=True)
    company_type = db.Column(db.String(10), nullable=False)
    records = db.relationship('Record', backref="company", lazy=False)

    def to_dict(self):
        return dict(id=self.id,
                    code=self.code,
                    name='({0}){1}'.format(self.short_name, self.full_name),
                    english_full=self.english_full,
                    english_short=self.english_short,
                    )
    # def serialize(self):
    #   return {
    #           'id': self.id,
    #           'code': self.code,
    #           'short_name': self.short_name,
    #           'full_name': self.full_name,
    #           'english_full': self.english_full,
    #           'english_short': self.english_short,
    #           }


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    query_text = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=True)
    year = db.Column(db.Integer)
    season = db.Column(db.String(3))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.code'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # def __init__(self, query_text, answer, year, season, user_id, company_id):
    #     self.query_text = query_text
    #     self.answer = answer
    #     self.year = year
    #     self.season = season
    #     self.user_id = user_id
    #     self.company_id = company_id

    def to_dict(self):
        return dict(id=self.id,
                    query_text=self.query_text,
                    answer=self.answer,
                    year=self.year,
                    season=self.season,
                    user_id=self.user_id,
                    company_id=self.company_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    )
        # questions=[question.to_dict() for question in self.questions])

    def company_to_dict(self):
        return dict(company_id=self.company_id,
                    company_name=self.company.short_name,
                    )


@app.route('/create_db')
def index():
    db.init_app(app)
    db.create_all()
    return 'ok'


if __name__ == "__main__":
    index()
