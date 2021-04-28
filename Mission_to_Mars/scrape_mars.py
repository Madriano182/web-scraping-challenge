from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time



# Set up Splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mission_to_mars_dict ={}


##### NASA MARS NEWS #####

    mars_news_url = "https://redplanetscience.com/"
    browser.visit(mars_news_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "lxml")


#Search for titles and paragraphs
    all_titles = soup.find_all('div', class_='content_title')
    all_p = soup.find_all('div', class_='article_teaser_body')

# Extract first title and first paragraph, and assign them to variables
    news_title = all_titles[0].text
    news_p = all_p[0].text



##### JPL Mars Space Images - Featured Image #####


#Search for the URL

    images_url = 'https://spaceimages-mars.com/'
    browser.visit(images_url)
    time.sleep(1)
    html = browser.html
    images_soup = BeautifulSoup(html, 'html.parser')

#Get the images 
    rel_image_path = images_soup.find_all('img')[2]["src"]
    featured_image_url = images_url + rel_image_path
    


##### MARS FACTS #####

#Scrape data with pd
    mars_facts_table = pd.read_html('https://space-facts.com/mars/')

# Get the table for Mars facts
    df = mars_facts_table[1]
    df.set_index('Mars - Earth Comparison')

#Convert it to HTML
    mars_facts_html = df.to_html()


##### MARS HEMISPHERES #####

#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)

    hemisphere_img_urls = []

# Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}

        browser.find_by_css("a.product-item h3")[item].click()
    # Get the href by locating the Samples images
        sample = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample["href"]
    # Get the Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text  
    # Append Hemisphere info collected to a list
        hemisphere_img_urls.append(hemisphere)
    # Go back to the main page to loop again
        browser.back()

#URLS
    hemisphere_img_urls


 # Store data in a dictionary
    mission_to_mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "mars_facts": mars_facts_html,
        "hemispheres": hemisphere_img_urls
    }

#Close the browser
    browser.quit()


    return mission_to_mars_dict