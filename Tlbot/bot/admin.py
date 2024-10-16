from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(TweetLookupWord)
admin.site.register(TweetLookupBadWord)
admin.site.register(TweetLookUpCoordinates)
admin.site.register(OutBoundDirectMessage)
admin.site.register(lastFollower)
admin.site.register(inboundDirectMessages)