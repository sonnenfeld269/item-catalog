from flask import Flask, render_template, request, url_for, redirect
from database_service import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)



@app.route('/hello')
def HelloWorld():
    return "HelloWorld"
    
@app.route('/')
@app.route('/restaurants/')
def showAllRestaurants():
    result = readAllRestaurants()
    print "returning" + str(result)
    return render_template("restaurants.html", restaurants = result)

@app.route('/restaurants/<int:restaurant_id>')
def showRestaurant(restaurant_id):
    print "inside show restaurant"
    print restaurant_id
    result = readRestaurantById(restaurant_id)
    menuItems = readMenuItemsByRestaurant(restaurant_id)
    return render_template("restaurant.html", restaurant = result, menuItems = menuItems)

@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
    if request.method == "POST":
        restaurant = createRestaurant(request.form['name'])
        return redirect(url_for('showRestaurant',restaurant_id=restaurant.id))
    else:
        return render_template("add_restaurant.html")

"""
@app.route('/restaurants/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
    return "new"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "edit"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "delete"
"""

def dbSetup(dbtype,dbname):
    engine = create_engine('%s:///%s' % (dbtype,dbname))
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

dbSetup("sqlite","restaurantmenu.db")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
