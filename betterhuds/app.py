# -- Import section --
from flask import render_template, request, Flask, jsonify
from categories import categories_wanted, recipes, locations
import requests
from multiprocessing import Pool
import datetime
import sqlite3
from sqlite3 import Error

# -- Initialization section --
app = Flask(__name__)


def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect(':memory:')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


# -- Routes section --
@app.route("/times")
def times():
    return render_template("times.html")


@app.route("/favs")
def favs():
    fav_items = []
    ew_items = []
    for item in recipes: 
        if (recipes[item]["upvotes"] != None) and (recipes[item]["downvotes"] != None):
            if (recipes[item]["upvotes"] - recipes[item]["downvotes"] > 0):
                fav_items.append((recipes[item]['name'], recipes[item]["upvotes"] - recipes[item]["downvotes"]))
            elif (recipes[item]["upvotes"] - recipes[item]["downvotes"] < 0):
                ew_items.append((recipes[item]['name'], recipes[item]["upvotes"] - recipes[item]["downvotes"] ))
    fav_items.sort(key = lambda x: x[1],reverse=True)
    ew_items.sort(key = lambda x: x[1])
    print(fav_items)
    return render_template("favs.html", favs=fav_items, notfavs=ew_items)


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
    
    return render_template("index.html", menu_lunch=menu_items_lunch,menu_breakfast=menu_items_breakfast,menu_dinner=menu_items_dinner, 
                           locations=locations, loc=dining_hall, date=date, date_string=date_string)

# Help from ChatGPT and TF Felix
# Rate (state): upvoted, downvoted, unrated
# Rate (action): upvote(item), downvote(item) 
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

if __name__ == '__main__':
    create_connection(r"pythonsqlite.db")
