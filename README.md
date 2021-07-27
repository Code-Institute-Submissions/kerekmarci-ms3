# Epic Food Receipe Website - Milestone Project 3

## View live project here: [Epic Food](http://epic-food.herokuapp.com/)

This website was created for my 3rd Milestone Project at the Code Institute. 
The website will utilise the languages and tools I learned so far in Front-End and Back-End, namely HTML, CSS, JavaScript, Python+Flask, MongoDB.

---

## Description

This project presents a web application that allows users to store and easily access cooking recipes.
A visitor can view and access various receipes based on meal types, while a registered user will have access to more functionalities, such as
uploading recipes, amending and deleting their own recipes, as well as leaving comments on recipes.

---

## User Experience

The aim of this website is to display recipes in a visually appealing and user friendly manner.
Upon loading the page, the navigation bar is present at ta fixed position, highlighting the registration button which is the main goal of the website.
Once the user registers, all features are revealed. Below that, the meal types are shown with eye-catching images, and the recipe cards are loaded below on the main landing page. It is intuitive for the user to click on the recipe (either the name or the image) to access full details.

### Strategy

The main goal of this 3rd Milestone project was to build a website that has both Front-End and Back-End elements and can manipulate data with CRUD operations. Within that, the aim was to create an application that allows users to register to the website, upload, amend and delete recipes, as well as able to browse within recipes while displaying results in a visually appealing way.

### User stories:

As a user...,

* I would like to be able to have a quick and easy access to recipes
* I would like to filter recipes by meal types and keywords
* I would like to easily find recipes on various cooking levels
* I would like to be part of the website by being able to register and upload recipes
* I would like to be part of the community by being able to leave my comments on recipes
* I would like to see a website that displays well on various devices, such as desktop and mobile devices
* I would like easy navigation between pages

As a site owner...,

* I would like to have useful recipes presented in a pleasing way that encourages users to revisit the website and try out recipes
* I would like to encourage users to return to the website by allowing them to be part of the community, such as uploading and commenting recipes
* I would like to promote cooking tools. The more returning users I have, the more changes that users click on the cooking tools and purchase them

### Scope

The key features of this web application is to be able to manage CRUD operations in MongoDB database:

* **Create:** registered users can upload recipes and comments to the database that can be viewed by others
* **Read:** to view data (recipes) uploaded in MongoDB, with having various options to filter data and display the selected result. Such filters are search by category, search by cooking level and search by keywords
* **Update:** registered users can make changes to any of their own recipes
* **Delete:** registered users can delete their own recipes

### Structure

The website will feature the following:

#### Main Page: 

* Banner on the top of the page with the logo of the website
* Navigation under the logo that has 2 parts: menu bar with text menu and search by meal types with icons
* 6 recipe cards shown with pagination - clicking on the recipes will land on the full individual recipe page
* Section to promote cooking equipment
* Footer

#### Registration Page:

* Allowing users to sign up to the website. Registered users have access to more features.

#### Login Page:

* Registered users can log in by entering their username and password.

#### Upload Recipe Page (Resistered Users):

* Registered users can upload a recipe. On this page, they can provide the title of the recipe, a brief description, food category, cooking level, number of servings, preparation time, cooking time, list of ingredients, recipe method and a photo of the ready meal.

#### My Recipes Page (Resistered Users):

* On this page, registered users can access the collection of the recipes uploaded by themselves.

#### Favourites Page (Resistered Users):

* Users can access to the recipes that they have added to their collection of favourites.

#### Profile Page (Resistered Users):

* Registered users can view their information and some basic statistics. On this page, their name, username and profile picture are displayed, as well as how many recipes the user has uploaded and how many they have added to their favourites. Users can also change their profile picture if they wish.

#### Statistics Page (Resistered Users):

* On this page, the total number of recipes are shown that are available on the website, as well as the total number of comments left by the community. Furthermore, there are two MongoDB charts that presents a summary on chart: a pie chart displaying the distribution of recipes by meal type, and a bar chart showing the total amount of recipes uploaded by users.

### Skeleton

The skeleton of the website is available in the below wireframes:

1. [Index Page](https://github.com/kerekmarci/ms3/blob/master/documentation/wireframes/landing_page.png)
2. [Upload Recipe Page](https://github.com/kerekmarci/ms3/blob/master/documentation/wireframes/upload_recipe.png)
3. [Full Recipe Page](https://github.com/kerekmarci/ms3/blob/master/documentation/wireframes/recipe_page.png)

### Surface

* **Planning of layout:**

xxx

* **Theme:**

xxx

* **Colours:**

The colour palette can be seen here.\

* **Typography:**

xxx

* **Icons:**

xxx

---

## Features

* Database: a database to store all recipes (this is the main purpose of the website)
* Registration: users can create an account
* Login: users with an account can upload, modify and delete their own recipes
* Profile page: users can review their name, username, password and profile picture
* Navbar
* Responsive
* More menu elements available if user is registered
* Full recipe page for each dish
* Comment: users are able to comment a recipe
* Recipe filter function to filter by: difficulty level, type of dish (starter, main, side)
* Text search function to search in a recipe
* Upload a recipe (registered users)
* Manage recipes: once logged in, users can edit or delete their own recipes
* Pagination to limit the number of recipes per page
* Dashboard to provide statistics about recipes 

## Structure of the menu

### For All Users (without resitration)

* Home
* Log In
* Register

### For Registered Users:

* Home
* Statistics
* Upload Recipe
* My Recipes
* Profile
* Log Out

### For Admin (same as registered, plus):

* Dashboard (to manage all recipes)
* Manage Categories

## Database Schema

### Users:

* name
* username: string
* password: string
* email: string
* profile picture:
* is_admin: Boolean

### Recipe:

* Name
* Category
* Level (Easy/Medium/Hard)
* Servings
* Vegetarian (Boolean) 
* Preparation time
* Cooking Time
* Ingredients
* Recipe Method
* Image
___

* Uploaded On (date)
* Uploaded By (username’s name)
* Comments
