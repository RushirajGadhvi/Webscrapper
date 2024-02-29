# Webscrapper
#This Python code implements a web scraper designed specifically for the OFAC Sanctions Search website. It leverages the Streamlit library to create a simple user interface where a last name can be entered. Using Selenium, the code automates interactions with the website: it enters the search term, clicks the search button, and navigates through the search results.  For each result, it extracts the link and accompanying text, and potentially scrapes additional details from individual result pages by opening them in new tabs. The collected data is then organized into a Pandas DataFrame and presented within the Streamlit interface, also offering the option to download the results as a CSV file.

Step 1: clone
git clone https://github.com/RushirajGadhvi/Webscrapper.git


