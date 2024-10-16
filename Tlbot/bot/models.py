from django.db import models

# Create your models here.
class TweetLookupWord(models.Model):

    Keyword=models.CharField(max_length=255)

class TweetLookupBadWord(models.Model):

    Keyword=models.CharField(max_length=255)
 
class TweetLookUpCoordinates(models.Model):
    value=models.TextField()

class OutBoundDirectMessage(models.Model):
    message=models.TextField()


class lastFollower(models.Model):
    last_follower=models.PositiveBigIntegerField()


class inboundDirectMessages(models.Model):

    sender=models.CharField(max_length=255)    
    message=models.TextField()
    sent_on=models.DateTimeField()       