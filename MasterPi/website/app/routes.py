from app import app
from app.forms import LoginForm, RegistrationForm, CarSearchForm, BookingForm
from app.models import User
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import requests
from config import Config
from datetime import date, datetime, timedelta

"""
This module contains the templates for structuring dynamic content
on the pages. It returns objects that in turn render html based on
the status of numerous factors such as the user currently validated.
- index
- login
- register
- logout
- book_car_request(id):
- my_bookings():
- car_info(id):
- cancel_booking(id):
- location(id):
These are prefixed with decorators which are used to enforce certain validation
when particular pages are loaded.
"""
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
    r = requests.get('http://192.168.1.109:10100/cars',json = data, verify=False)
    retdata = r.json() or {}    
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
        r = requests.post('http://192.168.1.109:10100/auth',json = data, verify=False)
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
        data = {'username':form.username.data,'password':form.password.data,'email':form.email.data}
        r = requests.post('http://192.168.1.109:10100/users',json = data, verify=False)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/book_car_request/<int:id>', methods=['GET', 'POST'])
@login_required
def book_car_request(id):
    form = BookingForm(date = date.today(),time = datetime.now() + timedelta(hours=1) , car_id = id, user_id = current_user.id)
    if form.validate_on_submit():
        time_start = datetime.combine(form.date.data, form.time.data)
        data = {
            'user_id':form.user_id.data, 
            'car_id':form.car_id.data, 
            'time_start': time_start.isoformat(),
            'hours':form.duration.data
        }
        r = requests.post('http://192.168.1.109:10100/book',json = data, verify=False)
        bookingData = r.json()
        r = requests.get('http://192.168.1.109:10100/cars/{}'.format(data['car_id']), verify=False)
        carData = r.json()
        if 'id' in bookingData:
            start = datetime.fromisoformat(bookingData['timestart']).strftime("%m/%d/%Y, %H:%M")
            flash('you booked {carname} for {hours} hours starting {start}'.format(carname = carData['name'], hours = bookingData['dration'], start = start))
            return redirect(url_for('index'))
        else:
            flash("The {carname} has been booked, try book another one".format(carname = carData['name']))
            return redirect(url_for('index'))
    return render_template('book.html', title = 'Make a Booking', form = form, id = id)

@app.route('/my_bookings', methods=['GET'])
@login_required
def my_bookings():
    r = requests.get('http://192.168.1.109:10100/user_bookings/{}'.format(current_user.id), verify=False)
    retdata = r.json() or {} 
    for booking in retdata:
        booking['timestart'] = datetime.fromisoformat(booking['timestart']).strftime("%m/%d/%Y, %H:%M")
    return render_template('myBookings.html', title='My Bookings',bookings = retdata, Config = Config)


@app.route('/car_info/<int:id>', methods=['GET'])
def car_info(id):
    r = requests.get('http://192.168.1.109:10100/cars/{}'.format(id), verify=False)
    retdata = r.json() or {}
    return render_template('index.html', title='Car No.{}'.format(id), cars = [retdata], Config = Config)

@app.route('/cancel_booking/<int:id>')
def cancel_booking(id):
    r = requests.get('http://192.168.1.109:10100/cancel_booking/{}'.format(id), verify=False)
    retdata = r.json() or {}
    if 'id' in retdata:
        start = datetime.fromisoformat(retdata['timestart']).strftime("%m/%d/%Y, %H:%M")
        flash('Booking No.{bid} starting {start} is canceled'.format(bid = retdata['id'], start = start))
        return redirect(url_for('index'))
    else:
        flash('An Error Occored:{}'.format(retdata['message']))
        return redirect(url_for('index'))

@app.route('/location/<int:id>')
def location(id):
    r = requests.get('http://192.168.1.109:10100/cars/{}'.format(id), verify=False)
    retdata = r.json() or {}
    location = retdata['location'][1:-1]
    location = location.replace(" ","")
    link = "https://maps.googleapis.com/maps/api/staticmap?center={}".format(location)
    link = link + "&zoom=13&size=600x300&maptype=roadmap"
    link = link + "&markers=color:blue%7Clabel:S%7C{}".format(location)
    link = link + "&key=AIzaSyBLCm8iSwMX79BiYI-aIfanIin70ql51QI"
    carinfo = "{}, a {} {} made by {} with {} seats, for A${}/h".format(retdata['name'], Config.CAR_COLORS[retdata["colour"]], Config.BODY_TYPE[retdata["body_type"]], retdata["make"], retdata["seats"], retdata["rate"])
    return render_template('location.html', title = "Location", location = retdata['location'].replace(" ",""), carinfo = carinfo, link = link)



def make_select_list(arr):
    i = 0
    c = []
    for value in arr:
        c.append((i,arr[i]))
        i+=1
    return c

if __name__ == "__main__":
    pass