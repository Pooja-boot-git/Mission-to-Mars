#!/usr/bin/env python
# coding: utf-8

# In[154]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[155]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[7]:


print(slide_elem.text)


# In[8]:


slide_elem.find('div', class_='content_title')


# In[18]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[19]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# In[20]:


news_date = slide_elem.find('div', class_='list_date').get_text()
news_date


# ### Featured Images

# In[51]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[56]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
#print(full_image_elem.text)
full_image_elem.click()


# In[57]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[58]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[59]:


abs_utl = f"{url}/{img_url_rel}"
print (abs_utl)


# In[61]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[62]:


df.to_html()


# ### Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 
# ## Hemispheres

# In[156]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)
browser.is_element_present_by_css('div.description', wait_time=1)
#browser.click_link_by_href('https://marshemispheres.com/cerberus.html')


# In[242]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
#key_list = ['img_url','title']
#hemisphere_image_urls_dict = dict.fromkeys(key_list)
html = browser.html
mars_soup = soup(html, 'html.parser')
for div in mars_soup.find_all('div', class_='description'):
    for items in div.find_all('a', class_='itemLink product-item'):
        for links in items.find_all('h3'):
            hemispheres = {}
            title = links.text
            browser.click_link_by_partial_text(links.text)
            html1 = browser.html
            img_soup = soup(html1, 'html.parser')
            img_link = img_soup.find_all('li')[0]
            relative_link = img_link.find('a').get('href')
            img_url = f"{url}{relative_link}"
            hemispheres['img_url'] = img_url
            hemispheres['title'] = title
            hemisphere_image_urls.append(hemispheres)
            browser.back()


# In[243]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[244]:


# 5. Quit the browser
browser.quit()


# In[ ]:




