# All the imports
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# Scraping function
def scrape_all():

    # Sets up splinter, which allows me to run Chrome sessions
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Goal is to return a json to load into MongoDB

    # Mars News
    news_title, news_p = news_scrape(browser)

    # Build out the dictionary with all of the information
    mars_data = {
        "News Title": news_title,
        "News Paragraph": news_p,
        "Featured Image URL": scrape_feature_image(browser)
    }

    browser.quit()

    return mars_data


# Mars News - function to grab it
def news_scrape(browser):
    # Copying code from jupyter file
    # Generates a session to visit the webpage
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Converts the browser visit html to soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Title and teaser are in the list_text div
    slide_element = soup.select_one('div.list_text')

    # Grabs the first headline
    slide_element.find('div', class_='content_title')

    # Grabs just the text string from the div for the first article title
    news_title = slide_element.find('div', class_='content_title').get_text()

    # Grabs just the text string from the div for the first teaser body
    news_p = slide_element.find('div', class_='article_teaser_body').get_text()

    # Return the news title and paragraph text
    return news_title, news_p

# Featured Image
def scrape_feature_image(browser):
    # Copying code from jupyter file
    # Generates a session to visit the webpage
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # This clicks on the full image button for the full image
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    # Converts the browser visit html to soup
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    # Locates the image in the soup html
    featured_image_url = image_soup.find('img', class_='fancybox-image')
    # Concatenates the image + base uURL and returns full URL
    featured_image_url = url + featured_image_url['src']

    # Return the image URL
    return featured_image_url



# Facts Table


# Hemispheres


# Setup Flask
if __name__ == "__main__":
    print(scrape_all())