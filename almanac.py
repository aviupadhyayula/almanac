import os
from selenium import webdriver

dirname = os.path.dirname(__file__)
driverpath = r'%s' % dirname + r"/chromedriver"
print('Running from: ' + driverpath)

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options, executable_path=driverpath)
driver.get('https://directory.apps.upenn.edu/directory/jsp/fast2.do')