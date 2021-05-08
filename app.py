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
from dotenv import load_dotenv
load_dotenv()

#create multiple checkbox field from wtforms
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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
app.config['SECRET_KEY'] = 'very hard to guess string'
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

class UpdateUserForm(FlaskForm):
    new_type = SelectField('Change Privileges:', choices = [('Freelancer', 'Freelancer'), ('Company', 'Company'), ('Administrator', 'Administrator')], validators=[DataRequired()])
    languages = MultiCheckboxField('Programming Language:', choices=[('cpp', 'C++'), ('py', 'Python'), ('rb', 'Ruby')])
    biography = TextAreaField('Bio:')
    hourlyrate = DecimalField('Hourly Rate:')
    submit=SubmitField('Update Details')

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
    return dict(db=db, User=User, Message=Message, JobPost=JobPost)

#Routing
@app.route("/verify")
def verify():
    return (
    '<p>'+ mongologin +'</p>'
    )

@app.route("/", methods=['GET', 'POST'])
def index():
    try: current_user=User.objects(username=session['name']).first()
    except KeyError:
        session['name'] = None
        current_user = None
    form = NameForm()
    usercount = User.objects(role="Freelancer").count()
    companycount = User.objects(role="Company").count()
    if session['name'] != None:
        posts = JobPost.objects(poster=session['name'])
    else:
        posts = JobPost.objects()
    if form.validate_on_submit():
        user = User.objects(username=form.name.data).first()
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
    return render_template('index.html', usercount=usercount, companycount=companycount, user=current_user, form=form, name=session.get('name'), known = session.get('known', False), posts=posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        return redirect(url_for('index'))
    else:
        form = NameForm()
        if form.validate_on_submit():
            user = User.objects(username=form.name.data).first()
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
            users = User.objects(username=form.username.data).first()
            try: user_registered = users.username
            except TypeError: user_registered = None
            except AttributeError: user_registered = None
            if form.password.data != form.password2.data:
                flash ("Password mismatch, please check and try again")
            else:
                if user_registered == form.username.data:
                    flash("Username already exists")
                else:
                    User(username=form.username.data, password_hash=generate_password_hash(form.password.data), role="Freelancer", date=datetime.utcnow()).save()
                    session['name']=form.username.data
                    session['known'] = True
                    return redirect(url_for('account'))
        return render_template('register.html', form=form)
    else:
        return redirect(url_for('index'))

@app.route("/account", methods=['GET', 'POST'])
def account():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        user=User.objects(username=session['name']).first()
        form=UpdateUserForm()
        if form.validate_on_submit():
            language = request.form.getlist('languages')
            languages = []
            for response in language:
                if response == "cpp":
                    languages.append("C++")
                if response == "py":
                    languages.append("Python")
                if response == "rb":
                    languages.append("Ruby")
            new_role = request.values.get('new_type')
            hourlyrate = request.values.get('hourlyrate')
            bio = request.values.get('biography')
            user.update(role=new_role, hourly_rate = hourlyrate, languages=languages, bio=bio)
            flash("Details Updated")
            return redirect(url_for("account"))
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
        user = User.objects(username=session['name']).first()
        messages_received = Message.objects(recipient=session['name'])
        rcount = []
        for message in messages_received:
            if message.receiver_deleted == False:
                rcount.append(message)
        received_count = len(rcount)
        messages_sent = Message.objects(sender=session['name'])
        scount = []
        for message in messages_sent:
            if message.sender_deleted == False:
                scount.append(message)
        sent_count=len(scount)
        return render_template('message.html', name=session['name'], messages_received=messages_received, rcount=received_count, scount= sent_count, messages_sent = messages_sent)
    else:
        return redirect(url_for('register'))

@app.route('/userlist')
def user_list():
    list=User.objects()
    message = []
    for user in list:
        message.append(user.username)
    return jsonify(message)

@app.route ('/userdata')
def user_data():
    data = User.objects(username = session['name']).first()
    return jsonify(data)

@app.route('/messages/compose', methods=['POST', 'GET'])
def compose_message():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        user = User.objects(username=session['name']).first()
        form=ComposeMessageForm()
        if form.validate_on_submit():
            send_to=form.send_to.data
            send_to_exist= True
            send_to_exist_checker = User.objects(username=send_to).first()
            if len(send_to_exist_checker) < 1:
                send_to_exist = False
            send_from=session['name']
            title=form.title.data
            message=form.message.data
            if send_to_exist == False:
                flash("This username is not valid")
            else:
                message_to_send=Message(sender=send_from, recipient=send_to, title=title, message=message, read_yn=False, sender_deleted=False, receiver_deleted=False, date=datetime.utcnow()).save()
                return redirect(url_for('message'))
        return render_template('messagecompose.html', name=session['name'], user=user, form=form)
    else:
        return redirect(url_for('register'))

@app.route('/message/delete/receiver', methods=['POST'])
def delete_from_recipient():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        message_id=request.values.get('message_id')
        message_to_delete= Message.objects(id=message_id, recipient=session['name']).first()
        message_to_delete.update(receiver_deleted = True)
        if message_to_delete.sender_deleted == True:
            message_to_delete.delete()
        return redirect(url_for('message'))
    else:
        return redirect(url_for('register'))

@app.route('/message/delete/sender', methods=['POST'])
def delete_from_sender():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        message_id=request.values.get('message_id')
        message_to_delete= Message.objects(id=message_id, sender=session['name']).first()
        message_to_delete.update(sender_deleted = True)
        if message_to_delete.receiver_deleted == True:
            message_to_delete.delete()
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
        is_correspondence=request.values.get('send')
        message_content= Message.objects(id=message_number).first()
        return render_template("messagereply.html", message=message_content, correspondence=is_correspondence, name=session['name'], form=form)
    else:
        return redirect(url_for('register'))

@app.route("/message/send", methods=['POST'])
def send():
    send_to=request.values.get('recipient')
    send_from=session['name']
    title=request.values.get('title')
    message_data=request.values.get('message')
    message_to_send=Message(sender=send_from, recipient=send_to, title=title, message=message_data,read_yn=False, sender_deleted=False, receiver_deleted=False).save()
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
        poster = session['name']
        post = JobPost(title=title, description=description, budget=budget, hourlypay=hourlypay, poster=poster).save()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('register'))

@app.route("/jobpost/delete", methods=['POST'])
def delete_job():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        job_number=request.values.get('post_number')
        job_to_delete= JobPost.objects(id=job_number).first()
        job_to_delete.delete()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('register'))

@app.route("/about")
def about():
    return render_template("about.html", name=session['name'])

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

@app.route("/search/results", methods=['POST'])
def results():
    jobform=JobSearchForm()
    freelancerform=FreelancerSearchForm()
    companyform=CompanySearchForm()
    type = request.values.get('type')
    field = request.values.get('searchfield')
    term = request.values.get('term')
    if type == "freelancer":
        results = User.objects(username__icontains=term, role="Freelancer")
    elif type == "company":
        results = User.objects(username__icontains=term, role="Company")
    else:
        results = JobPost.objects(title__icontains=term)
    return render_template('searchresults.html', name=session['name'], results=results, job=jobform, freelancer=freelancerform, company=companyform)

@app.route("/profile/<username>")
def profile(username):
    user = User.objects(username=username).first()
    return render_template('profile.html', name=session['name'], profile=user)

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
