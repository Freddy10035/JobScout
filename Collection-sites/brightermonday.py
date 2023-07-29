import re
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Get environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL database
mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

# Create cursor object
my_cursor = mydb.cursor()

# Check if the table exists, and create it if it doesn't
table_name = "BrighterMonday"
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        job_title VARCHAR(255),
        company_name VARCHAR(255),
        job_location VARCHAR(255),
        job_type VARCHAR(50),
        job_salary DECIMAL(10, 2),
        job_function VARCHAR(255),
        date_posted DATE,
        job_link VARCHAR(255),
        job_summary TEXT,
        min_qualifications TEXT,
        experience_level VARCHAR(50),
        experience_length VARCHAR(50),
        job_requirements TEXT,
        created_on DATETIME
    )
"""
my_cursor.execute(create_table_query)

# # Ask user for job function to search for
# search_function = input("Enter the job function you want to search for: ")

# Define the list of job functions to choose from
job_functions = ['All Jobs', 'Accounting, Auditing & Finance', 'Admin & Office', 'Building & Architecture',
                 'Community & Social Services', 'Consulting & Strategy', 'Creative & Design',
                 'Customer Service & Support', 'Driver & Transport Services', 'Engineering & Technology',
                 'Estate Agents & Property Management', 'Farming & Agriculture', 'Food Services & Catering',
                 'Health & Safety', 'Hospitality & Leisure', 'Human Resources', 'Legal Services',
                 'Management & Business Development', 'Marketing & Communications', 'Medical & Pharmaceutical',
                 'Product & Project Management', 'Quality Control & Assurance ', 'Research, Teaching & Training',
                 'Sales', 'Software & Data', 'Supply Chain & Procurement', 'Trades & Services']

# Prompt the user to choose a job function
print("Please choose a job function:")
for i, job_function in enumerate(job_functions):
    print(f"{i}. {job_function}")
print("\n")
selection = input("Enter the number of the job function you want to search for: \n")

print("\n")
print("====================================================================================")

# Convert the selection to an integer and use it to select the job function
selection = int(selection)
if selection == 0:
    search_function = 'All Jobs'
    print(f"You have chosen to search for '{search_function}'.")
elif 1 <= selection <= len(job_functions):
    search_function = job_functions[selection]
    print(f"You have chosen to search for '{search_function}' job function.")
else:
    print("Invalid selection.")


print("====================================================================================")

# Convert the selection to an integer and use it to select the job function
search_function = int(selection)

# Flag to keep track if any jobs were found for the search function
found_jobs = False

# Delay the execution of the script for 5 seconds to allow the website to load
# time.sleep(10)

# Loop through all pages
for i in range(1, 46):  # scrape pages 1-45
    url = f"https://www.brightermonday.co.ke/jobs?page={i}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    BrighterMonday_job_listings = soup.find_all('div', class_='flex flex-grow-0 flex-shrink-0 w-full')

    for job in BrighterMonday_job_listings:
        job_function = job.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block').text.split(':')[
            1].strip()
        # if search_function.lower() in job_function.lower():
        # if job_function.lower().startswith(job_functions[search_function].lower()):
        if selection == 0 or job_function.lower().startswith(job_functions[selection].lower()):

            found_jobs = True
            job_title = job.find('p', class_='text-lg font-medium break-words text-link-500').text.strip()

            # extract the job link
            job_link = job.find('a')['href']

            # extract the company name
            company_name = job.find('p', class_='text-sm text-link-500').text.strip()

            # extract the job location
            job_location = job.find('span',
                                    class_='mb-3 px-3 py-1 rounded bg-brand-secondary-100 mr-2 text-loading-hide').text.strip()

            # extract the job type
            job_type = job.find_all('span', class_='mb-3 px-3 py-1 rounded bg-brand-secondary-100 mr-2 text-loading-hide')[
                1].text.strip()

            # extract the job date posted
            date_element = job.find('p', class_='ml-auto text-sm font-normal text-gray-700 text-loading-animate')
            if date_element is not None:
                date_text = date_element.text.strip()
                date_posted = re.search(r'\w+\s+\d{1,2},\s+\d{4}', date_text)
                if date_posted is not None:
                    date = date_posted.group(0)
                else:
                    date_posted = ""
            else:
                date_posted = ""

            # extract the job function
            job_function = \
                job.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block').text.split(':')[
                    1].strip()

            # extract the job salary
            salary_span = job.find_all('span', class_='mb-3 px-3 py-1 rounded bg-brand-secondary-100 mr-2 text-loading-hide')[
                -1]
            salary = salary_span.text.strip() if salary_span else "Confidential"

            job_page = requests.get(job_link)
            job_soup = BeautifulSoup(job_page.content, 'html.parser')

            job_summary = job_soup.find('p', class_='mb-4 text-sm text-gray-500').text.strip()
            # job_summary = str(job_soup.find('p', class_='mb-4 text-sm text-gray-500'))
            # job_summary = textwrap.indent(job_summary, " " * 10)  # indent the job summary with 4 spaces

            job_requirements = job_soup.find('div', class_='text-sm text-gray-500').text.strip()
            # job_requirements = str(job_soup.find('div', class_='text-sm text-gray-500'))
            # job_requirements = textwrap.indent(job_requirements, " " * 10)  # indent the job requirements with 4 spaces

            # qualifications_experience = job_soup.find('ul', class_='pl-5 text-sm list-disc text-gray-500').text.strip()

            min_qualification = job_soup.find('span', string='Minimum Qualification:').find_next_sibling('span').text
            experience_level = job_soup.find('span', string='Experience Level:').find_next_sibling('span').text
            experience_length = job_soup.find('span', string='Experience Length:').find_next_sibling('span').text

            # print the extracted information
            print(
                "\nJob Title: {}\nCompany Name: {}\nJob Location: {}\nJob Type: {}\nJob Salary: {}\nJob Function: {}\nDate Posted: {}\nJob Link: {}\nJob Summary: {}\nMinimum Qualification: {}\nExperience Level: {}\nExperience Length: {}\n\n===============================================================".format(
                    job_title, company_name, job_location, job_type, salary, job_function, date_posted, job_link, job_summary, min_qualification, experience_level, experience_length))

            # Check if job listing already exists in database
            sql = "SELECT job_title, company_name FROM BrighterMonday WHERE job_title = %s AND company_name = %s"
            val = (job_title, company_name)
            my_cursor.execute(sql, val)
            result = my_cursor.fetchone()

            # Fetch any unread results from the SELECT query
            my_cursor.fetchall()

            try:
                # If job listing does not exist, insert into database
                if not result:
                    # Insert data into MySQL database
                    created_on = datetime.now()
                    sql = "INSERT INTO BrighterMonday (job_title, company_name, job_location, job_type, job_salary, job_function, date_posted, job_link, job_summary, min_qualifications, experience_level, experience_length, job_requirements, created_on) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (job_title, company_name, job_location, job_type, salary, job_function, date_posted, job_link, job_summary, min_qualification, experience_level, experience_length, job_requirements, created_on)

                    my_cursor.execute(sql, val)

                    # Commit changes to database
                    mydb.commit()
            except mysql.connector.errors.InternalError as e:
                if "Unread result found" in str(e):
                    # fetch any unread results before executing another query
                    my_cursor.fetchall()
                    mydb.commit()
                else:
                    raise e

if not found_jobs:
    print(f"No job listings found for the job function '{search_function}'")

# close the database connection
my_cursor.close()
mydb.close()
