import os
from flask import Flask, render_template, request, redirect, url_for
from flask_user import login_required, UserManager, UserMixin
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# pymongo settings
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor_Shopping')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items
comments = db.comments

# Flask settings
SECRET_KEY = os.getenv("SECRET_KEY")

# Flask-User settings
USER_APP_NAME = "Flask-User MongoDB App"  # Shown in and email templates and page footers
USER_ENABLE_EMAIL = False      # Disable email authentication
USER_ENABLE_USERNAME = True    # Enable username authentication
USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form

# Setup Flask
app = Flask(__name__)
#app.config.from_object(__name__+'.ConfigClass')

# Define the User document.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Document, UserMixin):
    active = db.BooleanField(default=True)

    # User information
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')

    # User authentication information
    username = db.StringField(default='')
    password = db.StringField()

    # Relationships
    roles = db.ListField(db.StringField(), default=[])

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)


########## COMMENT ROUTES ##########
@app.route('/items/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'item_id': ObjectId(request.form.get('item_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('show_item', item_id=request.form.get('item_id')))


@app.route('/items/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('show_item', item_id=comment.get('item_id')))
