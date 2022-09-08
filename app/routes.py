from app import app
from flask import render_template
from app.forms import Create_accountForm

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
    return render_template('cats.html')


@app.route('/createacct', methods=["GET", "POST"])
def createacct():
    form = Create_accountForm()
    print("Form has been validated")
    return render_template('createacct.html', form=form)
