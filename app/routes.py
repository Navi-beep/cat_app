from app import app
from flask import render_template

@app.route('/')
def hello_cat():
    cat_info = {
        'breed': 'Tuxedo cat',
        'name': 'Salem'
    }

    return render_template('index.html', cat = cat_info)