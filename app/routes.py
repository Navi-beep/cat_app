from app import app
from flask import render_template

@app.route('/')
def hello_cat():
    cat_info = {
        'breed': 'Tuxedo cat',
        'name': 'Salem'
    }

    breeds = ['tuxedo cat', 'norwegian forest cat', 'tortoise shell', 'british shorthair', 'siamese cat', 'sphynx cat', 'munchkin cat', 'siberian cat', 'tonkinese cat', 'van cat', 'burmese cat', 'british longhair', 'persian cat']

    
    return render_template('index.html', cat = cat_info, breeds=breeds)

@app.route('/cats')
def cat():
    return '<h1>Cats are superior</h1>'