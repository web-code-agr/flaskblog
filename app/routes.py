from app import app,db,bcrypt
from app.models import User,Post
from flask import render_template, flash, redirect, url_for
from app.forms import RegistrationForm, LoginForm


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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! you are now able to log in!', 'success')
        return redirect(url_for('login'))
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