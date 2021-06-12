import os
from flask import (
    Flask, flash, render_template, redirect, 
    request, session, url_for)
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args, get_page_parameter
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    recipes = list(mongo.db.recipes.find())
    return render_template("home.html", recipes=recipes)


users = list(range(100))
 
 
def get_users(offset=0, per_page=2):
    return users[offset: offset + per_page]


@app.route("/get_recipes")
def get_recipes():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(users)
    pagination_users = get_users(offset=offset, per_page=per_page)                      
    recipes = list(mongo.db.recipes.find())    
    page = request.args.get(get_page_parameter(), type=int, default=1)      
    # total = mongo.db.recipes.find().count()  
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template("get_recipes.html", recipes=recipes, 
                                            users=pagination_users,
                                            pagination=pagination,
                                            page=page,
                                            per_page=per_page)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("get_recipes.html", recipes=recipes)


@app.route("/my_recipes")
def my_recipes():
    recipes = list(mongo.db.recipes.find(
        {"uploaded_by": session["user"]}
    ))
    return render_template("my_recipes.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():    
    if request.method == "POST":
        # Check if username already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "name": request.form.get("name"),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),            
            "profile_picture": request.form.get("profile_picture")
        }

        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie        
        session["user"] = request.form.get("username").lower()
        session["name"] = request.form.get("name")
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if user exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            # check if password matches
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    session["name"] = mongo.db.users.find_one(
                        {"username": session["user"]})["name"]
                    flash("Welcome, {}".format(
                        session["name"]))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password
                flash("Incorrect Username or Password, please try again!")
                return redirect(url_for("login"))
        else:
            # username does not exist
            flash("Incorrect Username or Password, please try again!")
            return redirect(url_for("login"))
    
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):    
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    name = mongo.db.users.find_one(
        {"username": session["user"]})["name"]
    profile_picture = mongo.db.users.find_one(
        {"username": session["user"]})["profile_picture"]    
    
    if session["user"]:
        return render_template("profile.html",
                                username=username,
                                name=name,
                                profile_picture=profile_picture)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been successfully logged out!")
    session.pop("user")
    session.pop("name")
    return redirect(url_for("home"))


@app.route("/upload_recipe", methods=["GET", "POST"])
def upload_recipe():
    if request.method == "POST":
        is_vegetarian = "veg" if request.form.get("vegetarian") else "nonveg"
        ingredient_list, method_list = ([] for i in range(2))
        ingredients = request.form.getlist("ingredients")
        methods = request.form.getlist("method")
        for ingredient, method in zip(ingredients, methods):
            ingredient_list.append(ingredient)        
            method_list.append(method)        
        timestamp = datetime.now().strftime('%d-%m-%Y')
        recipe = {
            "recipe_name": request.form.get("recipename"),
            "description": request.form.get("description"),
            "recipe_cagetory": request.form.get("recipe-category"),
            "level": request.form.get("level"),
            "servings": request.form.get("servings"),
            "vegetarian": is_vegetarian,
            "preptime": request.form.get("preptime"),
            "cooktime": request.form.get("cooktime"),
            "ingredients": ingredient_list,
            "recipe_method": method_list,
            "recipe_picture": request.form.get("recipe_picture"),
            "uploaded_on": timestamp,
            "uploaded_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe has been successfully added!")
        return redirect(url_for("home"))

    categories = list(mongo.db.categories.find())
    return render_template("upload_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        is_vegetarian = "veg" if request.form.get("vegetarian") else "nonveg"
        ingredient_list, method_list = ([] for i in range(2))
        ingredients = request.form.getlist("ingredients")
        methods = request.form.getlist("method")
        for ingredient, method in zip(ingredients, methods):
            ingredient_list.append(ingredient)        
            method_list.append(method)        
        timestamp = datetime.now().strftime('%d-%m-%Y')
        recipe = {
            "recipe_name": request.form.get("recipename"),
            "description": request.form.get("description"),
            "recipe_cagetory": request.form.get("recipe-category"),
            "level": request.form.get("level"),
            "servings": request.form.get("servings"),
            "vegetarian": is_vegetarian,
            "preptime": request.form.get("preptime"),
            "cooktime": request.form.get("cooktime"),
            "ingredients": ingredient_list,
            "recipe_method": method_list,
            "recipe_picture": request.form.get("recipe_picture"),
            "uploaded_on": timestamp,
            "uploaded_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, recipe)
        flash("Recipe has been successfully updated!")
        return redirect(url_for("my_recipes"))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})    
    categories = list(mongo.db.categories.find())
    return render_template("edit_recipe.html", categories=categories, recipe=recipe)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(task_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("get_tasks"))


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    recipe = mongo.db.recipes.find_one(
        {"_id": ObjectId(recipe_id)})

    return render_template("recipe.html", recipe=recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)