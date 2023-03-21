CREATE TABLE BrighterMonday (
    id INT NOT NULL AUTO_INCREMENT,
    job_title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    job_location VARCHAR(255) NOT NULL,
    job_type VARCHAR(255) NOT NULL,
    job_salary VARCHAR(255) NOT NULL,
    job_function VARCHAR(255) NOT NULL,
    date_posted VARCHAR(255) NOT NULL,
    job_link VARCHAR(255) NOT NULL,
    job_summary TEXT,
    min_qualifications TEXT,
    experience_level VARCHAR(255),
    experience_length VARCHAR(255),
    job_requirements TEXT,
    PRIMARY KEY (id)
);
