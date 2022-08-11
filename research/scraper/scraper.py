import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scraper_():
    
    ## Get IMDB 250 urls
    def get_urls():
        page = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
        html = BeautifulSoup(page.content, "html.parser")

        urls = []
        title_columns = html.find_all("td", class_="titleColumn")

        for title in title_columns:
            urls.append("https://www.imdb.com" + title.find("a")["href"])
            
        return urls
    
    ## Get first page of reviews (rating 1-10) for IMDB movies from urls
    def get_reviews(urls):
        review_data = {1: [],
                       2: [],
                       3: [],
                       4: [],
                       5: [],
                       6: [],
                       7: [],
                       8: [],
                       9: [],
                       10:[]}


        for m in range(len(urls)):

            for rating in range(1,11):
                url = urls[m] + "reviews?ratingFilter=" + str(rating)
                page = requests.get(url)
                html = BeautifulSoup(page.content, "html.parser")
                reviews = html.find_all("div", class_="text show-more__control")
                for review in reviews:
                    review_data[rating].append(review.text)


        ## Make DataFrame
        review_df = pd.DataFrame([])
        for i in range(1, 11):

            reviews = review_data[i]
            ratings = [i] * len(review_data[i])

            part = pd.DataFrame({"reviews":reviews, "ratings":ratings})
            review_df = pd.concat([review_df, part])

        review_df.reset_index(inplace=True)
        
        return review_df
    

    urls = get_urls()
    review_df = get_reviews(urls)
    
    review_df.to_csv("research/data/reviews_data.csv")
    
    
scraper_()
