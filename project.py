from flask import Flask
from database_service import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)


@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "HelloWorld"

@app.route('/restaurants')
def showAllRestaurants():
    result = readAllRestaurants();
    output = ""
    for r in result:
        output += r.name + "</br></br>"
    return output

def dbSetup(dbtype,dbname):
    engine = create_engine('%s:///%s' % (dbtype,dbname))
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

dbSetup("sqlite","restaurantmenu.db")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
