from app import app
from app.forms import LoginForm, RegistrationForm, CarSearchForm
from app.models import User
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import requests
from config import Config

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    data = {"status":1}
    form = CarSearchForm(status = 1)
    if request.method == 'POST':
        if form.body_type.data is not 0:
            data["body_type"]=form.body_type.data
        if form.colour.data is not 0:
            data["colour"]=form.colour.data
        if form.make.data is not "":
            data["make"]=form.make.data
        if form.seats.data is not None:
            data["seats"]=form.seats.data
        print(data)
    r = requests.get('https://192.168.1.109:10100/cars',json = data, verify=False)
    retdata = r.json() or {}    
    print(retdata)
    form.body_type.choices = make_select_list(Config.BODY_TYPE)
    form.colour.choices = make_select_list(Config.CAR_COLORS)
    return render_template('index.html', title='Home',form = form,cars = retdata, Config = Config)
    
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print("test")
        data = {'username':form.username.data,'password':form.password.data}
        r = requests.post('https://192.168.1.109:10100/users',json = data, verify=False)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def make_select_list(arr):
    i = 0
    c = []
    for value in arr:
        c.append((i,arr[i]))
        i+=1
    return c