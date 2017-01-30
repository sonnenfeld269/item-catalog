from flask import Flask, render_template, request, url_for, redirect, jsonify
from database_service import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

#### User Actions

@app.route('/')
@app.route('/items')
def showAllData():
    """Get all items and categories. Calculate the number of items. And
    pass data to html template"""

    items = readAllItems()
    categories = readAllCategories()
    num_items = len(items)
    return render_template("display_all.html", categories = categories,
                            items = items, countItems = num_items)

@app.route('/<string:category_name>/items')
def showDataByCategory(category_name):
    """Get all items and categories. Calculate the number of items. And
    pass data to html template"""

    items = readItemsByName(category_name)
    categories = readAllCategories()
    num_items = len(items)
    return render_template("display_all.html", categories = categories,
                            items = items, countItems = num_items,
                            category_name=category_name)

#### Category - API Endpoints

@app.route('/categories/JSON')
def getAllCategoriesJSON():
    """Returns all categories as json."""

    categories = readAllCategories()
    return jsonify(Categories=[i.serialize for i in categories])

@app.route('/categories/<string:category_name>/JSON')
def getCategoryByNameJSON(category_name):
    category = readCategoryByName(category_name)
    return jsonify(Category=category.serialize)

#### Item - API Endpoints

@app.route('/<string:category_name>/items/JSON')
def getAllItemsJSON(category_name = None):
    """Returns all items as json.

    Args:
        category_name: string containing the category name

    Returns:
        string: json string
    """
    if category_name:
        items = readItemsByName(category_name)
    else:
        items = readAllItems()

    return jsonify(Items=[i.serialize for i in items])


@app.route('/<string:category_name>/items/new', methods=['POST'])
def addItem(category_name = None):
    if request.method == "POST":
        category_id=readCategoryByName(category_name).id
        item = createItem(request.form['title'],request.form['description'],category_id)
        return redirect(url_for('showAllCategories',category_name=category_name))
    else:
        return redirect(url_for('showAllCategories',category_name=category_name))

@app.route('/<string:category_name>/items/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_name, item_id):
    print "inside edit item"
    if request.method == "GET":
        item = readItemById(item_id)
        return redirect(url_for('showAllCategories',category_name=category_name,selected_item=item))
        #return "get"
    else:
        return "post"

@app.route('/<int:item_id>/delete', methods=['POST'])
def removeItem(item_id):
    item = readItemById(item_id)
    category_name = readCategoryById(item.category_id).name
    deleteItem(item_id)
    return redirect(url_for('showAllCategories',category_name=category_name))

#### Configuration

def dbSetup(dbtype,dbname):
    engine = create_engine('%s:///%s' % (dbtype,dbname))
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

dbSetup("sqlite","category_item.db")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
