# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from categories import categories_wanted, recipes, locations
import requests
from multiprocessing import Pool

# -- Initialization section --
app = Flask(__name__)


# -- Routes section --
@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index():
    if request.method == 'GET':
        response = requests.get("https://api.cs50.io/dining/menus", {"date": "2023-04-23", "location": 8, "meal": 1})
        menu = response.json()
        menu_items = []
        for item in menu: 
            recipe = recipes[item['recipe']]
            recipe['category'] = item['category']
            menu_items.append(recipe)
        return render_template("index.html", menu=menu_items, locations=locations)
    else:
        my_dhall = request.form.get("dhalls")
        my_date = request.form.get("datepick")
        my_meal = request.form.get("meals")
        # print(my_dhall)
        # print(locations[5])
        response = requests.get("https://api.cs50.io/dining/menus", {"date": my_date, "location": my_dhall, "meal": my_meal})
        menu = response.json()
        menu_items = []
        for item in menu: 
            recipe = recipes[item['recipe']]
            recipe['category'] = item['category']
            menu_items.append(recipe)
        return render_template("index.html", menu=menu_items, locations=locations)