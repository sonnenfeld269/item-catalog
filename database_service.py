import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from database_setup import Base, Item, Category
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

""" TODO How to create a doc reference to Base?"""
engine = create_engine('sqlite:///category_item.db')

""" this will bin our engine to the Base, to map to our sqlite db"""
Base.metadata.bind = engine


""" A session establish a connection between our classes and the tables in the db"""
DBSession = sessionmaker(bind=engine)

""" It is a collection of all commands to sql, and will only be called when commit is called"""
session = DBSession()

# Item Service Methods


def createItem(title, description, category_id):
    item = Item(title=title, description=description, category_id=category_id)
    session.add(item)
    session.commit()
    return item


def readAllItems():
    result = session.query(Item).all()
    return result


def readItemById(id):
    item = session.query(Item).filter_by(id=id).one()
    return item


def readItemsByName(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return items


def updateItem(id, title, description):
    item = session.query(Item).filter_by(id=id).one()
    item.title = title
    item.description = description
    session.add(item)
    session.commit()


def deleteItem(id):
    item = session.query(Item).filter_by(id=id).one()
    session.delete(item)
    session.commit()


def countItems():
    return session.query(Item).count()

# Category Service Methods


def createCategory(name):
    category = Category(name=name)
    session.add(category)
    session.commit()
    return category


def readAllCategories():
    result = session.query(Category).all()
    return result


def readCategoryById(id):
    category = session.query(Category).filter_by(id=id).one()
    return category


def readCategoryByName(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    return category


def updateCategory(id, name):
    category = session.query(Category).filter_by(id=id).one()
    category.name = name
    session.add(category)
    session.commit()


def deleteCategory(id):
    category = session.query(Category).filter_by(id=id).one()
    session.delete(category)
    session.commit()

# MenuItem Service Methods


def createMenuItem(name, course, description, price, item_id):
    menuItem = MenuItem(name=name, course=course, description=description,
                        price=price, item_id=item_id)
    session.add(menuItem)
    session.commit()


def readAllMenuItems():
    result = session.query(MenuItem).all()
    output = "ID  |NAME  | COURSE| description \n"
    for r in result:
        output += str(r.id) + " : " + r.name + " : " + \
            r.course + " : " + r.description + ";\n"
    return output


def readMenuItemsByItem(item_id):
    result = session.query(MenuItem).filter_by(item_id=item_id)
    return result


def updateMenuItem(id, name, course, description, price, item_id):
    menuItem = session.query(MenuItem).filter_by(id=id)
    menuItem.name = name
    menuItem.description = description
    menuItem.price = price
    menuItem.item_id = item_id
    session.add(menuItem)
    session.commit()


def deleteMenuItem(id):
    menuItem = session.query(MenuItem).filter_by(id=id).one()
    session.delete(menuItem)
    session.commit()


def dropAndCreate():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def fillDb():
    dropAndCreate()

    # create WATER items
    createCategory("Water")
    createItem("Orca", "Swimming in oceans", 1)
    createItem("Tuna", "Swimming in oceans", 1)
    createItem("Goldfish", "Swimming in sweet waters", 1)

    # create AIR items
    createCategory("Air")
    createItem("Cape crow", "The Cape crow or black crow (Corvus capensis) is"
               " slightly larger than the carrion crow"
               " and is completely black with a slight gloss of purple in"
               " its feathers.", 2)
    createItem("Eagle", "Flying through mountains", 2)

    # create LAND items
    createCategory("Land")
    createItem("Ape", "Moving on trees", 3)
    createItem("Lion", "Living in dessert", 3)

    print readAllCategories()
    print readAllItems()

# dropAndCreate()
# fillDb()
