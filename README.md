# LinkedIn-Scraper

These scripts were devised to scrape company data from linkedin - they are specific to the needs of scraping the follower count in such a way as not to be detected by LinkedIn anti-botting measures. This being said, the script could easily be repurporsed to scrape other company details.

linkedin_company_url_maker.py - This script was used as part of an exercise for LinkedIn webscraping and it creates a .txt file of LinkedIn Company URLS

follower_count_csv_maker.py - This script was used to follow on from the previous script and return a .csv file with the follower count for each company (this was subseuqently used as a variable in various machine learning models using R)

Please note that both scripts require previous download of selenium chromedriver and linkedin_company_url_maker.py requires one to make  a configuration file (config.txt) which contains LinkedIn username on line 1, and password on line 2 (for the function login("config.txt"). Furthermore, the specific code used in the function get_excel_column(), was specific to the excel spreadsheet used (data pulled from Pitchbook) and will require changes if this wishes to be used by anyone else.

