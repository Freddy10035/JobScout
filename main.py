from bs4 import BeautifulSoup
import requests

url = "https://www.brightermonday.co.ke/jobs/software-data"

page = requests.get(url)
# print(page.content)
soup = BeautifulSoup(page.content, 'html.parser')

job_listings = soup.find_all('div', class_='flex flex-grow-0 flex-shrink-0 w-full')

for job in job_listings:
    job_title = job.find('p', class_='text-lg font-medium break-words text-brand-linked').text.strip()

    # extract the company name
    company_name = job.find('p', class_='text-sm text-brand-linked').text.strip()

    # extract the job location
    job_location = job.find('span', class_='mb-3 px-3 py-1 rounded bg-brand-opaque mr-2 text-loading-hide').text.strip()

    # extract the job type
    job_type = job.find_all('span', class_='mb-3 px-3 py-1 rounded bg-brand-opaque mr-2 text-loading-hide')[1].text.strip()

    # extract the job function
    job_function = job.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block').text.split(':')[1].strip()

    # print the extracted information
    print("Job Title: ", job_title)
    print("Company Name: ", company_name)
    print("Job Location: ", job_location)
    print("Job Type: ", job_type)
    print("Job Salary: Confidential")
    print("Job Function: ", job_function)
    print("\n")