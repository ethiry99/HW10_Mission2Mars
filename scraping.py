# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests


#print("here is the start")
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
hemispheres = [
    {
        'img_url':"",
        'title':""}]*4

def scrape_all():
    
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    #print("starting data funtion calls")
    time.sleep(2)
    data = {"news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemi_pics(),
        "last_modified": dt.datetime.now()
        
    }
    #print("finished data funtion calls")
    time.sleep(2)
    #print(data)
    #print("starting nap")
    #time.sleep(10)

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    #print("finding news")
    #time.sleep(2)

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    print("visting new site")
    time.sleep(2)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    print(f"the title of the story is {news_title}")
    return news_title, news_p


def featured_image(browser):
    #print("finding pretty pictures")
    #time.sleep(2)
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    print(f"found pretty picture, it is at {img_url}")
    return img_url

def mars_facts():
    #print("looking for facts")
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
   
    except BaseException:
        print("found NONE facts")
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# def hemi_pics():
#     #print("hemipics was called")
#     # 1. Use browser to visit the URL 
#     url = 'https://marshemispheres.com/'
#     browser.visit(url)

#     # 2. Create a list to hold the images and titles.
#     hemispheres = [
#     {
#         'img_url':"",
#         'title':""}]*4

#     # 3. Write code to retrieve the image urls and titles for each hemisphere.
#     html=browser.html
#     response = requests.get(url)
#     hemi_soup = soup(response.text, 'html.parser')
#     img_soup=soup(html,'html.parser')
#     #hemi_click=soup(html,'html.parser')

#     results=hemi_soup.find_all('div',class_='item')
#     result=results[0]
#     i=3
#     for result in results:
#         hemi_desc=result.find('h3').get_text()
#         #print(hemi_desc)
#         hemi_full_img=browser.find_by_tag('img')[i]
#         hemi_full_img.click()
#         mars_soup=soup(browser.html,'html.parser')
#         img_url_rel=mars_soup.find_all('a')[3].get('href')
#         #print(img_url_rel)
#         img_url = f'https://marshemisphers.com/{img_url_rel}'
#         hemispheres[i-3]={img_url,hemi_desc}
#         browser.back()
#         i=i+1
#         print("hemispheres in app")
#         print(hemispheres)
     
#     return hemispheres    

# # hemispheres = [
# #    {
# #         'img_url':"",
# #         'title':""}]*4
# # hemi_pics()
# # print("after the function")
# # print(hemispheres)
def hemi_pics():
    #print("hemi_pics was called")
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemispheres = [{
        'img_url':[],
        'title':[]
        }]*4

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html=browser.html
    response = requests.get(url)
    hemi_soup = soup(response.text, 'html.parser')
    img_soup=soup(html,'html.parser')
    #hemi_click=soup(html,'html.parser')

    results=hemi_soup.find_all('div',class_='item')
    result=results[0]
    i=3
    print("entering for loop")
    for result in results:
        hemi_desc=result.find('h3').get_text()
        #print(hemi_desc)
        hemi_full_img=browser.find_by_tag('img')[i]
        hemi_full_img.click()
        mars_soup=soup(browser.html,'html.parser')
        img_url_rel=mars_soup.find_all('a')[3].get('href')
        #print(img_url_rel)
        img_url = f'https://marshemisphers.com/{img_url_rel}'
        hemispheres[i-3]={img_url,hemi_desc}
        #hemispheres[1-3]=hemi_desc
        
        #hemispheres['img_url'].append(img_url)
        #hemispheres['title'].append(hemi_desc)
        
        browser.back()
        i=i+1
        #print("hemispheres in app")
    print(hemispheres)
    #print("this one's got a hemi!") 
    return hemispheres    

# hemispheres = [
#    {
#         'img_url':"",
#         'title':""}]*4
# hemi_pics()
# print("after the function")
print(hemispheres)


if __name__ == "__main__":
    print("running scrape")
    # If running as script, print scraped data
    print(scrape_all())