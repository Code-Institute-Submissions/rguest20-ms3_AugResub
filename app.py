#Dependencies
from flask import Flask, redirect, url_for, render_template, request, abort, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
    password = db.Column(db.String(15))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    date_joined = db.Column(db.Date)
    messages = db.relationship('Message', backref='sender')

    def __repr__(self):
        return '<User %r>' % self.username

class Message(db.Model):
    __tablename__="messages"
    id= db.Column(db.Integer, primary_key = True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient= db.Column(db.String(64))
    date= db.Column(db.DateTime)
    title= db.Column(db.String(100))
    message=  db.Column(db.String(500))

    def __repr__(self):
        return '<Message %r>' % self.title

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
    message = StringField('Message:', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Python Shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Message=Message)

#Routing
@app.route("/", methods=['GET', 'POST'])
def index():
    form = NameForm()
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
    return render_template('index.html', form=form, name=session.get('name'), known = session.get('known', False))

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
                if user.password == form.password.data:
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
                new_user=User(username=form.username.data, password=form.password.data)
                db.session.add(new_user)
                db.session.commit()
                session['name']=form.username.data
                session['known'] = True
                return redirect(url_for('index'))
        return render_template('register.html', form=form)
    else:
        return redirect(url_for('index'))

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
        return render_template('message.html', name=session['name'], user=user)
    else:
        return redirect(url_for('register'))

@app.route('/messages/compose', methods=['POST', 'GET'])
def compose_message():
    try: session['name']
    except KeyError: session['name'] = None
    if session['name'] != None:
        user = User.query.filter_by(username=session['name']).first()
        form=ComposeMessageForm()
        return render_template('messagecompose.html', name=session['name'], user=user, form=form)
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#Run app
if __name__ == "__main__":
    app.run(
        host = os.environ.get("IP", "0.0.0.0"),
        port = int(os.environ.get("PORT", "5000")),
        debug = True
    )
