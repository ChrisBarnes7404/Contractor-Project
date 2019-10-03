from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# INDEX
@app.route('/')
def playlists_index():
    """Return homepage."""
    """Show all items."""
    return render_template('index.html')
    #return render_template('index.html', items=items.find())

# CREATE NEW
#@app.route('/item/new')
#def playlists_new():
#    """Create a new playlist."""
#    return render_template('new_item.html', item={}, title='New Item')
