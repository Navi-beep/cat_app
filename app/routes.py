from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import Create_accountForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user 


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


@app.route('/createaccount', methods=['GET', 'POST'])
def createacct():
    form = Create_accountForm()
    if form.validate_on_submit():
        print('Form is validated. That is such cool beans man')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('A user with that username or email already exists!', 'danger')
            return redirect(url_for('createacct'))
        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been added to website!", "success")
        return redirect(url_for('hello_cat')) 
    return render_template('createaccount.html', form=form)

        