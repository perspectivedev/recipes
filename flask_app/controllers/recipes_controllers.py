# -------------------- File imports --------------------
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User
bcrypt = Bcrypt(app)
# -------------------- Controllers/Routes for models --------------------


# -------------------- render_templates --------------------
# This route establishes(renders) the recipes dashboard page and the logic within recognizes if a user is in session 
# This route establishes (renders) the index page and the statement block within recognizes if a user is in session.
@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_one_user_by_id(data)
    all_recipes = Recipe.get_all_recipes_by_users()
    return render_template('welcome_user.html', all_recipes=all_recipes, logged_user=logged_user)


@app.route('/recipes/new')
def render_add_recipe():
    if 'user_id'not in session:
        return redirect('/')
    return render_template('add_recipe.html')


@app.route('/recipes/edit/<int:id>')
def render_edit_recipe(id):
    if 'user_id'not in session:
        return redirect('/')
    data = {
        'id': id,
        'user_id': session['user_id']
    }
    one_recipe = Recipe.get_one_recipe_by_user(data)
    return render_template('edit_recipe.html', one_recipe=one_recipe)


@app.route('/recipes/<int:id>')
def render_view_recipe(id):
    if 'user_id'not in session:
        return redirect('/')
    data = {
        'id': id
    }
    one_recipe = Recipe.get_one_recipe_by_user(data)
    return render_template('view_recipe.html', one_recipe=one_recipe)

# -------------------- POST methods --------------------

# This route establishes the POST method of the registeration form.
@app.route('/recipes/new', methods=['POST'])
def recipe_new():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    if not Recipe.validate_recipe(data):
        return redirect('/recipes/new')
    
    Recipe.create_recipe(data)
    print(data)
    return redirect('/recipes')



# This route establishess the an edit page for the user in session.
@app.route('/recipes/update/<int:id>', methods=['POST'])
def recipe_edit(id):
    if 'user_id'not in session:
        return redirect('/')
    data = {
        **request.form,
        'id': id,
    }
    if not Recipe.validate_recipe(data):
        return redirect(f'/recipes/edit/{id}')
    
    Recipe.update_recipe(data)
    return redirect('/recipes')


# This route establishess a link the recipe id and deletes the row of information for that id.
@app.route('/recipes/delete/<int:id>')
def recipe_delete(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    Recipe.destroy(data)
    return redirect('/recipes')
















# This route establishes...
# This route establishes...
# This route establishes...
# This route establishes...
# This route establishes...
# This route establishes...
# This route establishes...