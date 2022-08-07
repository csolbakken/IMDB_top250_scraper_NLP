import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def main():
    
    ## Get IMDB 250 urls
    def get_urls():
        page = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
        html = BeautifulSoup(page.content, "html.parser")

        urls = []
        title_columns = html.find_all("td", class_="titleColumn")

        for title in title_columns:
            urls.append("https://www.imdb.com" + title.find("a")["href"])
            
        return urls
    
    ## Get name, average rating and description of IMDB movies from urls
    def get_movie_data(urls):
        data = {
        "title":[],
        "rating": [],
        "description":[]
        }

        for url in urls:
            page = requests.get(url)
            html = BeautifulSoup(page.content, "html.parser")

            ## Get title
            title_html  = html.select("#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-c7f03a63-0.kUbSjY > section > div:nth-child(4) > section > section > div.sc-94726ce4-0.cMYixt > div.sc-94726ce4-2.khmuXj")
            for i in title_html:
                title = (i.find("h1")).text
            data["title"].append(title)

            ## Get rating
            rating_html = html.select_one("#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-c7f03a63-0.kUbSjY > section > div:nth-child(4) > section > section > div.sc-94726ce4-0.cMYixt > div.sc-db8c1937-0.eGmDjE.sc-94726ce4-4.dyFVGl > div > div:nth-child(1) > a > div > div > div.sc-7ab21ed2-0.fAePGh > div.sc-7ab21ed2-2.kYEdvH > span.sc-7ab21ed2-1.jGRxWM")
            data["rating"].append(rating_html.text)

            ## Get description
            desc_html = html.select_one("#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-c7f03a63-0.kUbSjY > section > div:nth-child(4) > section > section > div.sc-999e79a1-2.cFlWTV > div.sc-999e79a1-10.fgBNDS > div.sc-999e79a1-4.jrnPMn > div.sc-16ede01-8.hXeKyz.sc-999e79a1-11.fQLvsP > p > span.sc-16ede01-0.fMPjMP")
            if desc_html is not None:
                data["description"].append(desc_html.text) 
            else:
                data["description"].append(None)
                
            
            movie_data_df = pd.DataFrame.from_dict(data)
            
        return movie_data_df
    
    
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
    movie_data_df = get_movie_data(urls)
    review_df = get_reviews(urls)
    
    movie_data_df.to_csv("movie_data2.csv")
    review_df.to_csv("reviews_data2")
    
    
main()
        

    
    
