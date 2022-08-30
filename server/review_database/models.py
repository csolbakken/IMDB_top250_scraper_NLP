from django.db import models


class Review(models.Model):

    id = models.IntegerField(primary_key=True)
    review = models.CharField(max_length=5000)


    def __str__(self):
        return(self.review)
    


