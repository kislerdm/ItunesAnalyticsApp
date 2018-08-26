## establish a selenium driver
## author: D.Kisler <admin@dkisler.de>

from chrome_settings import *
from selenium import webdriver
# settings for chrome
from selenium.webdriver.chrome.options import Options
# browser settings
chrome_options = Options()  
chrome_options.binary_location = CHROME_PATH
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# create a browser 
browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
