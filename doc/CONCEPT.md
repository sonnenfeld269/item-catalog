**Table of Contents**

- [Concept](#concept)
  - [Project structure](#project-structure)
  - [Roadmap](#roadmap)
  - [Implementation](#implementation)
    - [Database Layer](#database-layer)
    - [Service Layer](#service-layer)
      - [Database Service](#database-service)
      - [Basic Server](#basic-server)

# Concept

## Project structure

- item_catalog/
    - doc/                - all documentation-related files
    - basic_server.py     - using a simple HTTP Basic Server
    - project.py          - using Flask Framework
    - database_setup.py      - creates our database by ORM
    - database_service.py    - uses crud-methods to operate on our db

## Roadmap

1. Database Layer
  * Create db-model
  * Create a [database_setup file](../database_setup.py)
  * Create a [database_service file](../database_setup.py)
  * Create a [basic_server.py](../basic_server.py)

## Implementation

### Database Layer

First we create our model

![model](model.png)

Now we create a database configuration file with our objects

**database_setup.py**
```
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
```

If we run this file with `python database_setup.py` then it create our
**restaurantmenu.db** file, which contains our `CREATE` statements.

### Service Layer

#### Database Service

Now we need a module to do CRUD operations on our db. For that we use
sessions in sqlalchemy. They allow us to call queries and commit them.

Check [database_service file](../database_service.py) for code and documentation.

#### Basic Server

Now we need to establish a basic server for communication between our server(localhost) and the client(browser).
Here is the documented [basic_server file](../basic_server.py).
