from flask import Flask, render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key = 'manishankar'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Simulate login success with mock user
        user = {
            'id': 1,
            'name': 'Mock User',
            'email': email,
            'role': 'admin' if email == 'admin@example.com' else 'user'
        }
        session['user'] = user
        flash('Logged in successfully!', 'success')
        return redirect(url_for('admin' if user['role'] == 'admin' else 'dashboard'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

        flash('Mock account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Simulate form submission logic (not saved anywhere)
    if request.method == 'POST':
        flash('Mock leave request submitted!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=session['user'])

@app.route('/admin')
def admin():
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('login'))

    # Mock list of leave requests
    requests = [
        {'id': 1, 'name': 'John Doe', 'reason': 'Vacation', 'from_date': '2025-04-20', 'to_date': '2025-04-25', 'status': 'Pending', 'created_at': '2025-04-17 10:00:00'},
        {'id': 2, 'name': 'Jane Smith', 'reason': 'Medical', 'from_date': '2025-04-18', 'to_date': '2025-04-20', 'status': 'Approved', 'created_at': '2025-04-16 09:30:00'},
    ]

    return render_template('admin.html', requests=requests)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
