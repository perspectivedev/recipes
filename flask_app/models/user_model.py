# -------------------- File imports --------------------
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
# -------------------- Regex variables --------------------
ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# -------------------- class declaration and constructor init --------------------

class User:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
# -------------------- @classmethods --------------------

    # This @classmethod creates the user in the db. Its a setter.
    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
        

    # This @classmethod gets one user and that user's corresponding data from the db. Its a getter.
    @classmethod
    def get_one_user_by_id(cls, data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False


    # This @classmethod gets all users and that users' data from the db. Its a getter.
    @classmethod
    def get_all_users(cls, data):
        query = "SELECT * FROM users;"
        users_from_db =  connectToMySQL(DATABASE).query_db(query,data)
        users =[]
        for u in users_from_db:
            users.append(cls(u))
        return users


    # This @classmethod gets a users email data from the db. Its a getter.
    @classmethod
    def get_user_email(cls, data):
        query = """
        SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False


    # -------------------- @staticmethods --------------------

    # This @staticmethod is used for validation of the user.
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 1:
            is_valid = False
            flash('First name required', 'reg')
        elif len(data['first_name']) < 2:
            is_valid = False
            flash('First name must be 2 chars', 'reg')
        elif not ALPHA.match(data['first_name']):
            is_valid = False
            flash('First name must be letter only', 'reg')
        if len(data['last_name']) < 1:
            is_valid = False
            flash('Last name required', 'reg')
        elif len(data['last_name']) < 2:
            is_valid = False
            flash('Last name must be 2 chars', 'reg')
        elif not ALPHA.match(data['last_name']):
            is_valid = False
            flash('Last name must be letter only', 'reg')
        if len(data['email']) < 1:
            is_valid = False
            flash('Email required', 'reg')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Email must be valid format', 'reg')
        else:
            potential_user = User.get_user_email({'email': data['email']})
            if potential_user:
                flash('Email already exist in db (hope that was you)', 'reg')
                is_valid = False
        if len(data['password']) < 1:
            flash('pass reg', 'reg')
            is_valid = False
        elif len(data['password']) < 8:
            flash('Pass must be > 8 char', 'reg')
            is_valid = False
        elif data['password'] != data['confirm_pass']:
            flash('password must match', 'reg')
            is_valid = False
            
            
        return is_valid
