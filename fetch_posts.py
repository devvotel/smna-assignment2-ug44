"""
A data collection script for Assessment 2 for Social Media and Network Analytics (Sem 1 2026)

This script collects posts from Bluesky using the AT Protocol API (atproto library).
The posts are collected using 7 different keywords that are related to the Twitter discourse
and user migration from Twitter to Bluesky.
~2000 posts are collected for each keyword. Pagination had to be used, since the API limit is fetching 
100 posts per call.
The posts were filtered to English language only.
The fetched posts are saved to `data/posts.csv"
"""

from atproto import Client
import csv

client = Client()
client.login("[INSERT USER HANDLE]", "[INSERT APP PASSWORD]")

keywords = ["twitter", "elon", "twitter refugee", "bluesky vs twitter", "twitter is dead", "quit twitter", "miss twitter"]
counts = {}

fields = ['uri', 'author_handle', 'author_did', 'text', 'created_at', 
          'reply_count', 'repost_count', 'quote_count', 'like_count', 'is_reply', 
          'reply_parent', 'keyword']

with open ('data/posts.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fields)
    writer.writeheader()
    
    for kw in keywords:
        count = 0
        cursor = None
        while count < 2000:
            if cursor:
                params = {"q":kw, "lang":"en", "limit":100, "cursor":cursor}
            else:
                params = {"q":kw, "lang":"en", "limit":100}
            res = client.app.bsky.feed.search_posts(params)
            for post in res.posts:
                writer.writerow({
                    "uri":post.uri,
                    "author_handle":post.author.handle,
                    "author_did":post.author.did,
                    "text":post.record.text,
                    "created_at":post.record.created_at,
                    "reply_count": post.reply_count,
                    "repost_count":post.repost_count,
                    "quote_count":post.quote_count,
                    "like_count":post.like_count,
                    "is_reply": post.record.reply is not None,
                    "reply_parent": post.record.reply.parent.uri if post.record.reply else None,
                    "keyword":kw
                })
            count += len(res.posts)
            cursor = res.cursor
            print(f"{kw} : {len(res.posts)} collected")
            if not cursor:
                break


#res = client.app.bsky.feed.search_posts({"q":"elon musk", "lang":"en", "limit":10})
#print(res.posts[0])

#cursor = None
#for kw in keywords:
#    count = 0
#    while count <= 2000:
#        if cursor:
#            queryParams = {"q":kw, "limit":100, "lang":"en", "cursor":cursor}
#        else:
#            queryParams = {"q":kw, "limit":100, "lang":"en"}
#        res = client.app.bsky.feed.search_posts(queryParams)
#        count += len(res.posts)
#        cursor = res.cursor
#        if not cursor:
#            break
        