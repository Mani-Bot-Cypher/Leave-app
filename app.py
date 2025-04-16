from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
from config import Config


app = Flask(__name__)
app.secret_key = 'secret_key'

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user'] = user
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin' if user['role'] == 'admin' else 'dashboard'))
        else:
            flash('Invalid email or password', 'danger')
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

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, phone, email, password, role) VALUES (%s, %s, %s, %s, %s)',
                           (name, phone, email, password, 'user'))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.errors.IntegrityError as e:
            if 'Duplicate entry' in str(e):
                flash('An account with this email already exists.', 'warning')
            else:
                flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        reason = request.form['reason']
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO leave_requests (user_id, reason, from_date, to_date) VALUES (%s, %s, %s, %s)',
                       (session['user']['id'], reason, from_date, to_date))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Leave request submitted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=session['user'])

@app.route('/admin')
def admin():
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT l.id, u.name, l.reason, l.from_date, l.to_date, l.status, l.created_at 
        FROM leave_requests l JOIN users u ON l.user_id = u.id
        ORDER BY l.created_at DESC
    ''')
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', requests=requests)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(100),
            role VARCHAR(10) DEFAULT 'user'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            reason TEXT,
            from_date DATE,
            to_date DATE,
            status VARCHAR(20) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()



create_tables()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

