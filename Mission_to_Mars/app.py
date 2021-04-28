from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create Flask Instance
app = Flask(__name__)

# Pymongo to make connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route index.html
@app.route("/")
def index():

    # Find one record from mongo
    mars = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars=mars)


# Route the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    # Back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)