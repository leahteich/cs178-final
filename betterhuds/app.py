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
from flask import jsonify
import datetime

# -- Initialization section --
app = Flask(__name__)

# --- Setting up Mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)


@app.route("/times")
def times():
    return render_template("times.html")

# -- Routes section --
@app.route("/")
@app.route("/index", methods=['GET','POST'])
def index():
    menu_items_breakfast = []
    menu_items_lunch = []
    menu_items_dinner = []
    dining_hall = ""
    date = ""
    date_unformatted = None
    if request.method == 'POST':
        my_dhall = int(request.form.get("dhalls"))
        datetimeobj = datetime.datetime.strptime(request.form.get("datepick"), "%Y-%m-%d")
        date_formatted = datetimeobj.strftime('%Y-%m-%d')
        date_unformatted = datetimeobj
        response_breakfast = requests.get("https://api.cs50.io/dining/menus", {"date": date_formatted, "location": my_dhall, "meal": 0})
        response_lunch = requests.get("https://api.cs50.io/dining/menus", {"date": date_formatted, "location": my_dhall, "meal": 1})
        response_dinner = requests.get("https://api.cs50.io/dining/menus", {"date": date_formatted, "location": my_dhall, "meal": 2})            
        dining_hall = my_dhall
        date = date_formatted
    else: 
        today = datetime.date.today()
        date_unformatted = today
        today_formatted = today.strftime('%Y-%m-%d')
        response_breakfast = requests.get("https://api.cs50.io/dining/menus", {"date": today_formatted, "location": 8, "meal": 0})
        response_lunch = requests.get("https://api.cs50.io/dining/menus", {"date": today_formatted, "location": 8, "meal": 1})
        response_dinner = requests.get("https://api.cs50.io/dining/menus", {"date": today_formatted, "location": 8, "meal": 2})
        dining_hall = 8
        date = today

    date_string = date_unformatted.strftime('%A') + ", "+ date_unformatted.strftime('%B') + " " + date_unformatted.strftime('%-d')

    menu_breakfast = response_breakfast.json()
    menu_items_breakfast = []
    for item in menu_breakfast: 
        if item['recipe'] in recipes: 
            recipe = recipes[item['recipe']]
        recipe['category'] = item['category']
        recipe['id'] = item['recipe']
        if not recipe in menu_items_breakfast:
            menu_items_breakfast.append(recipe)
    
    menu_lunch = response_lunch.json()
    menu_items_lunch = []
    for item in menu_lunch: 
        if item['recipe'] in recipes: 
            recipe = recipes[item['recipe']]
        recipe['category'] = item['category']
        recipe['id'] = item['recipe']
        if not recipe in menu_items_lunch:
            menu_items_lunch.append(recipe)
    
    menu_dinner = response_dinner.json()
    menu_items_dinner = []
    for item in menu_dinner: 
        if item['recipe'] in recipes: 
            recipe = recipes[item['recipe']]
        recipe['category'] = item['category']
        recipe['id'] = item['recipe']
        if not recipe in menu_items_dinner:
            menu_items_dinner.append(recipe)
    
    # print(menu_items_dinner)

    return render_template("index.html", menu_lunch=menu_items_lunch,menu_breakfast=menu_items_breakfast,menu_dinner=menu_items_dinner, 
                           locations=locations, loc=dining_hall, date=date, date_string=date_string)

@app.route('/api/upvote/<item_id>', methods=['POST'])
def upvote(item_id):
    item_id = int(item_id)
    recipes[item_id]['upvotes'] += 1
    return jsonify(recipes[item_id])

@app.route('/api/downvote/<item_id>', methods=['POST'])
def downvote(item_id):
    item_id = int(item_id)
    recipes[item_id]['downvotes'] += 1
    return jsonify(recipes[item_id])
