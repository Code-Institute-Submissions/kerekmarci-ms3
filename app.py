import os
from flask import (
    Flask, flash, render_template, redirect, 
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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
    return render_template("home.html")


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
        ingredient_list = []
        ingredients = request.form.getlist("ingredients")
        for ingredient in ingredients:
            ingredient_list.append(ingredient)
        method_list = []
        methods = request.form.getlist("method")
        for method in methods:
            method_list.append(method)
        recipe = {
            "recipe_name": request.form.get("recipename"),
            "recipe_cagetory": request.form.get("recipe-category"),
            "level": request.form.get("level"),
            "servings": request.form.get("servings"),
            "vegetarian": request.form.get("vegetarian"),
            "preptime": request.form.get("preptime"),
            "cooktime": request.form.get("cooktime"),
            "ingredients": ingredient_list,
            "recipe_method": method_list,
            "recipe_picture": request.form.get("recipe_picture")
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe has been successfully added!")
        return redirect(url_for("home"))

    categories = list(mongo.db.categories.find())
    return render_template("upload_recipe.html", categories=categories)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)