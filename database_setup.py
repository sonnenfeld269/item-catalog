import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

"""The declarative_base will let sqlalchemy know that our classes
are special alchemy classes that correspondent with our tables in our db
"""
Base = declarative_base()

class Restaurant(Base):
    """A restaurant class mapping to our restaurant table

    Args:
        Base: the parent class doing the mapping by sqlalchemy
    """

    __tablename__ = 'restaurant'

    name = Column(String(80), nullable = False)

    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    """A menu item class mapping to our manu_item table

    Args:
        Base: the parent class doing the mapping by sqlalchemy
    """

    __tablename__ = 'menu_item'

    name = Column(String(80), nullable = False)

    id = Column(Integer, primary_key = True)

    course =  Column(String(250))

    description = Column(String(250))

    price = Column(String(8))

    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    restaurant = relationship(Restaurant)


""" create_engine will create a new file to a more robust database like psql"""
engine = create_engine('sqlite:///restaurantmenu.db')

""" this will go to the database and add the classes as new tables in our database"""
Base.metadata.create_all(engine)
