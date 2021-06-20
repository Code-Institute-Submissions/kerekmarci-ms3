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

# Pagination
# Pagination help found: https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
# and here: https://betterprogramming.pub/simple-flask-pagination-example-4190b12c2e2e
# flask_paginate documentation: https://flask-paginate.readthedocs.io/_/downloads/en/master/pdf/

PER_PAGE = 6


def paginate(recipes):
    page, _, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    offset = page * PER_PAGE - PER_PAGE

    return recipes[offset: offset + PER_PAGE]


def pagination_args(recipes):
    page, _, _ = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    total = len(recipes)

    return Pagination(page=page, per_page=PER_PAGE, total=total,
                      css_framework='bootstrap4')


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    categories = list(mongo.db.categories.find())
    total = mongo.db.recipes.find().count()
    recipes = list(mongo.db.recipes.find())
    recipes_paginated = paginate(recipes)
    pagination = pagination_args(recipes)

    return render_template("get_recipes.html", recipes=recipes_paginated,
                           pagination=pagination)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    total = mongo.db.recipes.find().count()
    recipes_paginated = paginate(recipes)
    pagination = pagination_args(recipes)
    return render_template("get_recipes.html", recipes=recipes_paginated,
                           pagination=pagination)


@app.route("/search/<category>")
def food_category(category):
    level = request.args.get('level')

    recipes = list(mongo.db.recipes.find(
        {"recipe_cagetory": category}))

    if level != None:
        recipes_new = []
        for recipe in recipes:
            if level.lower() in recipe['level'].lower():
                recipes_new.append(recipe)

        recipes = recipes_new

    total = mongo.db.recipes.find().count()
    recipes_paginated = paginate(recipes)
    pagination = pagination_args(recipes)
    return render_template("get_recipes.html", recipes=recipes_paginated,
                           pagination=pagination, level=level, category=category)


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
    return redirect(url_for("get_recipes"))


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
        return redirect(url_for("get_recipes"))

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


@app.route("/recipe/<recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    recipe = mongo.db.recipes.find_one(
        {"_id": ObjectId(recipe_id)})

    comments = mongo.db.comments.find(
        {"recipe_id": recipe_id})

    if request.method == "POST":
        timestamp = datetime.now().strftime('%d-%m-%Y')
        review = {
            "recipe_id": recipe_id,
            "created_by_username": session["user"],
            "created_by_name": session["name"],
            "date": timestamp,
            "comment": request.form.get("comment")
        }
        mongo.db.comments.insert_one(review)

    return render_template("recipe.html", 
            recipe=recipe, comments=comments)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("get_tasks"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)