# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# scrape the function
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # get the information
    news_title, news_paragraph = scrape_mars(browser)
    
    #build a dictionary using the info from the scrapes
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemisphere": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }
    
    # stop web driver
    browser.quit()
    
    #display output
    return marsData
         
#scrape the pages
# srape the mars news page
def scrape_mars(browser):
   # Visit the NASA Mars News url 
    url = 'https://redplanetscience.com/'
    browser.visit(url)


    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    safety = soup(html, "html.parser")
    
    slide_element = safety.select_one("div.list_text")

    #slide_element.find("div", class_="content_title")

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_element.find("div", class_="content_title").get_text()
    #news_title
    # Use the parent element to find the paragraph text
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    #news_paragraph
    
    # return the title and paragraph
    return news_title, news_paragraph


# srape the featured image page
def scrape_feature_img(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_click = browser.find_by_tag('button')[1]
    full_image_click.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
    
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    print(img_url)
    #return the img url
    return img_url


# scrape the mars facts page
def scrape_facts_page(browser):
    # Visit URL
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)
    
    # Parse the resulting html with soup
    html = browser.html
    fact_soup = soup(html, 'html.parser')
    
    #facts location
    factslocation = fact_soup.find('div', class_="diagram mt-4")
    factTable = factslocation.find('table') 
    
    # create an empty string
    facts = ""
    
    #add text into the empty string then return
    facts += str(factTable)
    
    return facts


# scrape the Mars Hemisphere
def scrape_hemispheres(browser):
    #URL
    url = 'https://marshemispheres.com/'
    browser.visit(url +"index.html")
    
# Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # set up the loop
    for item in range(4):
        # Browse through each article
        #HEMI info DICT
        hemisphere = {}
            
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css('a.product-item img')[item].click()
            
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.links.find_by_text('Sample').first
        hemisphere["img_url"] = sample_element['href']
            
        # Get Hemisphere Title
        hemisphere['title'] = browser.find_by_css('h2.title').text
            
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
            
        # Navigate Backwards
        browser.back()
        
    # return the hemi with titles
    return hemisphere_image_urls

    
    

# set up flask app
if __name__ == "__main__":
    print(scrape_all())