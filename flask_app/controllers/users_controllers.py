# -------------------- File imports --------------------
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
bcrypt = Bcrypt(app)
# -------------------- Controllers/Routes for models --------------------

# This route establishes (renders) the index page and the statement block within recognizes if a user is in session.
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/recipes')
    return render_template('index.html')

# -------------------- POST methods --------------------

# This route establishes the POST method of the registeration form.
@app.route('/user/registration', methods=['POST'])
def user_regration():
    print(request.form)
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect('/')
        
        # hash the password
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        **request.form,
        'password': hashed_pass,
    }
    logged_user_id = User.create_user(data)
    session['user_id'] = logged_user_id
    session['first_name'] = request.form['first_name']
    return redirect('/recipes')


# This route establishes the POST method of the login form.
@app.route('/user/login', methods=['POST'])
def user_login():
    data = {
        'email': request.form['email']
        }
    potential_user = User.get_user_email(data)
    if not potential_user:
        flash('Invalid credentials', 'log')
        print('user not found')
        return redirect('/')
    
    if not bcrypt.check_password_hash(potential_user.password,request.form['password']):
        flash('Invalid credentials', 'log')
        print('invalid password')
        return redirect('/')
    session['user_id'] = potential_user.id
    session['first_name'] = potential_user.first_name
    return redirect('/recipes')


# This route establishess the...
@app.route('/user/logout')
def user_logout():
    del session['user_id']
    del session['first_name']
    return redirect('/')