import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

"""The declarative_base will let sqlalchemy know that our classes
are special alchemy classes that correspondent with our tables in our db
"""
Base = declarative_base()


class Category(Base):
    """A category class mapping to our category table

    Args:
        Base: the parent class doing the mapping by sqlalchemy
    """

    __tablename__ = 'category'

    name = Column(String(80), nullable=False)

    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class Item(Base):
    """An item class mapping to our item table

    Args:
        Base: the parent class doing the mapping by sqlalchemy
    """

    __tablename__ = 'item'

    title = Column(String(80), nullable=False)

    id = Column(Integer, primary_key=True)

    description = Column(String(250))

    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'category_id': self.category_id
        }


""" create_engine will create a new file to a more robust database like psql"""
engine = create_engine('sqlite:///category_item.db')

""" this will go to the database and add the classes as new tables in our database"""
Base.metadata.create_all(engine)
