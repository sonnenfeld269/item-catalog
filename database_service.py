import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

""" TODO How to create a doc reference to Base?"""
engine = create_engine('sqlite:///restaurantmenu.db')

""" this will bin our engine to the Base, to map to our sqlite db"""
Base.metadata.bind = engine

""" A session establish a connection between our classes and the tables in the db"""
DBSession = sessionmaker(bind=engine)

""" It is a collection of all commands to sql, and will only be called when commit is called"""
session = DBSession()

# Restaurant Service Methods


def createRestaurant(name):
    restaurant = Restaurant(name=name)
    session.add(restaurant)
    session.commit()


def readAllRestaurants():
    result = session.query(Restaurant).all()
    return result

def readRestaurantById(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    return restaurant

def updateRestaurant(id, name):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    restaurant.name = name
    session.add(restaurant)
    session.commit()

def deleteRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    session.delete(restaurant)
    session.commit()


#### MenuItem Service Methods


def createMenuItem(name, course, description, price, restaurant_id):
    menuItem = MenuItem(name=name, course=course, description=description,
                        price=price, restaurant_id=restaurant_id)
    session.add(menuItem)
    session.commit()


def readAllMenuItems():
    result = session.query(MenuItem).all()
    output = "ID  |NAME  | COURSE| description \n"
    for r in result:
        output += str(r.id) + " : " + r.name + " : " + r.course + " : " + r.description + ";\n"
    return output


def updateMenuItem(id, name, course, description, price, restaurant_id):
    menuItem = session.query(MenuItem).filter_by(id=id)
    menuItem.name = name
    menuItem.description = description
    menuItem.price = price
    menuItem.restaurant_id = restaurant_id
    session.add(menuItem)
    session.commit()


def deleteMenuItem(id):
    menuItem = session.query(MenuItem).filter_by(id=id).one()
    session.delete(menuItem)
    session.commit()
