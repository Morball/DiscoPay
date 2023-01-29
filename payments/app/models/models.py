from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
db=SQLAlchemy(app)


class Subscription(db.Model):

    __tablename__ ='subscription'

    id = db.Column(db.Integer, primary_key=True)
    payment_id=db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(100),unique=True, nullable=False)
    expiration_date = db.Column(db.DateTime, default=datetime.now()+timedelta(days=30), nullable=True)


