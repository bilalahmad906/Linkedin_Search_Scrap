# Import necessary modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up the Chrome WebDriver service
s = Service(r"C:\Drivers\chromedriver.exe")  # Adjust the path to your ChromeDriver

# URL of the website to scrape
url = "https://www.linkedin.com/jobs/search"  # Corrected URL

# Initialize the WebDriver
driver = webdriver.Chrome(service=s)
driver.get(url)

# Wait for the page to load
time.sleep(10)  # Adjust this sleep time if necessary

# Scroll to load more jobs
scroll_pause_time = 5
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Locate the job listing section
job_listings = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")

# Initialize lists to store the data
jd_list, cname_list, add_list, st_list, dt_list, link_list = [], [], [], [], [], []

# Loop through each job listing and extract the relevant data
for job in job_listings:
    try:
        # Extract Job Description
        job_description = job.find_element(By.CSS_SELECTOR, "span.sr-only").text.strip()
    except:
        job_description = "N/A"
    jd_list.append(job_description)

    try:
        # Extract Company Name
        company_name = job.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle").text.strip()
    except:
        company_name = "N/A"
    cname_list.append(company_name)

    try:
        # Extract Address
        address = job.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text.strip()
    except:
        address = "N/A"
    add_list.append(address)

    try:
        # Extract Job Status
        status = job.find_element(By.CSS_SELECTOR, "span.job-posting-benefits__text").text.strip()
    except:
        status = "N/A"
    st_list.append(status)

    try:
        # Extract Date Posted
        date_posted = job.find_element(By.CSS_SELECTOR, "time.job-search-card__listdate").text.strip()
    except:
        date_posted = "N/A"
    dt_list.append(date_posted)

    try:
        # Extract Job Link
        job_link = job.find_element(By.CSS_SELECTOR, "a.base-card__full-link").get_attribute('href')
    except:
        job_link = "N/A"
    link_list.append(job_link)

# Create a DataFrame with the extracted data
df = pd.DataFrame({
    "Job Description": jd_list,
    "Company": cname_list,
    "Address": add_list,
    "Status": st_list,
    "Date Posted": dt_list,
    "Job Link": link_list
})

# Export the DataFrame to a CSV file
df.to_csv("linkedinsearchdata.csv", index=False)

# Close the WebDriver
driver.quit()
