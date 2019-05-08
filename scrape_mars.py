#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), '../../../../mission-to-mars'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # Step 1 - Scraping
# 

#%%
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime as dt
from time import sleep



def scrape():
    executable_path = {'executable_path': "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=True)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # create new empty list to append data into
    mars_news = []

    browser.visit(url)

    html = browser.html
    soup= BeautifulSoup(html, 'html.parser')

    # Retrieve the class where the list of articles are
    results = soup.find_all(class_='slide')
    #loop through the result to append each result and create a dictionary 
    for result in results:
        news_title = result.find(class_='content_title').text

        try:
            news_p = result.find(class_='article_teaser_body').text
            result_dict = {
                "news_title":   news_title,
                "news_p": news_p,
            }
            mars_news.append(result_dict)
        except:
            
            continue

    browser.quit()
    mars_news


    #%%

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    # and assign the url string to a variable
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # first page

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(image_url)
    #splinter to click full image
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(2)

    #%%
    #splinter to click more info
    browser.click_link_by_partial_text('more info')


    #%%
    #get image url
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    jpegs = soup.find_all('div', class_='download_tiff')

    for x in jpegs:
        if "JPG" in x.text:
            featured_image_url = x.find('a')['href']
        else:
            continue 

    featured_image_url =  'https:'+ featured_image_url
    browser.quit()
    print(featured_image_url)


    #%%
    #initialize splinter again
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    twitter_url = "https://twitter.com/marswxreport?lang=en"

    browser.visit(twitter_url)
    #read the first tweet and save the text 
    html = browser.html
    soup= BeautifulSoup(html, 'html.parser')

    twitter_result = soup.find_all('div', class_='js-tweet-text-container', limit=1)
    for result in twitter_result:
        mars_weather = result.find('p').text

    browser.quit()
    print(mars_weather)


    #%%
    #use pandas to read the first table on the webpage and rename columns
    facts_table = pd.read_html("https://space-facts.com/mars/")[0]
    facts_table.columns = ['description','value']
    facts_table


    #%%
    astrogeology= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # create empty list to append the dictionaries
    hemisphere_image_urls = []

    # initialize splinter
    executable_path = {'executable_path': "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(astrogeology)

    response = requests.get(astrogeology)
    soup = BeautifulSoup(response.text, 'html.parser')

    #retrieve list of hemisphere images
    results = soup.find_all(class_='itemLink')

    # loop through each item
    for result in results:
        #store the title
        title = result.find(class_='description').text
        #click the title
        browser.click_link_by_partial_text(title)
        html = browser.html
        #create another beautiful soup for new page
        soup_result = BeautifulSoup(html, 'html.parser')
        image_urls = soup_result.find(class_='content').find(class_='block').find('dl').find('dd').find_next('dd')
        for image_url in image_urls:
            try:
                img_url = image_url ['href']
                img_url_jpeg = img_url + '/full.jpg'
                hemisphere_dict = {
                    "title":   title,
                    "img_url": img_url_jpeg,
                }
                hemisphere_image_urls.append(hemisphere_dict)
            except:
                continue
    #   always go back to the initial url window
        browser.back()
    # close browser 
    browser.quit()


    #%%
    hemisphere_image_urls
    mars_data = {
        "news" : mars_news,
        "mars_image" : featured_image_url,
        "current_weather" : mars_weather,
        "table" : facts_table.to_html(),
        "hemisphere_images" : hemisphere_image_urls
    }
    
    return mars_data



#%%



