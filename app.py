import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args, get_page_parameter
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Configuring Cloudinary
# https://pypi.org/project/cloudinary/
cloudinary.config(
  cloud_name = os.environ.get("CLOUDINARY_NAME"),
  api_key = os.environ.get("CLOUD_API_KEY"),
  api_secret = os.environ.get("CLOUD_API_SECRET_KEY")
)

PER_PAGE = 6

mongo = PyMongo(app)

# Pagination
# Pagination help found: https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
# and here: https://betterprogramming.pub/simple-flask-pagination-example-4190b12c2e2e
# flask_paginate documentation: https://flask-paginate.readthedocs.io/_/downloads/en/master/pdf/


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
    users = list(mongo.db.users.find())
    recipes_paginated = paginate(recipes)
    pagination = pagination_args(recipes)

    return render_template("get_recipes.html", recipes=recipes_paginated,
                           pagination=pagination,
                           users=users)


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

    """
    if level != None:
        recipes_new = []
        for recipe in recipes:
            if level.lower() in recipe['level'].lower():
                recipes_new.append(recipe)

        recipes = recipes_new
    """
    if category == "Vegetarian":
        recipes = list(mongo.db.recipes.find(
            {"vegetarian": "veg"}))
    else:
        recipes = list(mongo.db.recipes.find(
            {"recipe_cagetory": category}))

    total = mongo.db.recipes.find().count()
    recipes_paginated = paginate(recipes)
    pagination = pagination_args(recipes)
    return render_template("get_recipes.html", recipes=recipes_paginated,
                           pagination=pagination, level=level, category=category)


@app.route("/my_recipes")
def my_recipes():    
    if session.get("user"):          
        user = mongo.db.users.find_one(
            {"username": session["user"]})
        recipes = list(mongo.db.recipes.find(
            {"uploaded_by": session["user"]}))

    return render_template("my_recipes.html", recipes=recipes,
                                            user=user)


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

    return render_template("profile.html")


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

    
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
        timestamp = datetime.now().strftime('%d-%m-%Y')

        file_to_upload = request.files['file']
        recipe_picture_url = "https://img.pngio.com/restaurant-svg-dinner-clipart-kitchen-svg-food-png-silhouette-etsy-food-png-silhouette-2048_1536.jpg"
        if file_to_upload:            
            upload_result = cloudinary.uploader.upload(file_to_upload, 
                folder="recipe-images")
            recipe_picture_url = upload_result["url"]            

        recipe = {
            "recipe_name": request.form.get("recipename"),
            "description": request.form.get("description"),
            "recipe_cagetory": request.form.get("recipe-category"),
            "level": request.form.get("level"),
            "servings": request.form.get("servings"),
            "vegetarian": is_vegetarian,
            "preptime": request.form.get("preptime"),
            "cooktime": request.form.get("cooktime"),
            "ingredients": request.form.getlist("ingredients"),
            "recipe_method": request.form.getlist("method"),
            "recipe_picture": recipe_picture_url,
            "uploaded_on": timestamp,
            "uploaded_by": session["user"],
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

        file_to_upload = request.files['file']
        recipe_picture_url = mongo.db.recipes.find_one({
            "_id": ObjectId(recipe_id)})["recipe_picture"]
        if file_to_upload:            
            upload_result = cloudinary.uploader.upload(file_to_upload, 
                folder="recipe-images")
            recipe_picture_url = upload_result["url"]  

        edited_recipe = {
            "recipe_name": request.form.get("recipename"),
            "description": request.form.get("description"),
            "recipe_cagetory": request.form.get("recipe-category"),
            "level": request.form.get("level"),
            "servings": request.form.get("servings"),
            "vegetarian": is_vegetarian,
            "preptime": request.form.get("preptime"),
            "cooktime": request.form.get("cooktime"),
            "ingredients": request.form.getlist("ingredients"),
            "recipe_method": request.form.getlist("method"),
            "recipe_picture": recipe_picture_url            
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, {"$set": edited_recipe})
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
    users = list(mongo.db.users.find())

    if request.method == "POST":
        timestamp = datetime.now().strftime('%d-%m-%Y')
        new_comment = {
            "recipe_id": recipe_id,
            "created_by_username": session["user"],
            "created_by_name": session["name"],
            "date": timestamp,
            "comment": request.form.get("comment")
        }
        mongo.db.comments.insert_one(new_comment)

    return render_template("recipe.html", 
            recipe=recipe, comments=comments,
            users=users)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("my_recipes"))


@app.route("/add_favorite/<recipe_id>")
def add_favorite(recipe_id):
    username = session["user"]
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    # Push this receipe to the user's favourite recipe array    
    mongo.db.recipes.update_one(recipe, {"$push": {"favorited_by": username}})    
    flash("Recipe Successfully Added to Favourites")

    return redirect(url_for("favorite_recipes"))


@app.route("/remove_favorite/<recipe_id>")
def remove_favorite(recipe_id):
    username = session["user"]
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    mongo.db.recipes.update_one(recipe, {"$pull": {"favorited_by": username}})    
    flash("Recipe Successfully Added to Favourites")

    return redirect(url_for("favorite_recipes"))


@app.route("/favorite_recipes")
def favorite_recipes():
    if session.get("user"):          
        user = mongo.db.users.find_one(
            {"username": session["user"]})
    
    recipes = list(mongo.db.recipes.find())   
    
    return render_template("favorites.html", recipes=recipes,
                                            user=user)

# Based on Cloudinary documentation
# https://cloudinary.com/documentation/django_image_and_video_upload#server_side_upload
@app.route("/'upload_profile_image", methods=["GET", "POST"])
def upload_profile_image():
    if request.method == "POST":
        file_to_upload = request.files['file']        
        if file_to_upload:            
            upload_result = cloudinary.uploader.upload(file_to_upload, 
                folder="profile-images")
            profile_picture_url = upload_result["url"]
            mongo.db.users.update_one({"username": session["user"]}, {
                                        "$set": {"profile_picture": profile_picture_url}})
            
    return redirect(url_for("profile", username=session["user"]))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)