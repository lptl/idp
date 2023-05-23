from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import re as re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
df = pd.read_csv('C:/Users/fatih/PycharmProjects/Li_scraper/Crunchbase data/founders_dataset_IDP.csv',usecols=['first_name','last_name','linkedin_url'])

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

print(df.iloc[0]["linkedin_url"])
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


page = df.iloc[0]["linkedin_url"]
print(page)
try:
    f= open("linkedin_credentials.txt","r")
    contents = f.read()
    username = contents.replace("=",",").split(",")[1]
    password = contents.replace("=",",").split(",")[3]
except:
    f= open("linkedin_credentials.txt","w+")
    username = input('Enter your linkedin username: ')
    password = input('Enter your linkedin password: ')
    f.write("username={}, password={}".format(username,password))
    f.close()

chrome_options = Options()
#chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)

#Open login page
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

#Enter login info:
elementID = browser.find_element("id","username")
elementID.send_keys(username)

elementID = browser.find_element("id","password")
elementID.send_keys(password)
elementID.submit()

#browser.get(page + 'recent-activity/all/')
browser.get('https://www.linkedin.com/in/dmoskov'+'/detail/recent-activity/shares/')
link_activity = (page + '/recent-activity/all/')

browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
# delay = 3 # seconds
# try:
#     myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'ember501')))
#     print ("Page is ready!")
# except TimeoutException:
#     print ("Loading took too much time!")

#show_activity_button = browser.find_element("xpath","//button[contains(., 'Show all activity')]")

#show_activity_button.click()

# b = browser.find_element('xpath','//*[@id="ember157"]/footer/a/span')
# b.click()

print(link_activity)
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
screen_height = browser.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if (screen_height) * i > new_height:
        break


person_page = browser.page_source


#Use Beautiful Soup to get access tags
linkedin_soup = bs(person_page, 'lxml')
linkedin_soup.prettify("utf-8")
with open("output1.html","w", encoding= 'utf-8') as file:
    file.write(str(linkedin_soup))
#Find the post blocks
#containers = linkedin_soup.findAll("div",{"class":"occludable-update ember-view"})

containers = linkedin_soup.find_all('div', class_='relative')
print(containers)
post_texts = []

#ember859 > div > div.feed-shared-update-v2__description-wrapper > div > div
for container in containers:
    try:
        #posted_date = container.find("span", {"class": "visually-hidden"})
        text_box = container.find('div', attrs= {'class':"update-components-text relative feed-shared-update-v2__commentary", 'dir':"ltr"})
        text = text_box.find('span',attrs= {'dir': 'ltr'})

        # Appending date and text to lists
        if text != 'None' :
            no_span = text[16:-7]
            post_texts.append(no_span)
        print('loop')
    except:
        pass


print(post_texts)
data_exp = []
#print("output"+data_exp[0])


data_exp.append(post_texts)






