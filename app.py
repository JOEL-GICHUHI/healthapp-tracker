import itertools
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

appointment_id_counter = itertools.count(1)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

USERS = {"user@health.com": "password123"}
appointments = []
dosages = []

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
def login():
    # Clear old flashes unrelated to login
    session.pop('_flashes', None)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session['user'])

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=session['user'])

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/instructions')
@login_required
def instructions():
    return render_template('instructions.html')

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        flash('Thank you for your feedback!')
        return redirect(url_for('dashboard'))
    return render_template('feedback.html')

@app.route('/privacy')
@login_required
def privacy():
    return render_template('privacy.html')

@app.route('/appointments')
@login_required
def appointments_list():
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def appointments_add():
    if request.method == 'POST':
        new_id = next(appointment_id_counter)
        appointments.append({
            'id': new_id,
            'name': request.form.get('appointment_name'),
            'doctor': request.form.get('doctor_name'),
            'date': request.form.get('appointment_date'),
        })
        flash('Appointment saved successfully!')
        return redirect(url_for('appointments_list'))
    return render_template('appointments_add.html')

@app.route('/appointments/cancel/<int:id>', methods=['POST'])
@login_required
def cancel_appointment(id):
    global appointments
    appointments = [a for a in appointments if a.get('id') != id]
    flash('Appointment canceled')
    return redirect(url_for('appointments_list'))

@app.route('/appointments/reschedule/<int:id>', methods=['POST'])
@login_required
def reschedule_appointment(id):
    new_date = request.form.get('new_date')
    for a in appointments:
        if a.get('id') == id:
            a['date'] = new_date
            break
    flash('Appointment rescheduled')
    return redirect(url_for('appointments_list'))

@app.route('/dosage')
@login_required
def dosage_list():
    return render_template('dosage.html', dosages=dosages)

@app.route('/dosage/add', methods=['GET', 'POST'])
@login_required
def dosage_add():
    if request.method == 'POST':
        dosages.append({
            'medicine': request.form.get('medicine_name'),
            'prescription': request.form.get('prescription'),
            'morning': request.form.get('morning', 'off') == 'on',
            'afternoon': request.form.get('afternoon', 'off') == 'on',
            'night': request.form.get('night', 'off') == 'on',
        })
        flash('Medicine saved successfully!')
        return redirect(url_for('dosage_list'))
    return render_template('dosage_add.html')

@app.route('/cycle')
@login_required
def cycle():
    return render_template('cycle.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)