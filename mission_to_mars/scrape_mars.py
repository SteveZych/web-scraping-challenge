from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def scrape_info():

    # Set up splinter for article title and paragraph
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Uses splinter to interact with the html page for Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    #List to hold Mars news title and paragraph
    marsNews = []

    #div for articles
    newsContent = soup.find_all('div', class_='list_text')

    #Find title and paragraph, store in dictionary, append dictionary to news list
    for news in newsContent:
        title_paragraph = {}
        newsTitle = news.find('div', class_='content_title').text
        newsParagraph = news.find('div', class_='article_teaser_body').text
    
        title_paragraph["Title"] = newsTitle
        title_paragraph["Paragraph"] = newsParagraph
    
        marsNews.append(title_paragraph)    
    
    # Find featured Mars image url
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    full_image_elem = browser.find_by_css('a.showimg').first
    full_image_elem.click()
    img = browser.find_by_tag('img')
    featured_img_url = img['src']

    #Scrape for mars information using pandas
    marsTable = pd.read_html('https://space-facts.com/mars/')[0]
    marsTable.columns = ["Description", "Mars"]
    marsTable.set_index("Description", inplace=True)
    marsTable.to_html()

    #Scrape to find Mars hemispheres with image link and title
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)

    hemisphere_img_title = []

    links = browser.find_by_css("a.product-item h3")

    for l in range(len(links)):
        hemisphere = {}
    
        browser.find_by_css("a.product-item h3")[l].click()
   
        imgLink = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = imgLink['href']
    
        hemisphere['title'] = browser.find_by_css("h2.title").text
    
        hemisphere_img_title.append(hemisphere)
    
        browser.back()