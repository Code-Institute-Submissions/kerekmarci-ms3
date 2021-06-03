# Epic Food Receipe Website - Milestone Project 3

## View live project here: [Epic Food](https://kerekmarci.github.io/ms3/)

This website was created for my 3rd Milestone Project at the Code Institute. 
The website will utilise the languages and tools I learned so far, both in Front-End and Back-End.

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
