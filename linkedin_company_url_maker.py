import random, time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
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

def get_excel_column (file):  #Function to Get the Company Name Column of Pitchbook Exported Data"""whe Company Name Column of Pitchbook Exported Data
    wb = load_workbook(file) # Open Live companies workbook
    live_companies = wb["Data"] # Navigate to correct sheet 
    column = live_companies['B'] # Column B
    return column

def get_company_url(search_query): # This will search a company and then retrieve the linkedin URL of that company

    linkedin_search_box = driver.find_element_by_xpath("//input[@aria-label='Search']") # Locate Search Box
    linkedin_search_box.send_keys(search_query) # Enter search query into search box
    time.sleep(random.randint(5,8)) # Sleep
    linkedin_search_box.send_keys(Keys.ENTER) # "Press" enter key
    time.sleep(random.randint(5,8)) # Sleep
    linkedin_search_box.clear() # Clear Search Box
    try:
        companies_button = driver.find_element_by_xpath('//button[@aria-label="Companies"]') # Locate Companies Button on search page
        companies_button.click() # Click Button
    except:
        pass
    time.sleep(random.randint(5,8)) # Sleep
    
    soup = BeautifulSoup(driver.page_source, "lxml") # Make soup object
    results = soup.find("div", {"class":'ph0 pv2 artdeco-card mb2'}) # Locate results list
    
    if results != None:
        top_result = results.find("li", {"class":'reusable-search__result-container'}) # Locate Top Result

        if top_result != None:
            top_result_url = top_result.find("a")["href"] # Find the url associated with top result from search query
        else:
            top_result_url = driver.current_url
    else: 
        top_result_url = None

    time.sleep(random.randint(12,18))    
    return top_result_url # Return URL

def create_url_file(company_name_list, file_name): # Function to create a .txt file of company URLs and save with a given filename
    url_list = [] # Init Empty List
    for company in company_name_list: # Iterate Company Names
        print(f"Getting URL for {company}")
        url = get_company_url(company) # Get url for that company

        if url == None: # If get_company_url returns none try running function again
            print("No URL was found for this company, reattempting to find again")
            time.sleep(random.randint(10,30))     
            url = get_company_url(company)

        print(f"The URL for this company is {url}") # Print url
        url_list.append(url) # Append to list
        time.sleep(random.randint(5,8))

        if len(url_list) % 7 == 0: # Add random long break every 7 companies scraped in order to avoid linkedin maximum search frequency
            time.sleep(random.randint(60,120))

    with open(file_name, "w") as f: # Write a .txt file of company names
        for item in url_list:
            f.write(f"{item}\n")

def main(): # Main Function

    global driver # Create Global Driver

    live_list = get_excel_column("live_companies.xlsx") # Create Live Company List
    bankrupt_list = get_excel_column("bankrupt_companies.xlsx") # Create Bankrupt Company list
    live_company_list = [re.sub("\(.*\)", "", live_list[i].value) for i in range(9,len(live_list)) if live_list[i].value != None] # Munge Company List
    bankrupt_company_list = [re.sub("\(.*\)", "", bankrupt_list[i].value) for i in range(9,len(bankrupt_list)) if bankrupt_list[i].value != None] #Munge Company List

    driver = webdriver.Chrome("/Users/sam/Documents/Scripts/LinkedIn/driver/chromedriver") #Initiate Driver
    driver.get("https://www.linkedin.com/uas/login") # Get Driver to open LinkedIn Login Page
    login("config.txt") # Login to linkedin

    create_url_file(bankrupt_company_list, "bankrupt_url.txt") # Create URL txt file for bankrupt companies (calls get_company_url within)
    create_url_file(live_company_list, "live_url.txt" ) # Create URL txt file for live companies (calls get_company_url within)

    driver.quit() # Quite Driver

if __name__ == "__main__": # Executable Script as Main Program
    main()



    

