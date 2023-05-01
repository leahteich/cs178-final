# ---- YOUR APP STARTS HERE ----
# -- Import section --
# Help from ChatGPT setting up Mongo for Flask
from flask import Flask
from flask_pymongo import PyMongo
from flask import render_template
from flask import request
from categories import categories_wanted, recipes, locations
import requests
from multiprocessing import Pool

# -- Initialization section --
app = Flask(__name__)

# --- Setting up Mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)


# -- Routes section --
@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index():
    menu_items_breakfast = []
    menu_items_lunch = []
    menu_items_dinner = []
    dining_hall = ""
    date = ""
    if request.method == 'POST':
        my_dhall = int(request.form.get("dhalls"))
        my_date = request.form.get("datepick")
        response_breakfast = requests.get("https://api.cs50.io/dining/menus", {"date": my_date, "location": my_dhall, "meal": 0})
        response_lunch = requests.get("https://api.cs50.io/dining/menus", {"date": my_date, "location": my_dhall, "meal": 1})
        response_dinner = requests.get("https://api.cs50.io/dining/menus", {"date": my_date, "location": my_dhall, "meal": 2})
        dining_hall = my_dhall
        date = my_date
    else: 
        response_breakfast = requests.get("https://api.cs50.io/dining/menus", {"date": "2023-05-02", "location": 8, "meal": 0})
        response_lunch = requests.get("https://api.cs50.io/dining/menus", {"date": "2023-05-02", "location": 8, "meal": 1})
        response_dinner = requests.get("https://api.cs50.io/dining/menus", {"date": "2023-05-02", "location": 8, "meal": 2})
        dining_hall = 8
        date = "2023-05-02"
    menu_breakfast = response_breakfast.json()
    menu_items_breakfast = []
    for item in menu_breakfast: 
        if item['recipe'] in recipes: 
            recipe = recipes[item['recipe']]
        recipe['category'] = item['category']
        menu_items_breakfast.append(recipe)
    
    menu_lunch = response_lunch.json()
    menu_items_lunch = []
    for item in menu_lunch: 
        if item['recipe'] in recipes: 
            recipe = recipes[item['recipe']]
        recipe['category'] = item['category']
        menu_items_lunch.append(recipe)
    
    menu_dinner = response_dinner.json()
    menu_items_dinner = []
    for item in menu_dinner: 
        if item['recipe'] in recipes: 
            recipe = recipes[item['recipe']]
        recipe['category'] = item['category']
        menu_items_dinner.append(recipe)


    return render_template("index.html", menu_lunch=menu_items_lunch,menu_breakfast=menu_items_breakfast,menu_dinner=menu_items_dinner, locations=locations, loc=dining_hall, date=date)