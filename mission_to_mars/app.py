from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/web_scraping")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars = mongo.db.mission_to_mars.find_one()
    return render_template('index.html', mars=mars)

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()

    mongo.db.mission_to_mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)