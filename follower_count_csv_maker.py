import random, time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from openpyxl import load_workbook
import pandas as pd


def login(config_file): # Function to get username/password from config file and submit to linkedin

    file = open(config_file) # Open Username and Password Folder
    lines = file.readlines() # Read Lines
    username = lines[0] # Assign username
    password = lines[1] # Assign Password

    try: # Try 
        username_box = driver.find_element_by_id("username") # Locate Username Box
        username_box.send_keys(username) # Send username to username box
        time.sleep(random.randint(5,8))

        password_box = driver.find_element_by_id("password") # Locate Password Box
        password_box.send_keys(password) # Send password to password box
        password_box.submit() # Submit
    except: # except for auto login
        pass

def get_url_list(file_name):
    with open(file_name) as f:
        url_list = f.readlines()
    return url_list

def get_follower_count(url): # Get Follower Count From Browser Source
    driver.get(url) # Navigate Browser to URL
    time.sleep(random.randint(10,30)) # Sleep
    soup = BeautifulSoup(driver.page_source, "lxml") # Create Soup Object
    info_elements = soup.find_all("div", class_="org-top-card-summary-info-list__info-item") # Find Info Elements
    for element in info_elements: # Iterate Elements
        if "follower" in element.text: # If Follower Found in the text (i.e the follower count element)
            follower_count = int(element.text.split()[0].replace(",","")) # Munge Follower Count to int
        else:
            pass

    if follower_count != None: # If Follower Count was found, pass
        pass
    else: # If not, set follower_count to None and print "Not Found"
        follower_count = None
        print("Follower Count Not Found") 
    return follower_count

def iterate_company_url_tocsv(company_url_list, filename): # Iterate Company url list and save as a csv fileyeh ex
    follower_count_list = []

    for url in company_url_list:
        print(f"Follower Count Currently being scraped for {url}")
        follower_count = get_follower_count(url)
        print(f"The Follower Count is: {follower_count}")
        follower_count_list.append(follower_count)
    
    df = pd.DataFrame({"Follower Count":follower_count_list})
    df.to_csv(filename, index = False)

def main():

    global driver

    driver = webdriver.Chrome("/Users/sam/Documents/Scripts/LinkedIn/driver/chromedriver") #Initiate Driver
    driver.get("https://www.linkedin.com/uas/login") # Get Driver to open LinkedIn Login Page
    login("config.txt") # Login to linkedin

    bankrupt_url_list = get_url_list("bankrupt_url.txt")
    live_url_list = get_url_list("live_url.txt")

    iterate_company_url_tocsv(bankrupt_url_list, "bankrupt_follower_count.csv")
    iterate_company_url_tocsv(live_url_list, "live_follower_count.csv")

    driver.quit()

if __name__ == "__main__":
    main()