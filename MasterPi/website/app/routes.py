from app import app

@app.route('/')
@app.route('/index')
def index():
    return "index page"
    
@app.route('/login')
def index():
    return "login page"

@app.route('/signup')
def index():
    return "signup page"
