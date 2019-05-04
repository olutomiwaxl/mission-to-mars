from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

#create a new database called mars_db
db = client.mars_db

# Drops collection if available to remove duplicates
db.collection.drop()


@app.route("/")
def home():

    # Find one record of data from the mongo database
    needed_data = db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=needed_data)





# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    db.collection.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
