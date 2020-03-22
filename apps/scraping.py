
# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd, datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # run mars news
    news_title, news_paragraph = mars_news(browser)

    #run mars challenge
    hemi_list    = challenge_image(browser)
    
    #run all scraping functions and store data
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemi_img" : hemi_list
    }
    browser.quit()
    return data

def mars_news(browser):
    # ### Mars News

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = BeautifulSoup(html,'html.parser')

    try:
        # find element we want
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
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

    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')
    
    except AttributeError:
        return None

    # make a clickable url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

def mars_facts():
    # ### Space Facts
    try:
    # get html via pandas
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)

    # fact_html = '<table id="tablepress-p-mars-no-2" class="tablepress tablepress-id-p-mars"><tbody><tr class="row-1 odd"><td class="column-1"><strong>Equatorial Diameter:</strong></td><td class="column-2">6,792 km<br></td></tr><tr class="row-2 even"><td class="column-1"><strong>Polar Diameter:</strong></td><td class="column-2">6,752 km<br></td></tr><tr class="row-3 odd"><td class="column-1"><strong>Mass:</strong></td><td class="column-2">6.39 × 10^23 kg<br> (0.11 Earths)</td></tr><tr class="row-4 even"><td class="column-1"><strong>Moons:</strong></td><td class="column-2">2 (<a href="https://space-facts.com/moons/phobos/">Phobos</a> &amp; <a href="https://space-facts.com/moons/deimos/">Deimos</a>)</td></tr><tr class="row-5 odd"><td class="column-1"><strong>Orbit Distance:</strong></td><td class="column-2">227,943,824 km<br> (1.38 AU)</td></tr><tr class="row-6 even"><td class="column-1"><strong>Orbit Period:</strong></td><td class="column-2">687 days (1.9 years)<br></td></tr><tr class="row-7 odd"><td class="column-1"><strong>Surface Temperature: </strong></td><td class="column-2">-87 to -5 °C</td></tr><tr class="row-8 even"><td class="column-1"><strong>First Record:</strong></td><td class="column-2">2nd millennium BC</td></tr><tr class="row-9 odd"><td class="column-1"><strong>Recorded By:</strong></td><td class="column-2">Egyptian astronomers</td></tr></tbody></table>'
    fact_html = df.to_html(header=None).replace("dataframe","table table-striped")
    return fact_html

def challenge_image(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    #list of hemisphere names
    hemi_names = [
    "Cerberus",
    "Schiaparelli",
    "Syrtis Major",
    "Valles Marineris"
    ]

    hemi_list = []

    for hemi in hemi_names:
        # find hemi URL and click
        browser.is_element_present_by_text(hemi, wait_time=1)
        more_info_elem = browser.links.find_by_partial_text(hemi)
        more_info_elem.click()
        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        img_url_rel = img_soup.select_one('div.wide-image-wrapper \
                                        div.downloads ul li a').get('href')
        
        hemi_list.append({"title": hemi, "img_url": img_url_rel})

        browser.back()

    return hemi_list

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())    
