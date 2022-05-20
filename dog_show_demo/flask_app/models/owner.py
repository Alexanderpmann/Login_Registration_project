from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



# class - owner for model - data is same as form + mysql - no need for pass_conf here


class Owner:
    def __init__(self, data):
        self.id = data["id"]

        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @staticmethod
    def validate_register(data):
        is_valid = True

        # first name validation
        if len(data["first_name"]) < 3:
            flash("First Name must be at least 3 characters long!")
            is_valid = False
        # last name validation
        if len(data["last_name"]) < 3:
            flash("Last Name must be at least 3 characters long!")
            is_valid = False

        # email validation (1 - valid email)
        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid Email!")
            is_valid = False
        # email validation (2 - is email already in use?)
        if Owner.get_by_email(data):
            flash("Email already in use! Please register new email or login!")
            is_valid = False

        # password validation
        if len(data["password"]) < 5:
            flash("Password must be at least 5 characters long!")
            is_valid = False

        # password confirmation validation
        if data["password"] != data["pass_conf"]:
            flash("Password and Password Confirmation must match!!")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        # change owner to user in other projects
        owner_in_db = Owner.get_by_email(data)
        # user is not registered in the db
        if not owner_in_db:
            flash("Invalid Credentials!")
            is_valid = False
        elif not bcrypt.check_password_hash(owner_in_db.password, data["password"]):
            # if we get False after checking the password
            flash("Invalid Credentials!")
            is_valid = False
            
        return is_valid

# owner.get_by_id route
    @classmethod
    def get_by_id(cls, data):
        # try to keep the table as users not owners on exam
        query = "SELECT * FROM owners WHERE id = %(owner_id)s;"
        result = connectToMySQL("petshow_schema").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    # email validation(2) - queries current db to find if email is in use
    @classmethod
    def get_by_email(cls, data):
        # try to keep the table as users not owners on exam
        query = "SELECT * FROM owners WHERE email = %(email)s;"
        result = connectToMySQL("petshow_schema").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    # owner controller - #3 saving new owner to db


    @classmethod
    def create_owner(cls, data):
        query = "INSERT INTO owners (first_name, last_name, email, password, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"
        results = connectToMySQL("petshow_schema").query_db(query, data)
        return results
    