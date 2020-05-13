from app import app
from app.forms import LoginForm
from app.models import User
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import requests

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        data = {'username':form.username.data,'password':form.password.data}
        r = requests.post('https://192.168.1.109:10100/auth',json = data, verify=False)
        retdata = r.json() or {}
        if 'id' in retdata:
            user = User(username=retdata['username'],id=retdata['id']) 
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/regist')
def regist():
    return "signup page"

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
