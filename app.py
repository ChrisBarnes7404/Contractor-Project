from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor_Shopping')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items
comments = db.comments

app = Flask(__name__)

# INDEX
@app.route('/')
def items_index():
    """Return homepage."""
    """Show all items."""
    #return render_template('index.html')
    return render_template('index.html', items=items.find())

# CREATE NEW
@app.route('/item/new')
def items_new():
    """Create a new item."""
#    return render_template('new_item.html')
    return render_template('new_item.html', item={}, title='New Item')

# DISPLAY/SHOW
@app.route('/items', methods=['POST'])
def items_submit():
    """Submit a new item."""
    item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        #'videos': request.form.get('videos').split(),
        'created_at': datetime.now(),
        'ratings': request.form.get('ratings')
    }
    print(item)
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('show_items', item_id=item_id))

# DISPLAY/SHOW FROM ID
@app.route('/items/<item_id>')
def show_items(item_id):
    """Show a single item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    item_comments = comments.find({'item_id': ObjectId(item_id)})
    return render_template('show_item.html', item=item, comments=item_comments)
