import os, random, sys, time, json
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from openpyxl import load_workbook
import re
import requests
import pandas as pd

"""Random Sleep Functions"""
def random_long_sleep(): # Random long sleep function (10-30 seconds) to emulate human behaviour
    time.sleep(random.randint(10,30))
    
def random_short_sleep(): # Random short sleep function (5-10 seconds) to emulate human behaviour
    time.sleep(random.randint(5,8)) 

def get_url_list(file_name):
    with open(file_name) as f:
        url_list = f.readlines()
    return url_list

        
def get_follower_count(url): # Get Follower Count from A Browser Source:
    driver.get(url)
    random_long_sleep()
    info_elements = driver.find_elements_by_xpath("//div[@class='org-top-card-summary-info-list__info-item']") 
    for element in info_elements:
        if "follower" in element.text:
            follower_count = int(element.text.split()[0].replace(",",""))
        else:
            pass

    random_short_sleep()

    if follower_count != None:
        pass
    else:
        follower_count = None
    return follower_count

def iterate_company_url_tocsv(company_url_list, filename): # Iterate Company url list and save as a csv fileyeh ex
    follower_count_list = []

    for url in company_url_list:
        print(f"Follower Count Currently being scraped for {url}:")
        follower_count = get_follower_count(url)
        print(f"The Follower Count is: {follower_count}")
        follower_count_list.append(follower_count)
    
    df = pd.DataFrame({"Follower Count":follower_count_list})
    df.to_csv(filename, index = False)

bankrupt_url_list = get_url_list("bankrupt file")
live_url_list = get_url_list("live file")

iterate_company_url_tocsv(bankrupt_url_list, "bankrupt_follower_count.csv")
iterate_company_url_tocsv(live_url_list, "live_follower_count.csv")