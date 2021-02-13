#Dependencies
from flask import Flask, redirect, url_for, render_template, request, abort, session, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.fields.html5 import DecimalField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Configuration
basedir= os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'very hard to guess string'
bootstrap = Bootstrap(app)
migrate = Migrate(app,db)

#Database Classes
class Role(db.Model):
    __tablename__="roles"
    id= db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User', backref = 'role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__="users"
    id= db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    date_joined = db.Column(db.Date)
    inbox_id = db.Column(db.Integer, db.ForeignKey('inbox.id'))
    outbox_id = db.Column(db.Integer, db.ForeignKey('outbox.id'))
    posts = db.relationship("JobPost", backref="poster")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Inbox(db.Model):
    __tablename__="inbox"
    id= db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(50))
    owners=db.relationship("User", backref="inbox")
    recieved_messages=db.relationship("Message", backref = "recipient")

    def __repr__(self):
        return '<Inbox %r>' % self.id

class Outbox(db.Model):
    __tablename__="outbox"
    id = db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(50))
    owners=db.relationship("User", backref="outbox")
    sent_messages=db.relationship("Message", backref = "sender")

    def __repr__(self):
        return '<Outbox %r>' % self.id

class Message(db.Model):
    __tablename__="messages"
    id= db.Column(db.Integer, primary_key = True)
    sender_id = db.Column(db.Integer, db.ForeignKey('outbox.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('inbox.id'))
    read_yn = db.Column(db.Boolean)
    sender_deleted = db.Column(db.Boolean)
    reciever_deleted = db.Column(db.Boolean)
    date = db.Column(db.DateTime)
    title = db.Column(db.String(100))
    message = db.Column(db.String(500))

    def __repr__(self):
        return '<Message %r>' % self.title

class JobPost(db.Model):
    __tablename__="posts"
    id=db.Column(db.Integer, primary_key=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title= db.Column(db.String(100))
    description = db.Column(db.String(500))
    budget = db.Column(db.String(10))
    hourlypay = db.Column(db.String(10))

    def __repr__(self):
        return '<Post %r>' % self.title

#Form Classes
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    password = PasswordField('What is your password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Enter your username', validators=[DataRequired()])
    password = PasswordField("Enter your password", validators=[DataRequired()])
    password2 = PasswordField("Re-enter your password", validators=[DataRequired()])
    submit = SubmitField('Submit')

class ComposeMessageForm(FlaskForm):
    send_to = StringField("Username to send to:", validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    message = TextAreaField('Message:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangeUserTypeForm(FlaskForm):
    new_type=StringField('Change Privileges:', validators=[DataRequired()])
    submit=SubmitField('Change User Type')

class JobPostForm(FlaskForm):
    title= StringField('Title:', validators=[DataRequired()])
    description= TextAreaField('Description of Job:', validators=[DataRequired()])
    budget = DecimalField('How much are you looking to spend:')
    hourlypay = DecimalField('How much do you pay per hour:',  validators=[NumberRange(min=0, max=100000, message='bla')])
    submit = SubmitField('Submit')

class JobSearchForm(FlaskForm):
    term=StringField('Search Term:', validators=[DataRequired()])
    searchfield= SelectField('Search By:', choices=[('title', 'Title'), ('locationj', 'Location'), ('languagesj', 'Programming Languages')])
    submit=SubmitField('Search')

class FreelancerSearchForm(FlaskForm):
    term=StringField('Search Term:', validators=[DataRequired()])
    searchfield= SelectField('Search By:', choices=[('username', 'Username'), ('locationf', 'Location'), ('languagesf', 'Programming Languages')])
    submit=SubmitField('Search')

class CompanySearchForm(FlaskForm):
    term=StringField('Search Term:', validators=[DataRequired()])
    searchfield= SelectField('Search By:', choices=[('company', 'Company Name'), ('locationc', 'Location'), ('languagesc', 'Programming Languages Required')])
    submit=SubmitField('Search')

#Python Shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Message=Message, Inbox=Inbox, Outbox=Outbox, JobPost=JobPost)

#Routing
@app.route("/", methods=['GET', 'POST'])
def index():
    try: current_user=User.query.filter_by(username=session['name'])
    except KeyError:
        session['name'] = None
        current_user = None
    form = NameForm()
    if session['name'] != None:
        posts = current_user[0].posts
    else:
        posts = []
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user == None:
            flash("Username not found")
        else:
            if user.password == form.password.data:
                session['known'] = True
                session['name'] = form.name.data
            else:
                session['known'] = False
                flash('Password/Username combination incorrect')
        form.name.data = ""
        return redirect(url_for('index'))
    return render_template('index.html', user=current_user, form=form, name=session.get('name'), known = session.get('known', False), posts=posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        return redirect(url_for('index'))
    else:
        form = NameForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.name.data).first()
            if user == None:
                flash("Username not found")
            else:
                if user.verify_password(form.password.data) == True:
                    session['known'] = True
                    session['name'] = form.name.data
                    return redirect(url_for('index'))
                else:
                    form.name.data = ""
                    session['known'] = False
                    flash('Password/Username combination incorrect')
    return render_template('login.html', form=form, name=session.get('name'), known = session.get('known', False))

@app.route("/register", methods=['GET', 'POST'])
def register():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] == None:
        form = RegisterForm()
        if form.validate_on_submit():
            users = User.query.filter_by(username=form.username.data).first()
            try: user_registered = users[0].username
            except TypeError: user_registered = None
            if user_registered == form.username.data:
                flash("Username already exists")
            else:
                new_inbox=Inbox(name=form.username.data)
                db.session.add(new_inbox)
                db.session.commit()
                new_outbox=Outbox(name=form.username.data)
                db.session.add(new_outbox)
                db.session.commit()
                new_user=User(username=form.username.data, password=form.password.data, inbox=new_inbox, outbox=new_outbox)
                db.session.add(new_user)
                db.session.commit()
                session['name']=form.username.data
                session['known'] = True
                return redirect(url_for('index'))
        return render_template('register.html', form=form)
    else:
        return redirect(url_for('index'))

@app.route("/account", methods=['GET', 'POST'])
def account():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        user=User.query.filter_by(username=session['name']).first()
        form=ChangeUserTypeForm()
        if form.validate_on_submit():
            new_role=Role.query.filter_by(name=request.values.get('new_type')).first()
            user.role = new_role
            db.session.commit()
        return render_template('account.html', name=session['name'], form=form, user=user)
    else:
        return redirect(url_for('register'))

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session['name'] = None
    session['known'] = False
    return redirect(url_for('index'))

@app.route('/messages')
def message():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        user = User.query.filter_by(username=session['name']).first()
        messages_recieved = user.inbox.recieved_messages
        rcount = []
        for message in messages_recieved:
            if message.reciever_deleted == False:
                rcount.append(message)
        recieved_count = len(rcount)
        messages_sent = user.outbox.sent_messages
        scount = []
        for message in messages_sent:
            if message.sender_deleted == False:
                scount.append(message)
        sent_count=len(scount)
        return render_template('message.html', name=session['name'], messages_recieved=messages_recieved, rcount=recieved_count, scount= sent_count, messages_sent = messages_sent)
    else:
        return redirect(url_for('register'))

@app.route('/userlist')
def user_list():
    list=User.query.all()
    message = []
    for user in list:
        message.append(user.username)
    return jsonify(message)

@app.route('/messages/compose', methods=['POST', 'GET'])
def compose_message():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        user = User.query.filter_by(username=session['name']).first()
        form=ComposeMessageForm()
        if form.validate_on_submit():
            send_to=form.send_to.data
            send_to_exist= True
            send_to_exist_checker = User.query.filter_by(username=send_to).first()
            send_to_user = Inbox.query.filter_by(name=send_to).first()
            try: send_to = send_to_exist_checker.username
            except AttributeError: send_to_exist = False
            send_from=session['name']
            send_from_id=Outbox.query.filter_by(name=send_from).first()
            title=form.title.data
            message=form.message.data
            if send_to_exist == False:
                flash("This username is not valid")
            else:
                message_to_send=Message(sender=send_from_id, recipient=send_to_user, title=title, message=message, read_yn=False, sender_deleted=False, reciever_deleted=False)
                db.session.add(message_to_send)
                db.session.commit()
                return redirect(url_for('message'))
        return render_template('messagecompose.html', name=session['name'], user=user, form=form)
    else:
        return redirect(url_for('register'))

@app.route('/message/delete/reciever', methods=['POST'])
def delete_from_recipient():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        message_number=request.values.get('message_id')
        message_to_delete= Message.query.filter_by(id=message_number).first()
        message_to_delete.reciever_deleted = True
        db.session.commit()
        if message_to_delete.sender_deleted == True:
            db.session.delete(message_to_delete)
            db.session.commit()
        return redirect(url_for('message'))
    else:
        return redirect(url_for('register'))

@app.route('/message/delete/sender', methods=['POST'])
def delete_from_sender():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        message_number=request.values.get('message_id')
        message_to_delete= Message.query.filter_by(id=message_number).first()
        message_to_delete.sender_deleted = True
        db.session.commit()
        if message_to_delete.reciever_deleted == True:
            db.session.delete(message_to_delete)
            db.session.commit()
        return redirect(url_for('message'))
    else:
        return redirect(url_for('register'))

@app.route("/message/reply", methods=['POST'])
def reply():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        form=ComposeMessageForm()
        message_number=request.values.get('message_id')
        try: message_content=Message.query.filter_by(id=message_number)[0]
        except IndexError: message_content = None
        is_correspondence=request.values.get('send')
        message_to_reply_to= Message.query.filter_by(id=message_number).first()
        return render_template("messagereply.html", message=message_content, correspondence=is_correspondence, name=session['name'], form=form)
    else:
        return redirect(url_for('register'))

@app.route("/message/send", methods=['POST'])
def send():
    send_to=request.values.get('recipient')
    send_to_user = Inbox.query.filter_by(name=send_to).first()
    send_from=session['name']
    send_from_id=Outbox.query.filter_by(name=send_from).first()
    title=request.values.get('title')
    message_data=request.values.get('message')
    message_to_send=Message(sender=send_from_id, recipient=send_to_user, title=title, message=message_data,read_yn=False, sender_deleted=False, reciever_deleted=False)
    db.session.add(message_to_send)
    db.session.commit()
    return redirect(url_for('message'))

@app.route("/jobpost", methods=['GET', 'POST'])
def post_form():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        form=JobPostForm()
        return render_template("jobpost.html", name=session['name'], form=form)
    else:
        return redirect(url_for('register'))

@app.route("/jobpost/post", methods=['POST'])
def post_job():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        title = request.values.get('title')
        description = request.values.get('description')
        budget = request.values.get('budget')
        hourlypay = request.values.get('hourlypay')
        poster = User.query.filter_by(username=session['name']).first()
        post = JobPost(title=title, description=description, budget=budget, hourlypay=hourlypay, poster=poster)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('register'))

@app.route("/jobpost/delete", methods=['POST'])
def delete_job():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        job_number=request.values.get('post_number')
        job_to_delete= JobPost.query.filter_by(id=job_number).first()
        db.session.delete(job_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('register'))

@app.route("/about")
def about():
    return render_template("about.html", name=session['name'])

@app.route('/user/<id>')
def get_user(id):
    return render_template("user.html", id=id)

@app.route("/contact")
def contact():
    return render_template("contact.html", name=session['name'])

@app.route("/browser")
def browser():
    user_agent = request.headers.get("user-agent")
    return '<p>Your browser is {}</p>'.format(user_agent)

@app.route("/search")
def search():
    jobform=JobSearchForm()
    freelancerform=FreelancerSearchForm()
    companyform=CompanySearchForm()
    return render_template("search.html", name=session['name'], job=jobform, freelancer=freelancerform, company=companyform)

@app.errorhandler(404)
def page_not_found(e):
    try: session['name']
    except KeyError: session['name'] = None
    return render_template('404.html', e=e, name=session['name']), 404

@app.errorhandler(500)
def internal_server_error(e):
    try: session['name']
    except KeyError: session['name'] = None
    return render_template('500.html', e=e, name=session['name']), 500

#Run app
if __name__ == "__main__":
    app.run(
        host = os.environ.get("IP", "0.0.0.0"),
        port = int(os.environ.get("PORT", "5000")),
        debug = True
    )
