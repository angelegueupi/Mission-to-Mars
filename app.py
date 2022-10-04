from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


# use flask pymongonto set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    #access info from database
    mars_data = mongo.db.marsData.find_one()
    #print(mars_data)
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    #ref to a database collection (table)
    marsTable = mongo.db.marsData
    
    # drop the table if exists
    #mongo.db.marsData.drop()
    
    #test to call scrape mars script
    mars_data = scrape_mars.scrape_all()
   # print(mars_data)
    marsTable.update_one({}, {"$set": mars_data}, upsert=True)
    
    # take the dictionary and load it into mongoDB
    #marsTable.insert_one(mars_data)
    
    #print(mars_data) # print the dictionary that is returned from the scrape all script
    return redirect('/', code=302) 

# if __name__ == "__main__":
#     from flask import Flask, render_template, redirect, url_for
# from flask_pymongo import PyMongo
# import scrape_mars

# app = Flask(__name__)


# # use flask pymongonto set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
# mongo = PyMongo(app)

# @app.route("/")
# def index():
#     #access info from database
#     mars_data = mongo.db.marsData.find_one()
#     #print(mars_data)
#     return render_template("index.html", mars=mars_data)

# @app.route("/scrape")
# def scrape():
#     #ref to a database collection (table)
#     marsTable = mongo.db.marsData
    
#     # drop the table if exists
#     #mongo.db.marsData.drop()
    
#     #test to call scrape mars script
#     mars_data = scrape_mars.scrape_all()
#    # print(mars_data)
#     marsTable.update_one({}, {"$set": mars_data}, upsert=True)
    
#     # take the dictionary and load it into mongoDB
#     #marsTable.insert_one(mars_data)
    
#     #print(mars_data) # print the dictionary that is returned from the scrape all script
#     return mars_data #redirect('/', code=302) #mars_data

if __name__ == "__main__":
    app.run()