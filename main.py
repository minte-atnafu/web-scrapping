import requests 
from bs4 import BeautifulSoup
import pandas as pd

current_page = 1

proceed = True

data = []

while(proceed):
    print("Currenlt scraping page: "+str(current_page))

    # these is the url where the data is found in code format
    url = "https://books.toscrape.com/catalogue/page-"+str(current_page)+".html"
    # get method used to take everything on the website 
    page = requests.get(url)
    # beautifullSoup used for parsing mare html code 
    soup = BeautifulSoup(page.text,"html.parser")
    # try to tell the scraping to stop somewhere "404 Not Found"
    if soup.title.text == "404 Not Found":
        proceed = False

    else:
        # class are esentials in selecting the target information
        all_books = soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3") 
        for book in all_books:
            item = {}
            item['Title'] = book.find("img").attrs["alt"]

            item['Link'] = book.find("a").attrs["href"]

            item['Price'] =  book.find("p", class_="price_color").text[2:]
            item['Stock'] = book.find("p", class_= "instock availability").text.strip()

            data.append(item)

    current_page+=1 
# for organizing the scraped data in to tabular form
df = pd.DataFrame(data)
df.to_excel("books.xlsx")
df.to_csv("books.csv")        
     