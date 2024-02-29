import streamlit as st
import pandas as pd 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv 

def scrape_details(driver, href, text): #this function here scrappes and saves text from the results page of the tool bar
    data = {'href': href, 'text': text} #here trying to save the scrapped text and along with the link of results page which is different for every result 

    # Find potential data field 
    potential_fields = driver.find_elements(By.ID, "mainContentBox") #the target text you said to scrape kept changing with every result as it was a dynamic results so I used the tag to get the whole container itself

    # As the tool bar and its results were very complex for every entity found I tried to fetch whatever text shall be present on every result
    for field in potential_fields:
        if field.text.strip():
            field_type = field.get_attribute('mainContentBox')
            data[field_type] = field.text

    return data

def search_and_save(search_term): #this is the main driver function which goes to the tool bar and interacts with it...
    url = 'https://sanctionssearch.ofac.treas.gov/'
    with webdriver.Chrome() as driver:
        driver.get(url)

        name_field = driver.find_element(By.ID, "ctl00_MainContent_txtLastName") #the data can be accessed only if we would search and inspect the names and ref links along with it
        name_field.send_keys(search_term) #with selenium interact with the website
        submit_button = driver.find_element(By.ID, "ctl00_MainContent_btnSearch") #clicking the search button with its id for getting the results
        submit_button.click()
        driver.implicitly_wait(15) #putting a bit of wait time over here for it to type any word in search bar and hit search get results so the scrapping could begin afterwards as the data is loaded dynamically

        links = driver.find_elements(By.XPATH, '//*[@id="gvSearchResults"]//a') #here along with the name field in tool bar there will be a link clicking this link a new page is loaded which has all the data precisely unlike in the results shown initially
        results = []

        for link in links: #this loop goes around fetches every link they had href before the name and <a> tags so....xpath address
            href = link.get_attribute('href')
            text = link.text

            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform() #this selenium function clicks on the link to load the new page
            #this code inside the loop opens the search result into new window then it scrapes data through the function designed earlier from the new window's link then it brings the scrapper back to main page and continues with every other link
            driver.switch_to.window(driver.window_handles[-1])
            results.append(scrape_details(driver, href, text))#scrapes using the function designed above from the links opened in new page
            driver.close() 
            driver.switch_to.window(driver.window_handles[0])

    return results

st.title("Sanctions Search")
user_input = st.text_input("Enter the last name to search (e.g., 'b'):")

if st.button("Search"):
    results = search_and_save(user_input)

    if results:
        df = pd.DataFrame(results) 
        st.dataframe(df) 
        st.download_button("Download CSV", df.to_csv(), file_name='search_results.csv') 
    else:
        st.write("No results found.")
