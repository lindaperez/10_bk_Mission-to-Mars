#!/usr/bin/env python
# coding: utf-8

# # Mission_to_Mars

# Import Splinter and BeautifulSoup
from logging import exception
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = mars_news(browser)
    facts  = mars_facts()
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": facts,
      "last_modified": dt.datetime.now()

    }
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # In the next empty cell, we'll set up the HTML parser:
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:

        slide_elem = news_soup.select_one('div.list_text')
        # Notice how we've assigned slide_elem as the variable to look for the <div /> tag and its descendent (the other tags within the <div /> element)? This is our parent element. This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using select_one, the first matching element returned will be a <li /> element with a class of slide and all nested elements within it.
        slide_elem.find('div',class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_body = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_body

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # In[11]:

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

        # Use the base URL to create an absolute URL
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    except AttributeError:
        return None
    return  img_url

def mars_facts():

    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df.columns=['description', 'Mars', 'Earth']
        df.set_index('description', inplace=True)
    
    except BaseException:
        return None
  
    return df.html()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all()) 

