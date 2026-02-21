from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

USERS = {"123": "123"}
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

@app.route('/appointments')
@login_required
def appointments_list():
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def appointments_add():
    if request.method == 'POST':
        appointments.append({
            'name': request.form.get('appointment_name'),
            'doctor': request.form.get('doctor_name'),
            'date': request.form.get('appointment_date'),
        })
        flash('Appointment saved successfully!')
        return redirect(url_for('appointments_list'))
    return render_template('appointments_add.html')

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
    app.run(debug=True)