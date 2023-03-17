import re

from bs4 import BeautifulSoup
# from selenium import webdriver
import time
import requests

url = "https://www.brightermonday.co.ke/jobs/software-data"
page = requests.get(url)
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)

# driver.get(url)
# time.sleep(10)

# soup = BeautifulSoup(driver.page_source, 'html.parser')
soup = BeautifulSoup(page.content, 'html.parser')
job_listings = soup.find_all('div', class_='flex flex-grow-0 flex-shrink-0 w-full')

for job in job_listings:
    job_title = job.find('p', class_='text-lg font-medium break-words text-link-500').text.strip()
    job_link = job.find('a')['href']
    company_name = job.find('p', class_='text-sm text-link-500').text.strip()
    job_location = job.find('span',
                            class_='mb-3 px-3 py-1 rounded bg-brand-secondary-100 mr-2 text-loading-hide').text.strip()
    job_type = job.find_all('span', class_='mb-3 px-3 py-1 rounded bg-brand-secondary-100 mr-2 text-loading-hide')[
        1].text.strip()

    # job_date_element = job.find('p', class_='ml-auto text-sm font-normal text-gray-700 text-loading-animate')
    # if job_date_element:
    #     job_date = job_date_element.text.strip()
    # else:
    #     job_date = "N/A"

    time.sleep(2)
    date_element = job.find('p', class_='ml-auto text-sm font-normal text-gray-700 text-loading-animate')
    if date_element is not None:
        date_text = date_element.text.strip()
        date = re.search(r'\w+\s+\d{1,2},\s+\d{4}', date_text)
        if date is not None:
            date = date.group(0)
        else:
            date = ""
    else:
        date = ""

    job_function = job.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block').text.split(':')[
        1].strip()

    # print the extracted information
    print("Job Title: ", job_title)
    print("Job Link: ", job_link)
    print("Company Name: ", company_name)
    print("Job Location: ", job_location)
    print("Job Type: ", job_type)
    print("Job Salary: Confidential")
    print("Date Posted: ", date)
    print("Job Function: ", job_function)
    print("\n")

# driver.quit()
