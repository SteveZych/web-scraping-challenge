from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_costa

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/web_scraping.mission_to_mars")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():




@app.route("/scrape")