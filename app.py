from flask import Flask, render_template, request, redirect, url_for
#from flask_user import login_required, UserManager, UserMixin
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# pymongo settings
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor_Shopping')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items
comments = db.comments

app = Flask(__name__)

# INDEX
@app.route('/')
def items_index():
    """Show all items via the Home page which is accessible to anyone."""
    return render_template('item_index.html', items=items.find())

# CREATE NEW
@app.route('/new/item')
def items_new():
    """Create a new item."""
    return render_template('new_item.html', item={}, title='New Item')

# EDIT
@app.route('/items/<item_id>/edit')
def items_edit(item_id):
    """Show the edit form for an item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('items_edit.html', item=item, title='Edit item')

# UPDATE
@app.route('/items/<item_id>', methods=['POST'])
def items_update(item_id):
    """Submit an edited item."""
    updated_item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        #'videos': request.form.get('videos').split(),
        'ratings': request.form.get('ratings'),
        'price': request.form.get('price')
    }
    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})
    return redirect(url_for('show_item', item_id=item_id))

# DISPLAY/SHOW
@app.route('/items', methods=['POST'])
def items_submit():
    """Submit a new item."""
    item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        #'videos': request.form.get('videos').split(),
        'created_at': datetime.now(),
        'ratings': request.form.get('ratings'),
        'price': request.form.get('price')
        }
    print(item)
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('show_item', item_id=item_id))

# DISPLAY/SHOW FROM ID
@app.route('/items/<item_id>')
def show_item(item_id):
    """Show a single item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    #item_comments = comments.find({'item_id': ObjectId(item_id)})
    #return render_template('show_item.html', item=item, comments=item_comments)
    return render_template('show_item.html', item=item)

# Delete Item
@app.route('/items/<item_id>/delete', methods=['POST'])
def items_delete(item_id):
    """Delete one item."""
    items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('items_index'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)
