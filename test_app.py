import unittest
import app
#Dependencies
from flask import Flask, redirect, url_for, render_template, request, abort, session, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import DecimalField
from wtforms.validators import DataRequired, NumberRange
from flask_mongoengine import MongoEngine
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import *
from dateutil.relativedelta import *
import calendar
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

# Configuration
basedir= os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['MONGODB_SETTINGS']={
    'db': 'freelance',
    'host': os.environ.get('MONGO_LOGIN'),
    'port': 27017,
    'username': 'admin',
    'password': 'Glnayr86'
}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = MongoEngine()
db.init_app(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app,db)

#Database Classes
class User(db.DynamicDocument):
    username = db.StringField()
    password_hash = db.StringField()
    role = db.StringField()
    date_joined = db.DateField()
    posts = db.ReferenceField('JobPost')

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
        'username': self.username,
        'password_hash': self.password_hash,
        'role': self.role,
        'date_joined': self.date_joined,
        'posts': self.posts
        }

class Message(db.DynamicDocument):
    sender = db.StringField()
    recipient = db.StringField()
    read_yn = db.BooleanField()
    sender_deleted = db.BooleanField()
    receiver_deleted = db.BooleanField()
    date = db.DateField()
    title = db.StringField()
    message = db.StringField()

    def to_json(self):
        return {
        'sender': self.sender,
        'recipient': self.recipient,
        'read_yn': self.read_yn,
        'sender_deleted': self.sender_deleted,
        'receiver_deleted': self.receiver_deleted,
        'date': self.date,
        'title': self.title,
        'message': self.message}

class JobPost(db.DynamicDocument):
    poster = db.StringField()
    title= db.StringField()
    description = db.StringField()
    budget = db.StringField()
    hourlypay = db.StringField()

    def to_json(self):
        return {
        'poster_id': self.poster_id,
        'title': self.title,
        'description': self.description,
        'budget': self.budget,
        'hourlypay': self.hourlypay
        }


class test_app(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        User(username='test', password_hash=generate_password_hash('test'), role="Freelancer", languages=['PHP'], date=datetime.utcnow()).save()
        JobPost(title='test', description='test', budget='100', hourlypay='', stack='PHP', poster='test').save()
        Message(sender='test', recipient='test', title='test', message='test', read_yn=False, sender_deleted=False, receiver_deleted=False, date=datetime.utcnow()).save()

    @classmethod
    def tearDownClass(cls):
        User.objects(username='test').first().delete()
        JobPost.objects(title='test').first().delete()
        try:  Message.objects(sender='test').first().delete()
        except: print("\nmessage deleted as expected")

    def test_databaseStructureUser(self):
        current_user = User.objects(username='test').first()
        self.assertEqual(current_user.role, 'Freelancer')
        self.assertNotEqual(current_user.role, 'Company')

    def test_databaseStructureJob(self):
        test_job = JobPost.objects(title='test').first()
        self.assertEqual(test_job.stack, 'PHP')

    def test_databaseStructureMessage(self):
        test_message = Message.objects(sender='test').first()
        self.assertEqual(test_message.recipient, 'test')

    def test_messageDeleteIfNowhereToShow(self):
        test_message = Message.objects(sender='test').first()
        test_message.receiver_deleted = True
        test_message.sender_deleted = True
        primarykey=test_message.id
        if test_message.receiver_deleted == True and test_message.sender_deleted == True:
            test_message.delete()
        self.assertFalse(Message.objects(id=primarykey).count() > 0)

    def testPasswordHashing(self):
        current_user = User.objects(username='test').first()
        print ("secret key is" + app.config['SECRET_KEY'])
        self.assertTrue(current_user.verify_password('test'))

if __name__ == '__main__':
    unittest.main()
