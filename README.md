# Developer-Jobs

The Developer Job Scraper is a Python web scraper that extracts job listings from the different job boards for the software/data and other relevant categories. 
The scraper uses the requests library to make a `HTTP GET` request to the job board website, and the `beautifulsoup4` library to parse the HTML response and extract the relevant information from the job listings.
The extracted information includes the job title, company name, job location, job type, and job function. The scraper can be used to quickly gather job listing information for analysis or other purposes.
## How to Use

To use this scraper, simply run `main.py`. 
The output will be printed to the console and saved to your configures MySQL or PostgresSQL database.

## Dependencies

This project requires the following dependencies:

    beautifulsoup4
    requests
    mysql-connector-python
    psycopg2

## About

The Developer Job Scraper was created by [ME!](www.github.com/Freddy10035) as part of a project to help other developers get job alerts much faster. 
If you have any questions or suggestions, feel free to contact me [here](mailto:flaughters@gmail.com).

 
