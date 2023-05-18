import re
import textwrap
from bs4 import BeautifulSoup
import requests

url = "https://www.brightermonday.co.ke/jobs/medical-pharmaceutical"
page = requests.get(url)

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

    job_page = requests.get(job_link)
    job_soup = BeautifulSoup(job_page.content, 'html.parser')

    # job_summary = job_soup.find('p', class_='mb-4 text-sm text-gray-500').text.strip()
    job_summary = str(job_soup.find('p', class_='mb-4 text-sm text-gray-500'))

    # job_summary = textwrap.indent(job_summary, " " * 10)  # indent the job summary with 4 spaces

    # job_requirements = job_soup.find('div', class_='text-sm text-gray-500').text.strip()
    job_requirements = str(job_soup.find('div', class_='text-sm text-gray-500'))

    # job_requirements = textwrap.indent(job_requirements, " " * 10)  # indent the job requirements with 4 spaces

    # qualifications_experience = job_soup.find('ul', class_='pl-5 text-sm list-disc text-gray-500').text.strip()

    min_qualification = job_soup.find('span', string='Minimum Qualification:').find_next_sibling('span').text
    experience_level = job_soup.find('span', string='Experience Level:').find_next_sibling('span').text
    experience_length = job_soup.find('span', string='Experience Length:').find_next_sibling('span').text

    print("Job Title: ", job_title)
    print("Job Link: ", job_link)
    print("Company Name: ", company_name)
    print("Job Location: ", job_location)
    print("Job Type: ", job_type)
    print("Job Salary: Confidential")
    print("Date Posted: ", date)
    print("Job Function: ", job_function)
    print("Job Summary: \n", job_summary)
    print("Minimum Qualification:", min_qualification)
    print("Experience Level:", experience_level)
    print("Experience Length:", experience_length)
    print("Job Requirements/Description: \n", job_requirements)
    print("\n")
    print("==========================================================================")