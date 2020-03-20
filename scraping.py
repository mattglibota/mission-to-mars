
# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path)


    # ### Mars News

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = BeautifulSoup(html,'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find("div", class_='content_title').get_text()
    news_title

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    news_p


    # ### Featured Images

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # find and click the button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # find more info button and click
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    img_url_rel = img_soup.select_one('figure.lede a img').get('src')
    img_url_rel

    # make a clickable url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    img_url


    # ### Space Facts

    # get html via pandas
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)

    mars = df.to_html()

    browser.quit()

