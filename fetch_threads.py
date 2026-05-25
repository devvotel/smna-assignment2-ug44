"""
A reply thread collection script.

This script fetches reply threads for the 20 most-replied to posts from the posts.csv dataset - 
10 of them are top 10 most replied to posts overall and 10 are specifically from the "bluesky vs twitter"
keyword. The threads are fetched using the getPostThread function of the atproto library with 
a depth of 1000 (which is the max value) in order to capture as many nested reply chains as we can.

get_edges() recursively loops through the entire tree and extracts a directed edge for each reply relationship
(from replier to the recipient). Every edge includes the text and the metadata of both the reply and 
its parent post.

Output is saved in "edges.csv" in the data folder.
"""


from atproto import Client
import csv


def get_edges(thread, edges: list):
    post = thread.post
    current_did = post.author.did
    current_handle = post.author.handle
    current_text = post.record.text
    current_created_at = post.record.created_at
    if thread.replies:
        for reply in thread.replies:
            if hasattr(reply, 'post'):
                reply_did = reply.post.author.did
                reply_handle = reply.post.author.handle
                reply_text = reply.post.record.text
                reply_created_at = reply.post.record.created_at

                edges.append({
                    'from_did': reply_did,
                    'from_handle': reply_handle,
                    'from_text': reply_text,
                    'from_created_at': reply_created_at,
                    'to_did': current_did,
                    'to_handle': current_handle,
                    'to_text': current_text,
                    'to_created_at': current_created_at
                })

                get_edges(reply, edges)

posts_of_interest = ['at://did:plc:xyddpg6usmgh2t2jgf4e37yk/app.bsky.feed.post/3mhvfinvcgc2q', 'at://did:plc:ul5n745uxwymqppvpiwtpoa5/app.bsky.feed.post/3mkej7zyfnk2h', 'at://did:plc:5mqpgxjffcckasqv7h6g7itu/app.bsky.feed.post/3m3crrs6ark2y', 'at://did:plc:tsf3qulwq25yo27j6eznkfix/app.bsky.feed.post/3mc2crp2ahc27', 'at://did:plc:4q4ziw4qk2hxxaxfu7jweuey/app.bsky.feed.post/3mmak4a4rns2k', 'at://did:plc:ji7lroxun3yvv2pxhcf7jqsn/app.bsky.feed.post/3mmagsxpukq22', 'at://did:plc:37ukqjgnt2puqbdvxo6jw4le/app.bsky.feed.post/3mmafhs4fws2z', 'at://did:plc:t4i3a4fawuzge3dsw2i2h2fw/app.bsky.feed.post/3mbhvqutprk2a', 'at://did:plc:t46sqvutibvsmjgwn6r6izve/app.bsky.feed.post/3ltfs7bk3js2i', 'at://did:plc:dy4mk6ej5d7hlqgfeqjft3hd/app.bsky.feed.post/3mcnhpj3qj22j', 'at://did:plc:t46sqvutibvsmjgwn6r6izve/app.bsky.feed.post/3ltfs7bk3js2i', 'at://did:plc:3iwge6tzr76tkt6xdwyfs6mr/app.bsky.feed.post/3mf5ta52w7c2p', 'at://did:plc:jimtocu7irkkkupvh7g34rhs/app.bsky.feed.post/3lkvp53pxvk27', 'at://did:plc:rkfwqt5jedajtdnkx5kvedfo/app.bsky.feed.post/3mc4otj3ihk2p', 'at://did:plc:4vrssqepg6uj4tj5us7tnfgt/app.bsky.feed.post/3mb3z33qfvs25', 'at://did:plc:psxf6wrijwkudvi2etmxsess/app.bsky.feed.post/3lrui5beqrc22', 'at://did:plc:sgti3jsgu3luif24tokvth3a/app.bsky.feed.post/3lcjqkmtqfk23', 'at://did:plc:kyphkmluigfakab42kfn5ri2/app.bsky.feed.post/3lzdqczgivc2p', 'at://did:plc:cak4klqoj3bqgk5rj6b4f5do/app.bsky.feed.post/3ltpjfotlv22s', 'at://did:plc:slwpvr5uwq7dqv4nur35dlji/app.bsky.feed.post/3lr6y3qtqfc23']

client = Client()
client.login("[INSERT USER HANDLE]", "[INSERT APP PASSWORD]")


test_thread = client.get_post_thread(posts_of_interest[11])
with open("data/thread_sample.txt", "w", encoding="utf-8") as f:
    f.write(f"{test_thread}")
    f.close()

fields = ['from_did', 'from_handle', 'from_text', 'from_created_at', 
          'to_did', 'to_handle', 'to_text', 'to_created_at']

with open("data/edges.csv", "w", newline="", encoding = "utf-8") as csvf:
    writer = csv.DictWriter(csvf, fieldnames=fields)
    writer.writeheader()
    for uri in posts_of_interest:
        try:
            thread = client.get_post_thread(uri=uri, depth=1000, parent_height=0)
            edges = []
            get_edges(thread.thread, edges)
            writer.writerows(edges)
            print(f"Got {len(edges)}")
        except Exception as e:
            print(f"Error: {e}")
