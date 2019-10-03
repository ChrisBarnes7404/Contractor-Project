from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor_Shopping')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items
#comments = db.comments

app = Flask(__name__)

# INDEX
@app.route('/')
def items_index():
    """Return homepage."""
    """Show all items."""
    return render_template('index.html')
    #return render_template('index.html', items=items.find())

# CREATE NEW
@app.route('/item/new')
def items_new():
    """Create a new item."""
    return render_template('new_item.html')
#    return render_template('new_item.html', item={}, title='New Item')
