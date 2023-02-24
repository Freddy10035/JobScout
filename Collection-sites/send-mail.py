import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Open the CSV file and read the contents
with open('/Users/SoftClansUser/Developments/csv/developer_jobs.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Create the email message
msg = MIMEMultipart()
msg['Subject'] = 'Job Listings'
msg['From'] = 'flaughters@gmail.com'
msg['To'] = '#'

# Create the body of the email using the CSV data
html = '<html><body><table>'
for row in data:
    html += '<tr>'
    for col in row:
        html += f'<td>{col}</td>'
    html += '</tr>'
html += '</table></body></html>'
msg.attach(MIMEText(html, 'html'))

# Connect to the SMTP server and send the email
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'flaughters@gmail.com'
smtp_password = '#'
with smtplib.SMTP(smtp_server, smtp_port) as smtp:
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
