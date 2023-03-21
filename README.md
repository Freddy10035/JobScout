# JobScout

JobScout is a Python bot that extracts job listings from the different job boards from plenty different categories. 
The bot uses the requests library to make a `HTTP GET` request to the job board website, and the `beautifulsoup4` library to parse the HTML response and extract the relevant information from the job listings.
The extracted information includes the `job title`, `company name`, `job location`, `job type`, `salary` and `job function`. The bot can be used to quickly gather job listing information for analysis or other purposes.

## Usage

To use this bot, simply run `main.py`. 
The output will be printed to the console and saved to your configures MySQL or PostgreSQL database.

## Dependencies

This project requires the following dependencies:

    beautifulsoup4
    requests
    mysql-connector-python
    psycopg2

## About

JobScout was created by [@Freddy10035](https://www.github.com/Freddy10035) as part of a project to help other developers and jobseekers get job alerts much faster. 
If you have any questions or suggestions, feel free to contact me [here](mailto:flaughters@gmail.com).

 
