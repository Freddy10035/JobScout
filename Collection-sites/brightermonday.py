from bs4 import BeautifulSoup
import requests
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="freddie",
    password="freddie10035",
    database="developer_jobs"
)

# Create cursor object
my_cursor = mydb.cursor()

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
            job_title = job.find('p', class_='text-lg font-medium break-words text-brand-linked').text.strip()

            # extract the company name
            company_name = job.find('p', class_='text-sm text-brand-linked').text.strip()

            # extract the job location
            job_location = job.find('span',
                                    class_='mb-3 px-3 py-1 rounded bg-brand-opaque mr-2 text-loading-hide').text.strip()

            # extract the job type
            job_type = job.find_all('span', class_='mb-3 px-3 py-1 rounded bg-brand-opaque mr-2 text-loading-hide')[
                1].text.strip()

            # extract the job date posted
            # job_date_posted = job.find('p', class_='ml-auto text-sm font-normal text-gray-700 text-loading-animate').text.strip()

            # extract the job function
            job_function = \
                job.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block').text.split(':')[
                    1].strip()

            # extract the job salary
            salary_span = job.find_all('span', class_='mb-3 px-3 py-1 rounded bg-brand-opaque mr-2 text-loading-hide')[
                -1]
            salary = salary_span.text.strip() if salary_span else "Confidential"

            # print the extracted information
            print(
                "\nJob Title: {}\nCompany Name: {}\nJob Location: {}\nJob Type: {}\nJob Salary: {}\nJob Function: {}\n\n===============================================================".format(
                    job_title, company_name, job_location, job_type, salary, job_function))

            # Check if job listing already exists in database
            sql = "SELECT job_title, company_name FROM BrighterMonday_job_listings WHERE job_title = %s AND company_name = %s"
            val = (job_title, company_name)
            my_cursor.execute(sql, val)
            result = my_cursor.fetchone()

            # Fetch any unread results from the SELECT query
            my_cursor.fetchall()

            try:
                # If job listing does not exist, insert into database
                if not result:
                    # Insert data into MySQL database
                    sql = "INSERT INTO BrighterMonday_job_listings (job_title, company_name, job_location, job_type, job_salary, job_function) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (job_title, company_name, job_location, job_type, salary, job_function)

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
