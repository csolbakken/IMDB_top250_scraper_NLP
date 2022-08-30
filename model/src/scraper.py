import requests
from bs4 import BeautifulSoup
import pandas as pd



def main():
    
    ## Get IMDB 250 urls
    def get_urls():
        page = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
        html = BeautifulSoup(page.content, "html.parser")

        urls = []
        title_columns = html.find_all("td", class_="titleColumn")

        for i in title_columns:
            urls.append("https://www.imdb.com" + i.find("a")["href"])
            
        return urls
    
    ## Get name, average rating and description of IMDB movies from urls
    def get_movie_data(urls):
        data = {
        "title":[],
        "rating": [],
        "description":[]
        }
        
        ## Define a header to only accept English reviews
        headers = {"Accept-Language": "en-US,en;q=0.5"}

        ## Looping through the urls to get the data
        for url in urls:     
            page = requests.get(url, headers=headers)
            html = BeautifulSoup(page.content, "html.parser")

            ## Get title
            title_html  = html.select_one("#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-80d4314-1.fbQftq > h1")
            if title_html is not None:
                data["title"].append(title_html.text)
            else:
                data["title"].append("Not available")

            ## Get rating
            rating_html = html.select_one("#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-2a827f80-2.kqTacj > div.sc-2a827f80-10.fVYbpg > div.sc-2a827f80-4.bWdgcV > div.sc-db8c1937-0.eGmDjE.sc-2a827f80-12.gOJseW > div > div:nth-child(1) > a > div > div > div.sc-7ab21ed2-0.fAePGh > div.sc-7ab21ed2-2.kYEdvH > span.sc-7ab21ed2-1.jGRxWM")
            
            if rating_html is not None:
                data["rating"].append(rating_html.text)
            else:
                data["rating"].append("Not available")

            ## Get description
            desc_html = html.select_one("#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-2a827f80-2.kqTacj > div.sc-2a827f80-10.fVYbpg > div.sc-2a827f80-4.bWdgcV > div.sc-16ede01-8.hXeKyz.sc-2a827f80-11.kSXeJ > p > span.sc-16ede01-2.gXUyNh")
            if desc_html is not None:
                data["description"].append(desc_html.text)
                
            else:
                data["description"].append("Not available")
        ## Make a PD dataframe from the data
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
    
    movie_data_df.to_csv("model/data/movie_data.csv")
    review_df.to_csv("model/data/reviews_data.csv")
    
    
main()