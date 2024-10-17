from django.core.management.base import BaseCommand
import tweepy
from bot.models import TweetLookupBadWord, TweetLookupWord, TweetLookUpCoordinates
from bot.utils import get_bearer_token

class MyStreamListener(tweepy.StreamingClient):
    def __init__(self):
        # Fetch the bearer token from the settings via utility function
        bearer_token = get_bearer_token()
        super(MyStreamListener, self).__init__(bearer_token)

        # Fetch bad words from the database to filter tweets
        self.bad_words = list(TweetLookupBadWord.objects.values_list('Keyword', flat=True))

    def on_connect(self):
        print("Connected to Twitter stream")

    def on_tweet(self, tweet):
        tweet_id = tweet.id
        tweet_text = tweet.text

        if not hasattr(tweet, "retweeted_status"):
            if not any(bad_word in tweet_text for bad_word in self.bad_words):
                # Here you can interact with the tweet, such as liking it
                print(f"Favorited tweet: {tweet_id}")

    def on_error(self, status_code):
        if status_code == 420:
            return False  # Disconnects the stream if rate-limited
        else:
            print(f"Error occurred: {status_code}")

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            # Get filter words and locations from the database
            filter_words = list(TweetLookupWord.objects.values_list('Keyword', flat=True))
            filter_location = TweetLookUpCoordinates.objects.values_list('value', flat=True)

            # Initialize the stream listener with the bearer token
            stream_listener = MyStreamListener()

            # Add rules for filtering by keywords
            for word in filter_words:
                stream_listener.add_rules(tweepy.StreamRule(value=word))

            # Optionally, add location-based filtering if supported by your access level
            # Twitter API v2 does not provide location filtering directly; you may need to process the tweet manually.
            
            # Connect to the Twitter stream
            stream_listener.connect()

        except Exception as e:
            print(f"An error occurred: {e}")
