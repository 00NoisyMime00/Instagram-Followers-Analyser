from config import change, id, password
from getpass import getpass
from datetime import datetime
import time
import json
#selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


if id == "" or password == "":
    change()

    with open('user.json', 'r') as f:
        details = json.loads(f.read())
        id = details['id']
        password = details['password']


def execute():

    global id

    # create a new Chrome session
    try:
        driver = webdriver.Chrome('/usr/bin/chromedriver')
    except:
        driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.maximize_window()

    # Navigate to the application home page
    driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

    #login
    user = driver.find_element_by_name('username')
    user.send_keys(id)
    passw = driver.find_element_by_name('password')
    passw.send_keys(password)
    passw.send_keys(Keys.ENTER)

    driver.implicitly_wait(5)

    #click not now
    buttons = driver.find_elements_by_tag_name('button')
    not_now_button = driver.find_element_by_xpath('//button[text()="Not Now"]')
    not_now_button.click()

    # if input("do you want someone else's account? Y/n").lower() == 'y':
    #     id = input('enter new handle: ')
    
    

    #open followers list and save in a list
    driver.get('https://www.instagram.com/'+id)
    aTags = driver.find_elements_by_tag_name('a')

    numberOfFollowers = 0
    for tag in aTags:
        if tag.get_attribute("href") == "https://www.instagram.com/"+id+"/followers/":
            followerSpan = tag.find_element_by_tag_name('span')
            numberOfFollowers = int(followerSpan.get_attribute('title'))
            tag.click()

        else:
            pass

    driver.implicitly_wait(3)


    startTime = time.time()
    #scroll down
    count = 0
    while count <= numberOfFollowers:
        div = driver.find_element_by_xpath('//div[@role="dialog"]')
        divs =  div.find_elements_by_tag_name('li')

        
        for i in range(count, len(divs)):
            
            driver.execute_script('arguments[0].scrollIntoView(true);', divs[i])
            driver.implicitly_wait(10)
            count += 1
        
        if count == numberOfFollowers:
            break


    #append the names in list
    aList = []

    driver.implicitly_wait(3)
    div = driver.find_element_by_xpath('//div[@role="dialog"]')
    divs =  div.find_elements_by_tag_name('li')

    count = 0

    for div in divs:
        driver.implicitly_wait(20)
        try:
            handleName = div.find_elements_by_tag_name('a')
        except:
            dive = driver.find_element_by_xpath('//div[@role="dialog"]')
            divs =  dive.find_elements_by_tag_name('li')
            handleName = divs[count].find_elements_by_tag_name('a')
        

        if len(handleName) == 2:
            aList.append(handleName[1].text)
        
        else:
            aList.append(handleName[0].text)

        count += 1
    

###########################################################################################
    
    #open followers list and save in a list
    driver.get('https://www.instagram.com/'+id)
    aTags = driver.find_elements_by_tag_name('a')

    numberOfFollowing = 0
    for tag in aTags:
        if tag.get_attribute("href") == "https://www.instagram.com/"+id+"/following/":
            followingSpan = tag.find_element_by_tag_name('span')
            numberOfFollowing = int(followingSpan.text)
            tag.click()

        else:
            pass

    driver.implicitly_wait(10)


    #scroll down
    count = 0
    while count <= numberOfFollowing:
        div = driver.find_element_by_xpath('//div[@role="dialog"]')
        divs =  div.find_elements_by_tag_name('li')
        
        for i in range(count, len(divs)):
            
            driver.execute_script('arguments[0].scrollIntoView(true);', divs[i])
            driver.implicitly_wait(5)
            count += 1
        
        if count == numberOfFollowing:
            break
        

    #append the names in list
    followingList = []

    div = driver.find_element_by_xpath('//div[@role="dialog"]')
    divs =  div.find_elements_by_tag_name('li')


    for div in divs:
        driver.implicitly_wait(3)
        handleName = div.find_elements_by_tag_name('a')

        if len(handleName) == 2:
            followingList.append(handleName[1].text)
    
        else:
            followingList.append(handleName[0].text)
        


    return [aList, numberOfFollowers, followingList, numberOfFollowing]



def saveFile(aList, numberOfFollowers):
    with open('followersList.json', 'w') as f:
        json.dump([str(datetime.today()),numberOfFollowers]+aList, f)


if __name__ == "__main__":

    aList, numberOfFollowers, followingList, numberOfFollowing = execute()
    
    prevSavedFile = []
    prevSavedFollowers = []

    with open('followersList.json', 'r') as f:
        prevSavedFile = json.loads(f.read())
    

    if prevSavedFile != []:
        prevSavedFollowers = prevSavedFile[2:]
        print("")
        print('Last checked Date:', prevSavedFile[0])
        print("")
        print("")


        newFollowers = []
        counting = 0

        for name in aList:
            try:
                prevSavedFollowers.index(name)
                prevSavedFollowers.remove(name)
                
            except:
                newFollowers.append(name)

        print("A total of " + str(len(prevSavedFollowers)) + " unfollowed you, names are: ",prevSavedFollowers)
        print("")

        with open('followersList.json', 'w') as f:
            json.dump([str(datetime.today()), numberOfFollowers] + aList, f)

    else:
        saveFile(aList, numberOfFollowers)
        


    for name in aList:
        try:
            followingList.index(name)
            followingList.remove(name)
        except:
            pass


    print("The no. of people that you follow who do not follow you back are: "+str(len(followingList))+" and names are: ")
    for name in followingList:
        print(name)
        

