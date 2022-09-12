from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import Create_accountForm, LoginForm, CatForm
from app.models import User, Add_Cat
from flask_login import login_user, logout_user, login_required, current_user 


@app.route('/')
def hello_cat():
    cats = Add_Cat.query.all()
    return render_template('index.html', cats=cats)

@app.route('/addcats', methods=['GET', 'POST'])
@login_required
def cat():
    form = CatForm()
    if form.validate_on_submit():
        fav_cat_breed = form.fav_cat_breed.data
        fav_int_cat = form.fav_int_cat.data
        fav_cat_fact = form.fav_cat_fact.data
        new_cat = Add_Cat(fav_cat_breed=fav_cat_breed, fav_int_cat=fav_int_cat, fav_cat_fact=fav_cat_fact, user_id= current_user.id)
        flash(f"{new_cat.fav_int_cat} has been added to the kitty collection!", "info")
        return redirect(url_for('hello_cat'))
    return render_template('addcats.html', form=form)

@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    form = Create_accountForm()
    if form.validate_on_submit():
        print('Form is validated. That is such cool beans man')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('A user with that username or email already exists!', 'danger')
            return redirect(url_for('create_account'))
        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been added to website!", "success")
        return redirect(url_for('hello_cat')) 
    return render_template('createaccount.html', form=form)

@app.route('/loginpage', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"Welcome {user.username}!", "success")
            return redirect(url_for('hello_cat'))

        else:
            flash('Bad username and/or password, Please try signing in again', 'danger')
            return redirect(url_for('login'))
    return render_template('loginpage.html', form=form) 

@app.route('/logout')
def logout():
    logout_user()
    flash('You have now logged out and left the kitty kingdom', 'primary')
    return redirect(url_for('hello_cat'))


@app.route('/cats/<cat_id>')
@login_required
def view_cat(cat_id):
    cat = Add_Cat.query.get_or_404(cat_id)
    return render_template('viewcat.html', cat=cat)


@app.route('/cats/<cat_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_cat(cat_id):
    cat_to_edit = Add_Cat.query.get_or_404(cat_id)
    if cat_to_edit.author != current_user:
        flash("I'm sorry, you do not have permission to edit that cat!", "danger")
        return redirect(url_for('view_cat', cat_id = cat_id))
    form = CatForm()
    if form.validate_on_submit():
        fav_cat_breed = form.fav_cat_breed.data
        fav_int_cat = form.fav_int_cat.data
        fav_cat_fact = form.fav_cat_fact.data
        cat_to_edit.update_cat (fav_cat_breed=fav_cat_breed, fav_int_cat=fav_int_cat, fav_cat_fact=fav_cat_fact)
        flash(f"{cat_to_edit.fav_int_cat} has been updated for you", "success")
        return redirect(url_for('view_cat', cat_id=cat_id))
    return render_template('editcat.html', cat=cat_to_edit, form=form)    

@app.route('/cats/<cat_id>/delete')
@login_required
def delete_cat(cat_id):
    cat_to_delete = Add_Cat.query.get_or_404(cat_id)
    if cat_to_delete.author != current_user:
        flash("You can't do that! You're not allowed to delete that cat!!!", "danger")
        return redirect(url_for('hello_cat'))
    cat_to_delete.delete()
    flash(f"{cat_to_delete.fav_int_cat} has been deleted, how sad meow meow", "info")
    return redirect(url_for('hello_cat'))

@app.route('/user/<user_id>')
@login_required
def user_pro(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('userprofile.html', user= user)