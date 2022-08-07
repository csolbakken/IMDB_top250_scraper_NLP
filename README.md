# IMDB web scraping and sentiment analysis with Python

## Web scraper
Using Requests, BeautifulSoup, RegEx and Pandas to extract movie data and user reviews from IMDB's top 250 movies.

## Sentiment analysis
Using scikit-learn's TF-IDF vectorizer to perform sentiment analysis on the scraped reviews. Hyperparameters tuned by cross validation with GridSearch.

## Upcoming features
<ul> 
    <li> Case study of one false positive and one false negative to understand better what confuses the model </li>
    <li> Deploy the model as a web app with Django </li>
</ul>

## Results

### Confusion Matrix
The dataset is imbalanced in favor of positive reviews. As the scraper only gets the reviews from one single page, the distribution of available reviews is dependent on the length of each review string. This indicates that positive reviews in general are much shorter than negative ones. This results in the model is biased towards predicting positive reviews:

#### Accuracy = True predictions / All predictions
Accuracy for bad reviews = 2593 / 3362 = 0.77 <br>
Accuracy for good reviews = 5439 / 5915 = 0.92

![Confuson Matrix](model/ConfusionMatrix.png "Confusion Matrix")



