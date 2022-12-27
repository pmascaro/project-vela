####
#selenium solution - to access former version of this code refer to a former commit
####

# based on: https://medium.com/analytics-vidhya/what-if-selenium-could-do-a-better-job-than-your-travel-agency-5e4e74de08b0

# writing a good commit message: https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/

# install chrome driver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# avoid window popping up
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(ChromeDriverManager().install())

####
# launch your website for flight selection
####

# url = "https://www.kayak.com/flights"
# driver.get(url)
# time.sleep(1)

# Close cookies pop-up
# accept_cookies_xpath = '/html/body/div[12]/div/div[3]/div/div/div/div/div[1]/div/div[2]/div[2]/div[1]/button/span'

# try:
#    driver.find_element("xpath",accept_cookies_xpath).click()
# except NoSuchElementException:
#    pass

####
# fill in research info
####

departure = 'LON' 
arrival = 'PMI' 
departure_date = '2023-03-24' # Under the format 'YYYY-MM-DD'
arrival_date = '2023-03-28'
# flexibility_option = "" # commented as same day availability selected. for +/-3 days -> flexible.

url = f"https://www.kayak.com/flights/{departure}-{arrival}/{departure_date}/{arrival_date}" # add -{flexibility_option} after both dep date and arrival date for flexible search

# https://www.kayak.fr/flights/PAR-TUN/2020-11-07-flexible/2020-12-14-flexible
driver.get(url)

####
# handle dynamic web elements
####