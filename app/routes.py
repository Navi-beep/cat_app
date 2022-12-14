from urllib import response

from flask_cors import cross_origin
from app import app
from flask import render_template, redirect, url_for, flash, jsonify
from app.forms import Create_accountForm, LoginForm, CatForm
from app.models import User, Add_Cat
from flask_login import login_user, logout_user, login_required, current_user
import requests
import json 


@app.route('/')
def hello_cat():
    cats = Add_Cat.query.all()
    users = User.query.all()
    return render_template('index.html', cats=cats, users=users) 

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
        flash(f"{new_user.username} has been added to website, Please log in!", "success")
        return redirect(url_for('login')) 
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
    cats = Add_Cat.query.filter_by(user_id=user_id)
    return render_template('userprofile.html', user = user, cats=cats)

@app.route('/catimg')
@login_required
def cat_img():
    url ='https://api.thecatapi.com/v1/images/search?size=small'
    res = requests.get(url)
    cat_meow = eval(res.text)[0]['url']
    res_data = {
        'cat_meow' : cat_meow 
    }
    return jsonify(res_data) 

@app.route('/catphoto')
@login_required
def cat_photo():
    return render_template('catphoto.html')

@app.route('/favcats')
@login_required
def fav_cats():
    fam_cats = {'kittie':[
        {
         'name': 'BigOldBuns aka Dingus',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0V6nMQQnXmeJWypRB95gLlZ60S_NJsoWblg&usqp=CAU',
        'breed': 'tuxedo cat', 
        'linktocat': 'https://www.tiktok.com/@bigoldbuns/video/7103565800862207274?is_from_webapp=1&sender_device=pc&web_id=7125098913833141806'
        
        }, {
         'name': 'BoneBone',
        'image': 'https://scontent-ort2-1.xx.fbcdn.net/v/t1.18169-9/27973072_1039662136200166_4310467451451989784_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=ytfyDmyTi_MAX9ALeLn&_nc_ht=scontent-ort2-1.xx&oh=00_AT_QZBX2Y0ZAkpyPXveSXjzsOzfVUezm3fFN0ZTJEp0U-g&oe=6344FD2D',
        'breed': 'persian cat', 
        'linktocat': 'https://www.instagram.com/bonebone29/?fbclid=IwAR06P6Qe5JLEzGL-mULOGERAXNuQfzkn1JUtedU78plZvkv-zgrlM8AUYY8'
        
        }, {

        'name': 'Smudge Lord',
        'image': 'https://cdn.shopify.com/s/files/1/0255/4016/5720/files/Capture_720x.png?v=1637120671',
        'breed': 'white cat', 
        'linktocat': 'https://www.tiktok.com/@smudge_lord/video/7002688427669916934?is_from_webapp=1&sender_device=pc&web_id=7125098913833141806'
        } , 
        {

        'name': 'Bento aka Keyboard Cat',
        'image': 'https://scontent-ort2-1.xx.fbcdn.net/v/t1.6435-9/129021515_3742224249164856_3674502398938652537_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=730e14&_nc_ohc=_0mrfk90Q60AX81QMMz&_nc_ht=scontent-ort2-1.xx&oh=00_AT-gHO8grzQ6QKAacbVE70FIJFWi-3sw63HZJKG3Jzi2ww&oe=63488E86',
        'breed': 'tabby', 
        'linktocat': 'https://fb.watch/fxYmhhYAz-/'
        }
    ]} 

    return render_template('favcats.html', fam_cats = fam_cats['kittie'])


@app.route('/catfriends')
@login_required
def hello_friends():
    users = User.query.all()
    return render_template('catfriends.html', users=users) 


    # credits:
    #https://www.tiktok.com/@bigoldbuns
    #https://www.facebook.com/bonebone29
    #https://www.instagram.com/bonebone29/
    #https://smudge-lord.com/
    #https://www.tiktok.com/@smudge_lord
    #https://www.facebook.com/thekeyboardcat
    #https://scontent-ort2-1.xx.fbcdn.net/v/t1.6435-9/129021515_3742224249164856_3674502398938652537_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=730e14&_nc_ohc=_0mrfk90Q60AX81QMMz&_nc_ht=scontent-ort2-1.xx&oh=00_AT-gHO8grzQ6QKAacbVE70FIJFWi-3sw63HZJKG3Jzi2ww&oe=63488E86
    #https://www.facebook.com/thekeyboardcat/photos/pb.100044369021492.-2207520000../3742224245831523/?type=3