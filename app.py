from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "123456789"
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref= 'author', lazy = True)

    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.image_file}")'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False, )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [
    {
        'author':'Vaibhav Kant Agrawal',
        'title' : 'Post 1',
        'content' : 'first post content',
        'date_posted' : 'April 20,2016' 
    },
    {
        'author':'Ayush Agrawal',
        'title' : 'Post 2',
        'content' : 'Second post content',
        'date_posted' : 'August 20,2016' 
    }
]

@app.route('/')
@app.route('/home')
def home():
    
    return render_template('home.html', posts = posts)


@app.route('/about')
def about():
    return render_template("about.html", title = "About")

@app.route('/register', methods = ['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        print(url_for('home'))
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'abc@xyz.com' and form.password.data == '123':
            flash(f'you have been logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Unsuccessful login, please check email/password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

if __name__=='__main__':
    app.run(debug = True)