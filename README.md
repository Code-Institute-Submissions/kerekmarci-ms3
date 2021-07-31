# Epic Food Recipe Website - Milestone Project 3

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

#### Upload Recipe Page (Registered Users):

* Registered users can upload a recipe. On this page, they can provide the title of the recipe, a brief description, food category, cooking level, number of servings, preparation time, cooking time, list of ingredients, recipe method and a photo of the ready meal.

#### My Recipes Page (Registered Users):

* On this page, registered users can access the collection of the recipes uploaded by themselves.

#### Favourites Page (Registered Users):

* Users can access to the recipes that they have added to their collection of favourites.

#### Profile Page (Registered Users):

* Registered users can view their information and some basic statistics. On this page, their name, username and profile picture are displayed, as well as how many recipes the user has uploaded and how many they have added to their favourites. Users can also change their profile picture if they wish.

#### Statistics Page (Registered Users):

* On this page, the total number of recipes are shown that are available on the website, as well as the total number of comments left by the community. Furthermore, there are two MongoDB charts that presents a summary on chart: a pie chart displaying the distribution of recipes by meal type, and a bar chart showing the total amount of recipes uploaded by users.

### Skeleton

The skeleton of the website is designed with the wireframes below:

1. [Index Page](https://github.com/kerekmarci/ms3/blob/master/documentation/wireframes/landing_page.png)
2. [Upload Recipe Page](https://github.com/kerekmarci/ms3/blob/master/documentation/wireframes/upload_recipe.png)
3. [Full Recipe Page](https://github.com/kerekmarci/ms3/blob/master/documentation/wireframes/recipe_page.png)
4. [Registration Page](https://github.com/kerekmarci/ms3/blob/master/documentation/wireframes/registration_page.png)
4. [Login Page](https://github.com/kerekmarci/ms3/blob/master/documentation/wireframes/login_page.png)

### Surface

* **Colours:**

For a website that contains a database, I believe that a brigther scheme is more suitable than a dark one.
Being a recipe website, a food-related banner on the top of the page will immediately create a feeling in the user what the entire website is about. This is why an image was selected which is showing some ingredients. A green colour in the theme is a suitable match with the ingredients and food in overall, and brown and orange go well with green. This is why the main colour of the banner is brown, and the various highlights and buttons are either green or orange. The overall white and grey background is neutral and is a good match with any colours.\
The colour palette can be seen here.\
\
![Colour palette](https://github.com/kerekmarci/ms3/blob/master/documentation/images/color_palette.JPG)

* **Typography:**

For the text content of the website, traditional-looking fonts were selected that are easy to read.  
    - The main font is called *Barlow*. This is a suitable font for both the content and a headlines, with a heavier font-weight for the latter.  
    - To add a little flavour to the titles, the friendly one-liners on the top of each sections are written with a fond called  *Handlee*  

* **Icons:**

FontAwesome icons are used on the recipe cards and on the full recipe pages to add more visual element to the categories, cooking time and number of servings.

---

## Features

* **Database:** a database to store all recipes (this is the main purpose of the website).
* **Registration:** users can create an account to gain access to more functionalities.
* **Login:** users with an account can upload, modify and delete their own recipes, as well as comment any recipes.
* **Profile page:** users can review their name, username and profile picture, as well as a quick stats on how many recipes they uploaded and favourited.
* **Search functionality:** uses can select recipes with keywords that will search in the recipe name and description. Users can also select recipes based on meal type, in combination with cooking level.
* **Card views:** Recipes are loaded in card views. Each card leads to the full recipe page with detailed information for that particular recipe.
* **Comment:** registered users are able to comment any recipes.
* **Upload a recipe:** registered users can upload a recipe with detailed information that is required to prepare that meal.
* **Edit a recipe:** registered users can make changes on the recipes uploaded by them.
* **Delete a recipe:** registered users can delete their own recipes. Deletion needs to be confirmed in a pop-up modal.
* **Favourites:** registered users can add recipes to their favourites collection
* **Statistics:** registered users can see statistics on the recipes, such as the total number of recipes in the database and a visual chart on the meal categories
* **Pagination:** when recipe cards are loaded, 6 cards are shown per page, and users can navigate between pages on a pagination tab
* **Photo Upload:** Users can upload images of the ready food for the recipes, as well as uploading an image as their profile picture. Images are handled by *Cloudinary* image-management solution, and the URL is stored in the MongoDB database
* **Responsive:** the website is responsive to desktop, tablet and mobile devices

---

## Structure of the menu

### For All Users (without registration)

* Home
* Log In
* Register

### For Registered Users:

* Home
* Upload Recipes
* My Recipes
* Favourites
* Profile
* Statistics
* Log Out

---

## Database Schema

Data is stored in MongoDB non-relational database, consisting of 4 tables:

### Food Categories:

| Name              | Type      |
| :---              | :---      |
| id                | ObjectID  |
| Category Name     | String    |

![Categories in MongoDB](https://github.com/kerekmarci/ms3/blob/master/documentation/images/mongodb_categories.JPG)

### Users:

| Name              | Type      |
| :---              | :---      |
| id                | ObjectID  |
| Name              | String    |
| Username          | String    |
| Password          | String    |
| Profile Picture   | String    |

![Users in MongoDB](https://github.com/kerekmarci/ms3/blob/master/documentation/images/mongodb_users.jpg)

### Recipe:

| Name              | Type      |
| :---              | :---      |
| id                | ObjectID  |
| Recipe Name       | String    |
| Description       | String    |
| Recipe Category   | String    |
| Level             | String    |
| Servings          | Integer   |
| Preparation Time  | Integer   |
| Cooking Time      | Integer   |
| Ingredients       | Array     |
| Recipe Method     | Array     |
| Recipe Picture    | String    |
| Uploaded On       | Timestamp |
| Uploaded By       | String    |
| Favourited By     | Array     |

![Recipes in MongoDB](https://github.com/kerekmarci/ms3/blob/master/documentation/images/mongodb_recipes.JPG)

### Comments:

| Name              | Type      |
| :---              | :---      |
| id                | ObjectID  |
| Recipe ID         | String    |
| Created by Username | String  |
| Created by Name   | String    |
| Date              | Timestamp |
| Comment           | String    |

![Comments in MongoDB](https://github.com/kerekmarci/ms3/blob/master/documentation/images/mongodb_comments.JPG)

### The relations among the tables can be seen here:

![Relations among database tables](https://github.com/kerekmarci/ms3/blob/master/documentation/images/database_schema.jpg)

---

## Security Features

During the user's journey, there are certain security-related features that have been implemented.

### User Registration

When user creates an account, the username and password are stored in the MongoDB database.
To prevent storing the actual password, the password gets hashed and salted with the help of the *generate_password_hash()* security helper.
This has been imported from Werkzeug Security with the following import command:
*from werkzeug.security import generate_password_hash*

### User Login

The *check_password_hash* security helper from Werkzeug Security is able to check a password against a given salted and hashed password value.
This has been imported from Werkzeug Security with the following import command:
*from werkzeug.security import check_password_hash*

### Defensive Programming

It is a good practice to add a step of confirmation before user can make significant changes with the data.
The best example for this is to prevent the user accidentally deleting a recipe. Therefore, when the user clicks on the *Delete Recipe* button, a prompt alert (modal) appears to reconfirm if the user would indeed like to delete the recipe.

---

## Technologies Used

### Languages

* HTML5
* CSS3
* JavaScript
* Python

### Libraries

* Bootstrap: HTML, CSS and JavaScript library to create modern websites and web apps
* Balsamiq: an industry standard low-fidelity wireframing tool
* Google Fonts: for providing stylish fonts across the website

### Framework

* Flask: micro web framework written in Python, that depends on the Jinja template engine and the Werkzeug WSGI toolkit

### Database

* MongoDB: non-relational database

### Version control

* Github: is used to store all codes
* Gitpod: is used as a IDE and to push code to Github

### Hosting

* Heroku: the web app is hosted on Heroku Cloud Application Platform

---

## Deployment

All necessary code for this web app is stored in *GitHub* repository, and is available to view at https://kerekmarci.github.io/ms3/ \
The full web app is hosted on *Heroku* and can be viewed here: https://epic-food.herokuapp.com/

### Setting up Github

1. As a starting point, I used the base templated provided by The Code Institute: https://github.com/Code-Institute-Org/gitpod-full-template
2. I clicked on the button called *Use this template*
3. Entered a name for my new repository, then clicked on the *Create repository from this template* button. Now the development environment has been created.

### Setting up Environment Variables

Sensitive data needs to be hidden using environment variables in the `env.py` file. Files that should not be pushed to GitHub needs to be added to the `.gitignore` file.
The enviroment variables take two arguments: first the name of the variable, second the data itself, for example `os.environ.setdefault("PORT", "5000")`.
In the *env.py* file, the following variables are set up: *IP, PORT, SECRET_KEY, MONGO_URI, MONGO_DBNAME.* In my project, *Cloudinary* is used to store images, therefore *CLOUDINARY_NAME, CLOUD_API_KEY, CLOUD_API_SECRET_KEY* need to be included too.

### Requirements for Heroku

Heroku needs the *Procfile* and the *Requirements* in order to run the app.
To create the file for the requirements, the following needs to be created: `pip3 freeze --local > requirements.txt"`.
In the *Procfile*, the following line needs to be added so that Heroku will know which file to run: `web: python app.py`.

### Setting up and deploying to Heroku 

As the enviroment variables contained in the *env.py* file will not be pushed, therefore these variables need to be configured directly in Heroku.
Once a Heroku app has been created, under the *Settings* tab, the variables can be entered by clicking on the *Reveal Config Vars* button.

To automatically deploy code to Heroku from Github, in the *Deployment method* in Heroku, the *GitHub* icon needs to be selected. Then, the name of the GitHub repository needs to be entered and automatic deployment can be enabled.

### Cloning

To clone the GitHub repository, follow these steps:\  

1. Go to my GitHub repository - https://github.com/kerekmarci/ms3
2. Click on the CODE button
3. Copy the link with the HTTPS option selected
4. Open your IDE
5. Type git clone in the terminal, followed by pasting the link. For example: *git clone https://github.com/kerekmarci/ms3.git*
6. Press Enter, and now a local clone has been created