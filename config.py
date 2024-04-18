from flask import Flask,request,render_template
import psycopg2 
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
import os

user = os.environ["PG_USER"]
password = os.environ["PG_PASSWORD"]
uri = f"postgresql+psycopg2://{user}:{password}@localhost:5432/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
print('success')
print(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
app= app


try: 
    conn = psycopg2.connect(database="postgres", user="postgres",  
    password="root", host="localhost")
    print("connected")
except as e:
    print ("I am unable to connect to the database")
    print(e)
mycursor =conn.cursor()
