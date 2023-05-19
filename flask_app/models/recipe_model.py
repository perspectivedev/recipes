# -------------------- File imports --------------------

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash
import re

# -------------------- Regex variables --------------------

ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# -------------------- class declaration and constructor init --------------------

class Recipe:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_minutes = data['under_30_minutes']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


# -------------------- @classmethods --------------------

    # This @classmethod creates an initial recipe by the user to the db. Its a setter.
    @classmethod
    def create_recipe(cls, data):
        query = """
        INSERT INTO recipes (user_id, name, description, instructions, under_30_minutes, date_cooked)
        VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(under_30_minutes)s, %(date_cooked)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def update_recipe(cls, data):
        query = """
        UPDATE recipes SET name=%(name)s,description=%(description)s,instructions=%(instructions)s,under_30_minutes=%(under_30_minutes)s,date_cooked = %(date_cooked)s WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


    # This @classmethod creates an initial recipe by the user to the db. Its a setter.
    @classmethod
    def get_recipe_id(cls, data):
        query = """
        SELECT * FROM recipes WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False


    # This @classmethod creates an initial recipe by the user to the db. Its a setter.
    @classmethod
    def get_one_recipe_by_user(cls, data):
        query = """
            SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;
            """
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        print(results)
        if results:
            one_recipe = cls(results[0])
            user_data = {
                    **results[0],
                    'id': results[0]['users.id'],
                    'created_at': results[0]['users.created_at'],
                    'updated_at': results[0]['users.updated_at']
                }
            user_instance = user_model.User(user_data)
            one_recipe.chef = user_instance
            return one_recipe
        return False


    # This @classmethod creates an initial recipe by the user to the db. Its a setter.
    @classmethod
    def get_all_recipes_by_users(cls):
        query = """
            SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;
            """
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes = []
        
        if results:
            for row in results:
                recipe_instance = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                user_instance = user_model.User(user_data)
                recipe_instance.chef = user_instance
                all_recipes.append(recipe_instance)
            return all_recipes

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)

    # -------------------- @staticmethods --------------------

    # This @staticmethod is used for validation
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 1:#1
            is_valid = False
            flash('Name of recipe is required')
        elif len(data['name']) < 2:
            is_valid = False
            flash('Name of recipe must be 2 chars')
        if len(data['description']) < 1:#2
            is_valid = False
            flash('Description must not be blank')
        elif len(data['description']) < 3:
            is_valid = False
            flash('First name must be 3 chars')
        if len(data['instructions']) < 1:#3
            is_valid = False
            flash('Instructions must not be blank')
        elif len(data['instructions']) < 3:
            is_valid = False
            flash('Instructions must be 3 chars')
        if  'under_30_minutes' not in data:#4
            is_valid = False
            flash('Check "Yes" or "No"')
        if len(data['date_cooked']) < 1:#5
            is_valid = False
            flash('Must select or enter a date')
        elif len(data['date_cooked']) < 3:
            is_valid = False
            flash('Date must be valid')
        return is_valid
