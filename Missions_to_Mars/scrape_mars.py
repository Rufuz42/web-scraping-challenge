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
        "Featured Image URL": scrape_feature_image(browser),
        "Facts": scrape_facts_mars(browser),
        "Hemispheres": scrape_hemispheres(browser)
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
def scrape_facts_mars(browser):
    # Generates a session to visit the webpage
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Converts the browser visit html to soup
    facts_html = browser.html
    facts_soup = bs(facts_html, 'html.parser')

    # Can't use pandas the same way, so grabbing the html code
    facts_locations = facts_soup.find('div', class_= 'diagram mt-4')
    facts_table = facts_locations.find('table')

    # string to hold the facts
    facts = ""

    # Adds the facts to the string
    facts += str(facts_table)

    # Returns the facts
    return facts


# Hemispheres
def scrape_hemispheres(browser):
    # Generates a session to visit the webpage
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Converts the browser visit html to soup
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')

    # Uses soup to create a list of all the class=item parts of the page as that's where the images are.
    hemi_soup2 = hemi_soup.find_all('div', class_='item')
    hemi_soup2

    # Create an empty list to store both titles and image urls
    hemisphere_dict = []

    # Create a for loop to scroll through the images, grab the URLs, and append them to the list
    for x in hemi_soup2:
    
        # Grabs the titles in the h3 text on the main page
        page_title = x.h3.text
        # Locates the image page
        image_links = x.find("a", class_="itemLink product-item")['href']
        browser.visit(f"https://marshemispheres.com/{image_links}")
        # Finds the link witihin that page
        image_url = browser.find_by_text('Sample')['href']
        # Appends both the title and image url to the list to create a dictionary
        hemisphere_dict.append({'title': page_title, 'img_url': image_url})

    # Return both hemipshere Titles and URLs
    return hemisphere_dict



# Setup Flask
if __name__ == "__main__":
    print(scrape_all())