from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Initialize the Chrome WebDriver
s      = Service("C:/Users/jasme/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe") 
driver = webdriver.Chrome(service=s)

# Amazon search results page
url = 'https://www.amazon.com/s?k=data+science+books'

# Open in the browser webdriver's Chrome
driver.get(url)

#  Load more results by Scrolling down
for _ in range(5):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# Store scraped data
data = []

# Pagination loop starts here
while True:
    # By class name its finding all the product listings on the page amazon page 
    product_listings = driver.find_elements(By.CSS_SELECTOR, '.s-main-slot .s-result-item')

    for listing in product_listings:
        try:
            title = listing.find_element(By.CSS_SELECTOR, '.a-text-normal').text
        except:
            title = 'N/A'

        try:
            price = listing.find_element(By.CSS_SELECTOR, '.a-price-whole').text + "." + listing.find_element(By.CSS_SELECTOR, '.a-price-fraction').text
        except:
            price = '0.00'

        try:
            author = listing.find_element(By.CSS_SELECTOR, '.a-row.a-size-base.a-color-secondary').text
        except:
            author = 'N/A'

        try:
            product_reviews = listing.find_element(By.CSS_SELECTOR, '.a-link-normal.s-underline-text.s-underline-link-text.s-link-style .a-size-base.s-underline-text').text 
        except:
            product_reviews = 'N/A'
        
        try:
            product_type = listing.find_element(By.CSS_SELECTOR, '.a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-bold').text 
        except:
            product_type = 'N/A'

        if(title != 'N/A'):
            data.append({
                'title'     : title,
                'price'     : float(price),
                'author'    : author,
                'reviews'   : product_reviews,
                'type'      : product_type,
            })

    # Find the "Next" button and click it
    try:
        next_button = driver.find_element(By.PARTIAL_LINK_TEXT, '.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')
        next_button.click()
        time.sleep(2)  
    except:
        break         

# Close the webdriver.Chrome browser 
driver.quit()

# DataFrame created from the scraped data
df = pd.DataFrame(data)

# Save the data to amazon_product.csv
df.to_csv('amazon_product.csv', index = False)


