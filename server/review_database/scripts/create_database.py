from review_database.models import Review
import csv


def run():
    with open('/Users/clausanesorboesolbakken/Desktop/IMDB_top250_scraper_NLP/model/data/reviews_data.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Review.objects.all().delete()

        for row in reader:
            prediction = Review(
                        id = row[1],
                        review=row[2])
            prediction.save()

        print("Database Created")
run()