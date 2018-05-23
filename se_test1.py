# To install the Python client library:
# pip install -U selenium

# Import the Selenium 2 namespace (aka "webdriver")
from selenium import webdriver

# Google Chrome 
driver = webdriver.Chrome('C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe')

# ------------------------------
# The actual test scenario: Test the codepad.org code execution service.

# Go to codepad.org
driver.get('http://codepad.org')

# Select the Python language option
python_link = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
python_link.click()

# Enter some text!
text_area = driver.find_element_by_id('textarea')
text_area.send_keys("print 'Good,' + ' Morning!'")

# Submit the form!
submit_switch = driver.find_element_by_name('submit')
submit_switch.click()

# Make this an actual test. Isn't Python beautiful?
assert "Good, Morning!" in driver.get_page_source()

# Close the browser!
driver.quit()