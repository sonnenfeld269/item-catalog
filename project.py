from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from database_service import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

# User Actions


@app.route('/')
@app.route('/items')
def showAllData():
    """Get all items and categories. Calculate the number of items. And
    pass data to html template"""

    items = readAllItems()
    categories = readAllCategories()
    num_items = len(items)

    rendered_categories = render_template("category/show_all_categories.html",
                                          categories=categories)

    rendered_items = render_template("item/show_items.html", items=items,
                                     categories=categories,
                                     countItems=num_items)

    return render_template("display_all.html",
                           categories=rendered_categories,
                           items=rendered_items)


@app.route('/<string:category_name>/items')
def showDataByCategory(category_name):
    """Get all items and categories. Calculate the number of items. And
    pass data to html template"""

    items = readItemsByName(category_name)
    categories = readAllCategories()
    num_items = len(items)

    rendered_categories = render_template("category/show_all_categories.html",
                                          categories=categories,
                                          category_name=category_name)

    show_form = request.args.get('show_form')
    rendered_items = render_template("item/show_items.html",
                                     items=items, categories=categories,
                                     category_name=category_name,
                                     countItems=num_items)

    return render_template("display_all.html",
                           categories=rendered_categories,
                           items=rendered_items)


@app.route('/items/<int:item_id>')
@app.route('/<string:category_name>/items/<int:item_id>')
def showItem(category_name=None, item_id=None):
    """Show a single item"""

    item = readItemById(item_id)
    if not category_name:
        category_name = readCategoryById(item.category_id).name

    return render_template("item/single_item.html",
                           category_name=category_name,
                           item=item)


@app.route('/items/new', methods=['GET', 'POST'])
@app.route('/<string:category_name>/items/new', methods=['GET', 'POST'])
def addItem(category_name=None):
    """Render and return an add-item form if the request is GET.
    If there is a POST request, then add the item to the database.

    Args:
        category_name: name of the category

    """

    if request.method == "GET":

        categories = readAllCategories()

        if category_name:
            return render_template('item/add_item.html',
                                   category_name=category_name,
                                   categories=categories)
        else:
            return render_template('item/add_item.html',
                                   categories=categories)
    else:
        if request.form['title'] and request.form['description']:
            category_name = request.form['selected_category_name']
            category_id = readCategoryByName(category_name).id
            item = createItem(request.form['title'], request.form[
                              'description'], category_id)
            flash("Item successfully added!", "success")
            return redirect(url_for('showDataByCategory', category_name=category_name))
        else:
            flash("Missing Title, Content or Category Name.", "danger")
            return redirect(url_for('showDataByCategory', category_name=category_name))


@app.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
@app.route('/<string:category_name>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_name=None, item_id=None):
    category_name = ""

    if request.method == "GET":
        item = readItemById(item_id)
        if not category_name:
            category_name = readCategoryById(item.category_id).name
        return render_template('item/edit_item.html', item=item,
                               category_name=category_name,
                               categories=readAllCategories())
    else:
        if request.form['title'] and request.form['description'] and request.form['selected_category_name']:
            updateItem(item_id, request.form['title'],
                       request.form['description'],
                       request.form['selected_category_name'])
            flash("Item successfully edited!", "success")
            return redirect(url_for('showDataByCategory',
                                    category_name=category_name))
        else:
            # TODO is this approach ok?
            item = Item()
            item.title = request.form['title']
            item.description = request.form['description']
            flash("Missing Title, Content or Category Name.", "danger")
            return render_template('item/edit_item.html', item=item,
                                   category_name=category_name,
                                   categories=readAllCategories())


@app.route('/items/<int:item_id>/delete', methods=['POST'])
@app.route('/<string:category_name>/items/<int:item_id>/delete', methods=['POST'])
def removeItem(category_name=None, item_id=None):
    """Deletes an item from the database."""

    # delete item
    deleteItem(item_id)
    flash("Item successfully deleted!", "success")

    # redirect to showDataByCategory
    if category_name:
        return redirect(url_for('showDataByCategory', category_name=category_name))
    else:
        return redirect(url_for('showAllData'))
# Category - API Endpoints


@app.route('/categories/JSON')
def getAllCategoriesJSON():
    """Returns all categories as json."""

    categories = readAllCategories()
    return jsonify(Categories=[i.serialize for i in categories])


@app.route('/categories/<string:category_name>/JSON')
def getCategoryByNameJSON(category_name):
    category = readCategoryByName(category_name)
    return jsonify(Category=category.serialize)

# Item - API Endpoints


@app.route('/<string:category_name>/items/JSON')
def getAllItemsJSON(category_name=None):
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

# Configuration


def dbSetup(dbtype, dbname):
    engine = create_engine('%s:///%s' % (dbtype, dbname))
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

dbSetup("sqlite", "category_item.db")

if __name__ == '__main__':
    app.secret_key = "my_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
