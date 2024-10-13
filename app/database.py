import pymysql
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

pymysql.install_as_MySQLdb()
