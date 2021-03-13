from bs4 import BeautifulSoup 
import requests, os, datetime, smtplib
from time import time, sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

file_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
load_dotenv()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def send_mail(URL):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    mail_content = "One of your selected items are in stock at " + str(datetime.datetime.now()) + "\n\n\n" + URL
    #The mail addresses and password
    sender_address = os.getenv('SENDER_ADDRESS')
    sender_pass = os.getenv('SENDER_PASS')
    receiver_address = os.getenv('RECEIVER_ADDRESS')
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] =  "One of your selected items are in stock"   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

def main(URL):
    HEADERS = ({'User-Agent': 'Mozilla/5.0'})
    webpage = requests.get(URL, headers=HEADERS) 
    soup = BeautifulSoup(webpage.content, "lxml")
    try:
        resp = ""
        title = str(soup.find("title").string)
        resp = bcolors.UNDERLINE + title + bcolors.ENDC
        print(resp)

    except AttributeError:
        print ("Something went wrong")

    try:
        resp = ""
        instock = str(soup.findAll("script", attrs={"type":"application/ld+json"}))
        if "http://schema.org/InStock" in instock:
            resp = bcolors.OKGREEN + "In stock" + bcolors.ENDC
            send_mail(URL)
            log.write("In stock: " + str(datetime.datetime.now()) + " " + URL + "\n")
            
        else:
            resp = bcolors.FAIL + "Out of stock" + bcolors.ENDC
        print(resp)

    except AttributeError:
        print ("Something went wrong")
    
if __name__ == '__main__':
    while True:
        url = open(file_location + "/bestbuy_urls.txt","r")
        log = open(file_location + "/bestbuy_log.txt","a+")

        for links in url.readlines():
            main(links)
        sleep(60 - time() % 60)