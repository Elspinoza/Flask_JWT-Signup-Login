from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/auth'  # Mettez à jour avec les informations appropriées
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
