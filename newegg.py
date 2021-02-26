from bs4 import BeautifulSoup 
import requests, os, datetime
from time import time, sleep

file_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

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

def main(URL):
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)','Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(URL, headers=HEADERS) 
    soup = BeautifulSoup(webpage.content, "lxml")

    #title
    try:
        title = soup.find("h1", attrs={"class": 'product-title'}) 
        title_string = str(title.string).strip()
        title_string = bcolors.BOLD + title_string + bcolors.ENDC
    except AttributeError: 
        title_string = bcolors.FAIL + "NA" + bcolors.ENDC
    print(title_string)

    #price
    try:
        price = soup.find("li", attrs={"class":"price-current"})
        full_price = price.strong.text + price.sup.text
    except AttributeError:
        price = bcolors.FAIL + "NA" + bcolors.ENDC
    print(full_price)

    #instock
    try:
        instock = soup.find("div", attrs={"class":"product-inventory"})
        instock = str(instock.strong.text).strip()
        if "OUT" in instock:
            instock = bcolors.FAIL + instock + bcolors.ENDC
        else:
            instock = bcolors.OKGREEN + instock + bcolors.ENDC
            log.write("In stock: " + datetime.now())
    except AttributeError:
        instock = bcolors.FAIL + "NA" + bcolors.ENDC
    print(instock)    

if __name__ == '__main__':
    while True:
        url = open(file_location + "/url.txt","r")
        log = open(file_location + "/log.txt","a+")
        for links in url.readlines():
            main(links)
        sleep(60 - time() % 60)