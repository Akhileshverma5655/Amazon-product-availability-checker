# Python script for Amazon product availability checker
# importing libraries
print("Program Started...")
from lxml import html
import requests
from time import sleep
import time
import schedule
import smtplib

# Email id for who want to check availability
receiver_email_id = "EMAIL_ID_OF_USER"

def check(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    
    # adding headers to show that you are
    # a browser who is sending GET request
    page = requests.get(url, headers = headers) 
    for i in range(20):
        # because continuous checks in 
        # milliseconds or few seconds
        # blocks your request
        sleep(3) 
        
        # parsing the html content
        doc = html.fromstring(page.content)
        
        # checking availability
        XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
        RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
        AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
        return AVAILABILITY

    
def sendemail(ans, product):
    GMAIL_USERNAME = "YOUR_GMAIL_ID"
    GMAIL_PASSWORD = "YOUR_GMAIL_PASSWORD"
    
    recipient = receiver_email_id
    body_of_email = ans
    email_subject = product + ' product availability'
    
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    
    # start TLS for security 
    s.starttls() 
    
    # Authentication 
    s.login(GMAIL_USERNAME, GMAIL_PASSWORD) 
    
    # message to be sent 
    headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                        "subject: " + email_subject,
                        "to: " + recipient,
                        "mime-version: 1.0",
                        "content-type: text/html"])

    content = headers + "\r\n\r\n" + body_of_email
    s.sendmail(GMAIL_USERNAME, recipient, content)
    s.quit() 


def ReadAsin():
    Asin1 = 'B0G2BLXG3B'
    url1= "https://www.amazon.in/dp/" + Asin1

    Asin2 = 'B0D2BMWZ31'
    url2 =  "https://www.amazon.in/dp/" + Asin2


    print("Processing:", url1 ,url2)

    ans1 = check(url1)
    ans2 = check(url2)
    print("Availability:", ans1 , ans2) 

# scheduling same code to run multiple
# times after every 1 minute 
def job():
    print("Tracking....") 
    ReadAsin()

schedule.every(1).minutes.do(job)

while True:
    
    # running all pending tasks/jobs
    schedule.run_pending() 
    time.sleep(1)