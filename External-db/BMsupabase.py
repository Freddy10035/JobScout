import os
from bs4 import BeautifulSoup
import requests
import supabase

# Connect to Supabase database
supabase_url = '#'
supabase_key = '#'
supabase_client = supabase.create_client(supabase_url, supabase_key)

# Loop through all pages
for i in range(1, 46):  # scrape pages 1-45
    url = f"https://www.brightermonday.co.ke/jobs?page={i}"
    page = requests.get(url)
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

        # extract the job salary
        salary_span = job.find_all('span', class_='mb-3 px-3 py-1 rounded bg-brand-opaque mr-2 text-loading-hide')[-1]
        salary = salary_span.text.strip() if salary_span else "Confidential"

        # print the extracted information
        print("Job Title: {}\nCompany Name: {}\nJob Location: {}\nJob Type: {}\nJob Salary: {}\nJob Function: {}\n===============================================================".format(
                job_title, company_name, job_location, job_type, salary, job_function))

        # Check if job listing already exists in database
        sql = "SELECT job_title, company_name FROM BrighterMonday_job_listings WHERE job_title = %s AND company_name = %s"
        val = (job_title, company_name)
        result = supabase_client.from_table('BrighterMonday_job_listings').select('job_title, company_name').eq('job_title', job_title).eq('company_name', company_name).execute().get('data')

        if not result:
            # If job listing does not exist, insert into database
            insert_data = {
                'job_title': job_title,
                'company_name': company_name,
                'job_location': job_location,
                'job_type': job_type,
                'job_salary': salary,
                'job_function': job_function
            }
            supabase_client.from_table('BrighterMonday_job_listings').insert(insert_data).execute()

# close the Supabase connection
supabase_client.close()