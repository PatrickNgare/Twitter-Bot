from django.core.management.base import BaseCommand

import tweepy

from bot.models import TweetLookupBadWord,TweetLookupWord,TweetLookUpCoordinates
from bot.utils import get_auth_api,get_bearer_token

class MyStreamListener(tweepy.StreamingClient):

    def __init__(self):
        bearer_token=get_bearer_token()
        self.bad_words =list(TweetLookupBadWord.objects.values_list('Keyword',flat=True))
        super(MyStreamListener,self).__init__(bearer_token)
    

    def on_connect(self):

        print("Conected to twitter")

    def on_status(self,status):

        tweet_id=status.id
        if status.truncated:
            tweet_text=status.extended_tweet['full_text']

        else:
            tweet_text=status.text

        if not hasattr(status,"retweeted_status"):
            for bad_word in self.bad_words:
                if bad_word in tweet_text:
                    break
                else:
                    api=get_auth_api()
                    resp=api.create_favorite(tweet_id)
                    print(tweet_id)


    def on_error(sefl, status_code):

        if status_code==420:
            return False

class Command(BaseCommand):
    def handle(self,*args, **kwargs):
        try:
            filter_words=TweetLookupWord.objects.values_list('Keyword', flat=True)
            filter_location=TweetLookUpCoordinates.objects.values_list('value',flat=True)
            filter_location=[float(cor)for loc in filter_location for cor in loc.split(',')]
            api=get_auth_api()

            stream_listener=MyStreamListener()
            stream=tweepy.stream(auth=api.auth,lister=stream_listener,tweet_mode='extended')
            stream.filter(track=[filter_words],location=filter_location)
        except Exception as e:
            print(e)