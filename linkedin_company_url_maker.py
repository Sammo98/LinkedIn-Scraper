import os, random, sys, time, json
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from openpyxl import load_workbook
import re
import requests
import pandas as pd

def random_long_sleep(): # Random long sleep function (10-30 seconds) to emulate human behaviour
    time.sleep(random.randint(10,30))
    
def random_short_sleep(): # Random short sleep function (5-10 seconds) to emulate human behaviour
    time.sleep(random.randint(5,8)) 

def login(config_file): # Function to get username/password from config file and submit to linkedin

    file = open(config_file) # Open Username and Password Folder
    lines = file.readlines() # Read Lines
    username = lines[0] # Assign username
    password = lines[1] # Assign Password

    try: # Try 
        username_box = driver.find_element_by_id("username") # Locate Username Box
        username_box.send_keys(username) # Send username to username box
        random_short_sleep() # Short sleep

        password_box = driver.find_element_by_id("password") # Locate Password Box
        password_box.send_keys(password) # Send password to password box
        password_box.submit() # Submit
    except: # except for auto login
        pass

def get_excel_column (file):  #Function to Get t"""Function to Get the Company Name Column of Pitchbook Exported Data"""whe Company Name Column of Pitchbook Exported Data
    wb = load_workbook(file) # Open Live companies workbook
    live_companies = wb["Data"] # Navigate to correct sheet 
    column = live_companies['B'] # Column B
    return column

def get_company_url(search_query): # This will search a company and then retrieve the linkedin URL of that company

    linkedin_search_box = driver.find_element_by_xpath("//input[@aria-label='Search']") # Locate Search Box
    linkedin_search_box.send_keys(search_query) # Enter search query into search box
    random_short_sleep() # Sleep
    linkedin_search_box.send_keys(Keys.ENTER) # "Press" enter key
    random_short_sleep() # Sleep
    linkedin_search_box.clear()
    try:
        companies_button = driver.find_element_by_xpath('//button[@aria-label="Companies"]') # Locate Companies Button on search page
        companies_button.click() # Click Button
    except:
        pass
    random_short_sleep() # Sleep
    
    source = driver.page_source # Retrieve source code from search page
    soup = BeautifulSoup(source, "lxml") # Make soup object
    results = soup.find("div", {"class":'ph0 pv2 artdeco-card mb2'}) # Locate results list
    
    if results != None:
        top_result = results.find("li", {"class":'reusable-search__result-container'}) # Locate Top Result

        if top_result != None:
            top_result_url = top_result.find("a")["href"] # Find the url associated with top result from search query
        else:
            top_result_url = driver.current_url
    else: 
        top_result_url = None
        
    return top_result_url # Return URL

def create_url_file(company_name_list, file_name):
    url_list = []
    for company in company_name_list:
        print(f"Getting URL for {company}")
        url = get_company_url(company)
        if url == None: # If get_company_url returns none try running function again
            print("No URL was found for this company, reattempting to find again")
            random_long_sleep()       
            url = get_company_url(company)
        print(f"The URL for this company is {url}") # Print url
        url_list.append(url) # Append to list
        random_short_sleep()
        if len(url_list) % 7 == 0: # Add random long break every 7 companies scraped in order to avoid linkedin maximum search frequency
            time.sleep(random.randint(60,120))

    with open(file_name, "w") as f: # Write a .txt file of company names
        for item in url_list:
            f.write(f"{item}\n")

live_list = get_excel_column("live_companies.xlsx") # Create Live Company List
bankrupt_list = get_excel_column("bankrupt_companies.xlsx") # Create Bankrupt Company list
live_company_list = [re.sub("\(.*\)", "", live_list[i].value) for i in range(9,len(live_list)) if live_list[i].value != None] # Munge
bankrupt_company_list = [re.sub("\(.*\)", "", bankrupt_list[i].value) for i in range(9,len(bankrupt_list)) if bankrupt_list[i].value != None] #Munge

driver = webdriver.Chrome("/Users/sam/Documents/Scripts/LinkedIn/driver/chromedriver") #Initiate Driver
driver.get("https://www.linkedin.com/uas/login") # Get Driver to open LinkedIn Login Page
login("config.txt") # Login to linkedin

create_url_file(bankrupt_company_list, "bankrupt_url.txt")
create_url_file(live_company_list, "live_url.txt")

driver.quit()




    

