# All the imports
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import pymongo
import scrape_mars

app = Flask(__name__)

# Connects to MongoDB 
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

database = client.MissionToMars
column = database.MarsData

@app.route("/")
def index():

    # Display the information from the Mongo DB
    mars_data = client.db.MissionToMars.find_one()
    # Renders the HTML page
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
# Function calls on the scrape_mars python file and executes the whole thing, returns the values on the /scrape page
def scrape():

    # Drop the Mongo table if it exists
    client.drop_database('MissionToMars')

    # Stores the scraped data as a dictionary
    mars_data = scrape_mars.scrape_all()

    # Inserts the scraped data to a Mongo DB
    column.insert_one(mars_data)

    # Go back to the index page
    return redirect('/')



# Setup Flask
if __name__ == "__main__":
    app.run()