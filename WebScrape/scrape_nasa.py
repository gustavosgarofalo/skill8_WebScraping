import requests
import os
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs

 
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#initiate scrapping tool 
def scrape_info():
    browser = init_browser()

######################################################
#vitit the nasa url to retrieve data (title/paragraph)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

# Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

# Access the division of the title 
    title_div = soup.find('div', class_='content_title')
    
#Store the title into a variabe
    news_title = title_div.find_all('a')[0].text

#Store the paragraph content of the title (teaser) into a varible
    news_p = soup.find('div', class_='article_teaser_body').text


########################################################
#vitit the nasa url to retrieve Featured image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')

    browser.find_by_css('.fancybox-expand').first.click()

    html = browser.html
    soup = bs(html, 'html.parser')
    
    #Scrapping and Assigning the desired image (latest of mars) to a variable
    img_place = soup.find('img', class_='fancybox-image')
    img_path= img_place['src']
    feat_url = f'https://www.jpl.nasa.gov{img_path}'


##########################################################
# Scrape nasa twitter account to retrieve the last mars weather information published
#vitit the nasa url to retrieve weather data from last post
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

# Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

# Access the division of the weather content 
    weather_div = soup.find('div', class_='js-tweet-text-container')
    
#Store the weather information into a variabe
    mars_weather = weather_div.find_all('p')[0].text


##########################################################
#Navigate through the space-facts website to retrieve the table using pandas
    url='https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html

    #reading the webpage url with read_html
    page_tables = pd.read_html(url)

    #assigning the one table to a mariable
    facts_table=pd.DataFrame(page_tables[0])
    #rename default columns name 
    facts_table=facts_table.rename(columns={0:'description', 1:'value'})
    #setting the first column as index
    facts_table=facts_table.set_index('description')

    #converting the table scraped to html
    mars_facts=facts_table.to_html(classes='table')


##########################################################
#Visit the USGS Astrogeology website to scrape each mars hemispheres
    #Creating lists with all the hemisphere names to be scraped
    hemis=['Cerberus Hemisphere', 'Schiaparelli Hemisphere', "Syrtis Major Hemisphere", 'Valles Marineris Hemisphere']
    #Create empty list to append each hemisphere name(title) with its respective url
    hemisphere_img_urls = []
    #Get Hemisphere Pictures
    for hemi in hemis:
        #for each item in the hemisphere list, visit the url, click on the desired hemisphere
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = bs(html, 'html.parser')

        #Reference the desired image
        img_place= soup.find('a', text='Sample')
        img_url = img_place['href']
        post={
            'title': hemi,
            'img_url': img_url
        }
        hemisphere_img_urls.append(post)


# Store all scraped data in a dictionary
    news_data = {
        "news_title": news_title,
        "news_p": news_p,
        "feat_url": feat_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        'hemisphere_img_urls': hemisphere_img_urls      
    }

# Close the browser after scraping
    browser.quit()

# Return results
    return news_data

 