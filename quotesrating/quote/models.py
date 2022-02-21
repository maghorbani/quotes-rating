from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Quote(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    average_score = models.FloatField(default=0)
    """
    This field is calculated using 'moving average' method, 
    since there is a massive number of ratings, by using this method
    the pain of calculating average will reduce to O(1) and one calculation on rate. 
    """

    def __str__(self):
        return self.title


def on_delete_user(collector, field, sub_objs, using):
    """
    This function is actually a pre-action to models.CASCADE
    it chages the moving average (Quote.average_score) befor deleting a user
    befor the user is deleted, the score assosiated between that user and 
    any Quote should be reduced from the average score, using moving average method
    """
    quote = sub_objs[0].quote
    ratings = quote.rate_set
    ratings_count = ratings.count()
    if(ratings_count < 2):
        quote.average_score = 0
    else:
        quote.average_score = (quote.average_score*ratings_count - sub_objs[0].score)/(ratings_count-1)
    quote.save()

    models.CASCADE(collector, field, sub_objs, using)


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=on_delete_user)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)

    score = models.IntegerField(default=0,validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])

    def __str__(self):
        return "{} rates {}/5 the quote {}".format(self.user.username, self.score, self.quote.title)