import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

dirname = os.path.dirname(__file__)
driverpath = r'%s' % dirname + r"/chromedriver"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enableautomation'])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=driverpath)
print("Running from: " + driverpath)

driver.get('https://directory.apps.upenn.edu/directory/jsp/fast2.do')
try:
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[9]/td/a[1]/span")))
finally:
    print('hi')

organization='UNDER'
affiliation='STU'
npath = '/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/table/tbody/tr[{}]/td[1]/table/tbody/tr/td/a/span'
epath = 'html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/table/tbody/tr[{}]/td[3]/table/tbody/tr[2]/td/a'
people = []

with open(dirname + '/contacts.csv', mode='w') as contacts:
    writer = csv.writer(contacts, delimiter =',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    entry = ["Name", "Given Name", "Additional Name", "Family Name", "Yomi Name", "Given Name Yomi", "Additional Name Yomi", "Family Name Yomi", "Name Prefix", "Name Suffix", "Initials", "Nickname", "Short Name", "Maiden Name", "Birthday", "Gender", "Location", "Directory Server", "Mileage", "Occupation", "Hobby", "Sensitivity", "Priority", "Subject", "Notes", "Language", "Photo", "Group Membership", "E-mail 1 - Type", "E-mail 1 - Value"]
    writer.writerow(entry)

for flet in range (97, 123):
    for slet in range (97, 123):
        driver.get('https://directory.apps.upenn.edu/directory/jsp/fast2.do')
        org = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[7]/td[2]/input')
        affil = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[6]/td[2]/select')
        search = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[3]/td[2]/input')
        org.clear()
        search.clear()
        org.send_keys(organization)
        affil.send_keys(affiliation)
        search.send_keys(chr(flet) + chr(slet))
        search = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[9]/td/a[1]/span')
        search.click()
        time.sleep(1)
        hasNext = True
        while (hasNext):
            for row in range(2, 22):
                try:
                    name = driver.find_element(By.XPATH, npath.format(row))
                    email = driver.find_element(By.XPATH, epath.format(row))
                except NoSuchElementException:
                    break
                else:
                    name = name.text 
                    email = email.text 
                    lastname = name[0 : name.index(',')]
                    firstname = name[name.index(',') + 2 : len(name)]
                    try:
                        middlename = firstname[firstname.index(' ') + 1 : len(firstname)]
                        firstname = firstname[0 : firstname.index(' ')]
                        middlename = middlename[0 : 1] + middlename[1 : len(middlename)].lower()
                    except Exception:
                        middlename = ""
                    firstname = firstname[0 : 1] + firstname[1 : len(firstname)].lower()
                    lastname = lastname[0 : 1] + lastname[1 : len(lastname)].lower()
                    if len(middlename) == 1:
                        middlename = middlename + '.'
                    name = firstname + " " + middlename + " " + lastname
                    entry = {"name" : name, "firstname": firstname, "middlename": middlename, "lastname": lastname, "email": email}
                    if entry in people:
                        break
                    else:
                        people.append(entry)
                        print(entry)
                        with open(dirname + '/contacts.csv', mode='a') as contacts:
                            writer = csv.writer(contacts, delimiter =',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            entry = [name, firstname, middlename, lastname, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", email]
                            writer.writerow(entry)
            try:
                nextpage = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/div[2]/a[2]/span')
            except NoSuchElementException:
                hasNext = False
                break
            else:
                if (nextpage.text == "Next"):
                    nextpage.click()
                    time.sleep(1)
                else:
                    break

# with open(dirname + '/contacts.csv', mode='w') as contacts:
#     writer = csv.writer(contacts, delimiter =',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     entry = ["Name", "Given Name", "Additional Name", "Family Name", "Yomi Name", "Given Name Yomi", "Additional Name Yomi", "Family Name Yomi", "Name Prefix", "Name Suffix", "Initials", "Nickname", "Short Name", "Maiden Name", "Birthday", "Gender", "Location", "Directory Server", "Mileage", "Occupation", "Hobby", "Sensitivity", "Priority", "Subject", "Notes", "Language", "Photo", "Group Membership", "E-mail 1 - Type", "E-mail 1 - Value"]
#     writer.writerow(entry)
#     for person in people:
#         entry = [person['name'], person['firstname'], person['middlename'], person['lastname'], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", person['email']]
#         writer.writerow(entry)