# LinkedIn-Scraper

linkedin_company_url_maker.py - This script was used as part of an exercise for LinkedIn webscraping and it creates a .txt file of LinkedIn Company URLS



Please note that this requires previous download of selenium chromedriver and making a configuration file (config.txt) which contains LinkedIn username on line 1, and password on line 2.

The purpose of this is that (with the final function defined) one can pass a list of company names into the function and retrieve the urls for all of them.
It should be noted however that this will take a long time to run (approximately 10 hours for 500 companies in order to make the scraper "human like"

Currently in development is another script which will run through the URLs retrieved and retrieve data from each company - followers and number of employees etc.
