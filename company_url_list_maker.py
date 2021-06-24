#!/usr/bin/env python
# coding: utf-8


import os, random, sys, time
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from openpyxl import load_workbook
import time
import random
import re

""" Create Driver - You must provide the FULL file path as a sting type arguemtn to drvier = webdriver.Chrome"""

driver = webdriver.Chrome("/Users/apple/Documents/Scripts/LinkedIn/driver/chromedriver") 
driver.get("https://www.linkedin.com/uas/login") # Get Driver to open LinkedIn Login Page


def random_long_sleep(): # Random long sleep function (10-30 seconds) to emulate human behaviour
    time.sleep(random.randint(10,30))
    
def random_short_sleep(): # Random short sleep function (5-10 seconds) to emulate human behaviour
    time.sleep(random.randint(5,10)) 



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



def search(search_query): # Function to search a company name and then locate to the company section of the search

    linkedin_search_box = driver.find_element_by_xpath("//input[@aria-label='Search']") # Locate Search Box
    linkedin_search_box.send_keys(search_query) # Enter search query into search box
    random_short_sleep() # Short Sleep
    
    linkedin_search_box.send_keys(Keys.ENTER) # "Press" enter key
    
    random_short_sleep() # Short sleep
    
    linkedin_search_box.clear() # Clear search box
    
    try: # Try Click Companies button after search
        companies_button = driver.find_element_by_xpath('//button[@aria-label="Companies"]') # Locate Companies Button on search page
        companies_button.click() # Click Button
    except: # If button already clicked, pass
        pass

    random_short_sleep() # Sleep - Necessary to load the page fully before grabbing source code from search page
    


def get_url(): # Function url of top search result for searh query

    source = driver.page_source # Retrieve source code from search page
    soup = BeautifulSoup(source, "lxml") # Make soup object

    results = soup.find("div", {"class":'ph0 pv2 artdeco-card mb2'}) # Locate results list

    top_result = results.find("li", {"class":'reusable-search__result-container'}) # Locate Top Result
    
    if top_result != None:
        top_result_url = top_result.find("a")["href"] # Find the url associated with top result from search query
    else:
        top_result_url = driver.current_url
    
    return top_result_url # Return URL


"""Uncomment these three functions to run script with a chosen company name in the search function"""

# login("config.txt") # Run Login function

# search("company name here") # Search company name

# company_url = get_url() # Get company url from search



"""This function will iterate through a list of company names and return a list of all the urls for each company and
save a .txt file with the urls each on a new line"""

def get_url_list(company_name_list):

    company_url_list = [] # Empty list to store Company URLs

    for company in company_name_list: # Iterate companies
        
        search(company) # Search company
        
        random_long_sleep() # Random sleep time 10-30
        
        url = get_url() # get url through get_url()
        
        company_url_list.append(url) # Append url to list
        
        random_long_sleep() # Random sleep time 10-30

    file = open("company_url_file.txt", "w") # Create txt file
    for url in company_url_list: # Iterate urls
        file.write(url + "\n") # Write to list with new line
    file.close() # Close File

