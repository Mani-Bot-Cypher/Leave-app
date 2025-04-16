class Config:
    MYSQL_HOST = 'leave-db'  # Name of the MySQL service in OpenShift
    MYSQL_USER = 'leaveuser'  # from Secret
    MYSQL_PASSWORD = 'leavepass123'  # from Secret
    MYSQL_DATABASE = 'leavedb'  # from Secret
