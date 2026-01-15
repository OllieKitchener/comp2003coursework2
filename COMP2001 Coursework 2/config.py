import pathlib
import connexion
import pyodbc
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app

server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=Yes;'
    'TrustServerCertificate=Yes;'
    'Connection Timeout=30;'
    'Trusted_Connection=No'
)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={conn_str}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

def initialize_database():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        columns = [
            'id INT IDENTITY(1,1) PRIMARY KEY',
            'lname VARCHAR(25) UNIQUE',
            'fname VARCHAR(25)',
            'timestamp DATETIME',
        ]
        create_table_cmd = f"IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'person') CREATE TABLE person ({','.join(columns)})"

        cursor.execute(create_table_cmd)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database connection verified and table checked.")
    except Exception as e:
        print(f"Database setup error: {e}")

initialize_database()