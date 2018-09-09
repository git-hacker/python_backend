import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()






class Driver(db.Model):
    __tablename__ = "drivers"
    id = db.Column(db.String, primary_key=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # firstname = db.Column(db.String, nullable=False)
    # lastname = db.Column(db.String, nullable=False)



    cars = db.relationship("Car", backref="drivers", lazy=True)
    cars = db.Column(db.String, db.ForeignKey("cars.numbe"),nullable=True)
    journeys = db.relationship("Journey", backref="drivers", lazy=True)
    journeys = db.Column(db.String, db.ForeignKey("journeys.id"),nullable=True)




    gender = db.Column(db.String, nullable= True)
    age =db.Column(db.Integer, nullable= True)
    point =db.Column(db.Float, nullable= True)


    # def add_car(self, """info of car"""):
    #     c = Car("""info of car""")
    #     db.session.add(c)
    #     db.session.commit()

class Car(db.Model):
    __tablename__ = "cars"
    numbe = db.Column(db.String, primary_key=True, nullable=False)
    policy = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Float) # default 2.5
    height = db.Column(db.Float) # default 1.6
    load = db.Column(db.Float) # default 0.9
    weight = db.Column(db.Float) # default 10
    axlesNum = db.Column(db.Integer) # default 2
    province = db.Column(db.String)
    owner = db.Column(db.String)



    driver = db.Column(db.String, db.ForeignKey("drivers.id"), nullable=False)
    journey = db.Column(db.String, db.ForeignKey("journeys.id"), nullable=False)

class Journey(db.Model):
    __tablename__ = "journeys"
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    end = db.Column(db.Integer)
    time= db.Column(db.Integer)

    driver = db.Column(db.String, db.ForeignKey("drivers.id"), nullable=False)

def add_user(id,pw):
    user = Driver(id= id,password=pw, point=0)
    db.session.add(user)
    db.session.commit()
