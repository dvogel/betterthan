from django.contrib import admin
from tweeteater.models import TwitterUser, Tweet

class TwitterUserAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'created_at', 'name')
    search_fields = ('screen_name', 'name')

class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'text')
    search_fields = ('user', 'text')

admin.site.register(TwitterUser, TwitterUserAdmin)
admin.site.register(Tweet, TweetAdmin)
