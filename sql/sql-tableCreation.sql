CREATE TABLE BrighterMonday_job_listings (
    id INT NOT NULL AUTO_INCREMENT,
    job_title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    job_location VARCHAR(255) NOT NULL,
    job_type VARCHAR(255) NOT NULL,
    job_salary VARCHAR(255) NOT NULL,
    job_function VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);