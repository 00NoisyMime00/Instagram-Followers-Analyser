from config import change, id, password
from getpass import getpass
#selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


if id == "" or password == "":
    change()

# create a new Chrome session
driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.implicitly_wait(3)
driver.maximize_window()

# Navigate to the application home page
driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")





user = driver.find_element_by_name('username')
user.send_keys(id)
passw = driver.find_element_by_name('password')
passw.send_keys(password)
passw.send_keys(Keys.ENTER)



driver.implicitly_wait(5)

buttons = driver.find_elements_by_tag_name('button')

sign_in_button = driver.find_element_by_xpath('//button[text()="Not Now"]')
sign_in_button.click()

driver.get('https://www.instagram.com/noisy_mime')


aTags = driver.find_elements_by_tag_name('a')


numberOfFollowers = 0
for tag in aTags:
    if tag.get_attribute("href") == "https://www.instagram.com/noisy_mime/followers/":
        followerSpan = tag.find_element_by_tag_name('span')
        numberOfFollowers = int(followerSpan.get_attribute('title'))
        tag.click()

    else:
        pass

driver.implicitly_wait(3)



count = 0
while count <= numberOfFollowers:
    div = driver.find_element_by_xpath('//div[@role="dialog"]')
    divs =  div.find_elements_by_tag_name('li')
    
    for i in range(count, len(divs)):
        
        driver.execute_script('arguments[0].scrollIntoView(true);', divs[i])
        driver.implicitly_wait(3)
        count += 1
    
    if count == numberOfFollowers:
        break

aList = []
div = driver.find_element_by_xpath('//div[@role="dialog"]')
divs =  div.find_elements_by_tag_name('li')
for div in divs:
    handleName = div.find_elements_by_tag_name('a')
    if len(handleName) == 2:
        # print(handleName[1].text)
        aList.append(handleName[1].text)
    else:
        # print(handleName[0].text)
        aList.append(handleName[0].text)

with open('followersList.txt', 'a') as f:
    for i in aList:
        f.write(i+"\n")

        

