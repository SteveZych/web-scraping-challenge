from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_info():

    # Set up splinter for article title and paragraph
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    newsTitle, newsParagraph = marsNews(browser)

    data = {
        'newsTitle': newsTitle,
        'newsParagraph': newsParagraph,
        'featured_img_url': featureImage(browser),
        'marsFacts': marsFacts(),
        'hemispheres': hemispheres(browser)
    }
    browser.quit()
    return data

def hemispheres(browser):
    #Scrape to find Mars hemispheres with image link and title
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
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

    return hemisphere_img_title

def featureImage(browser):
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = bs(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def marsNews(browser):
    # Uses splinter to interact with the html page for Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    #div for articles
    newsContent = soup.find_all('div', class_='list_text')

    #Find title and paragraph, store in dictionary, append dictionary to news list
    for news in newsContent:
        try:
            newsTitle = news.find('div', class_='content_title').text
            newsParagraph = news.find('div', class_='article_teaser_body').text
        except:
            return None, None

    return newsTitle, newsParagraph

def marsFacts():
    #Scrape for mars information using pandas
    marsTable = pd.read_html('https://space-facts.com/mars/')[0]
    marsTable.columns = ["Description", "Mars"]
    marsTable.set_index("Description", inplace=True)
    marsTableHTML = marsTable.to_html(classes="table table-stripped")
    return marsTableHTML

