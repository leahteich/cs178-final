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
    if request.method == 'GET':
        response = requests.get("https://api.cs50.io/dining/menus", {"date": "2023-04-25", "location": 8, "meal": 1})
    else: 
        my_dhall = request.form.get("dhalls")
        my_date = request.form.get("datepick")
        print(my_dhall)
        response = requests.get("https://api.cs50.io/dining/menus", {"date": my_date, "location": my_dhall, "meal": 1})
    menu = response.json()
    menu_items = []
    for item in menu: 
        if item['recipe'] in recipes: 
            recipe = recipes[item['recipe']]
        recipe['category'] = item['category']
        menu_items.append(recipe)
    return render_template("index.html", menu=menu_items, locations=locations)