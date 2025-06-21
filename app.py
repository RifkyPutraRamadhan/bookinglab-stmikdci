from flask import Flask, render_template, request, redirect, url_for, session, flash
from logic import fifo_scheduling, sjf_scheduling, round_robin_scheduling
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

bookings = []
booking_id_counter = 1

app = Flask(__name__)
app.secret_key = 'stmikdci'
users = {
    "admin": {
        "password": generate_password_hash("admin"),
        "name": "Rifky Putra Ramadhan",
        "nim": "11240025"
    }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            session['name'] = users[username]['name']
            session['nim'] = users[username]['nim']
            flash('Login berhasil!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout!', 'info')
    return redirect(url_for('login'))

@app.before_request
def require_login():
    allowed_routes = ['login', 'static', 'about']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))

class Booking:
    def __init__(self, id, nim, name, duration, arrival_time):
        self.id = id
        self.nim = nim
        self.name = name
        self.duration = duration
        self.arrival_time = arrival_time
        self.start_time = None
        self.end_time = None

@app.route('/')
def index():
    return render_template('index.html', bookings=bookings, scheduled_data=[])

@app.route('/add_booking', methods=['POST'])
def add_booking():
    global booking_id_counter
    nim = request.form['nim']
    name = request.form['name']
    duration = int(request.form['duration'])
    arrival_time = int(request.form['arrival_time'])
    
    new_booking = Booking(booking_id_counter, nim, name, duration, arrival_time)
    bookings.append(new_booking)
    booking_id_counter += 1
    
    return redirect(url_for('index'))

@app.route('/clear_bookings', methods=['POST'])
def clear_bookings():
    global bookings, booking_id_counter
    bookings = []
    booking_id_counter = 1
    return redirect(url_for('index'))

@app.route('/schedule', methods=['POST'])
def schedule():
    algorithm = request.form['algorithm']
    time_quantum = int(request.form.get('time_quantum', 1))
    
    if algorithm == 'fifo':
        scheduled = fifo_scheduling(bookings.copy())
        execution_log = [{
            'id': b.id,
            'name': b.name,
            'nim': b.nim,
            'start': b.start_time,
            'end': b.end_time,
            'duration': b.end_time - b.start_time
        } for b in scheduled]
    elif algorithm == 'sjf':
        scheduled = sjf_scheduling(bookings.copy())
        execution_log = [{
            'id': b.id,
            'name': b.name,
            'nim': b.nim,
            'start': b.start_time,
            'end': b.end_time,
            'duration': b.end_time - b.start_time
        } for b in scheduled]
    elif algorithm == 'rr':
        scheduled, execution_log = round_robin_scheduling(bookings.copy(), time_quantum)
    else:
        scheduled = []
        execution_log = []

    return render_template('index.html', 
                           bookings=bookings, 
                           scheduled=scheduled, 
                           algorithm=algorithm,
                           scheduled_data=execution_log)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)