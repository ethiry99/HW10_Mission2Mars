#!/usr/bin/env python
# coding: utf-8

# In[64]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[65]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager


# ### Visit the NASA Mars News Site

# In[66]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[67]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[68]:


slide_elem.find('div', class_='content_title')


# In[69]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[70]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[71]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[72]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[73]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[74]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[75]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[76]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[77]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[78]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[79]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[80]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = [
    {
        'img_url':"",
        'title':""}]*4

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html=browser.html
response = requests.get(url)
hemi_soup = soup(response.text, 'html.parser')
img_soup=soup(html,'html.parser')
#hemi_click=soup(html,'html.parser')

results=hemi_soup.find_all('div',class_='item')
result=results[0]
i=3
for result in results:

    hemi_desc=result.find('h3').get_text()
    
    print(hemi_desc)
    #val = 5 # in seconds
    #browser.implicitly_wait(val)
    hemi_full_img=browser.find_by_tag('img')[i]
    
    
    hemi_full_img.click()
    
    #val = 5 # in seconds
    #browser.implicitly_wait(val)
    mars_soup=soup(browser.html,'html.parser')
    img_url_rel=mars_soup.find_all('a')[3].get('href')
    print(img_url_rel)
    img_url = f'https://marshemisphers.com/{img_url_rel}'
    hemisphere_image_urls[i-3]={img_url,hemi_desc}
    browser.back()
    #hemi_full_image=browser
    i=i+1

hemisphere_image_urls


# In[81]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[82]:


# 5. Quit the browser
browser.quit()


# In[ ]:




