import os

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'mysql'),
    'user': os.environ.get('DB_USER', 'leaveuser'),
    'password': os.environ.get('DB_PASSWORD', 'leavepass'),
    'database': os.environ.get('DB_NAME', 'leave_app_db')
}
