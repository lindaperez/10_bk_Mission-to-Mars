#!/usr/bin/env python
# coding: utf-8

# In[32]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt


# In[55]:


def scrape_all():
    # Set the executable path and initialize Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    facts = mars_facts()
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": facts,
      "last_modified": dt.datetime.now(),
      "hemispheres": mars_hemispheres(browser)
    }
    
    browser.quit()
    return data



# ### Visit the NASA Mars News Site

# In[8]:


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    waited = browser.is_element_present_by_css('div.list_text', wait_time=1)
    #print(waited)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
            return None
    return news_title, news_p


# ### JPL Space Images Featured Image

# In[40]:


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')


        # Use the base url to create an absolute url
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    except AttributeError:
        return None
    return img_url


# ### Mars Facts

# In[10]:


def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df.columns=['Description', 'Mars', 'Earth']
        df.set_index('Description', inplace=True)
      
    except BaseException:
        return None
    print(df)
    return df.to_html(classes=["table","table-bordered", "table-striped", "table-hover","table-responsive"],header = "true", justify = "center")


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[52]:


def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    browser.is_element_present_by_css('div#product-section', wait_time=1)  # delay to load page
    hemisps_soup = soup(browser.html, 'html.parser')
    h_selector = hemisps_soup.select_one('div#product-section')
    h_items = h_selector.find_all('div', class_='item')


    for item in h_items:
        img_url = f"{url}{item.select_one('img.thumb').get('src')}"

        title_selector = item.select_one('a.itemLink.product-item')
        title = title_selector.find_next('h3').get_text()
        title_link = f"{url}{title_selector.get('href')}"
        img_url = find_full_image_hemispheres(url,title_link,browser)
        #print(title_link)
        hemisphere_image_urls.append({'img_url':img_url, 'title':title})

    # 4. Print the list that holds the dictionary of each image url and title.
    print(hemisphere_image_urls)
    return hemisphere_image_urls


# In[50]:


def find_full_image_hemispheres(url,title_link,browser):

    # Find and click the full image button
    browser.visit(title_link)

    # Parse the resulting html with soup
    html_img = browser.html
    img_hem_soup = soup(html_img, 'html.parser')
  
    
    try:
        # find the relative image url
        div_downloads = img_hem_soup.find('div', class_='downloads')
        full_img_src = div_downloads.find('a').get('href')


        # Use the base url to create an absolute url
        img_url = f'{url}{full_img_src}'

    except AttributeError as e:
        print(str(e))
        return None
    return img_url





