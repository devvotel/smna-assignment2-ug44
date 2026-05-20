import csv
from collections import defaultdict
import pandas

with open ("data/posts.csv", "r", newline="", encoding="utf-8") as data:
    reader = csv.DictReader(data)
    kw_counts = defaultdict(int)
    for row in reader:
        kw_counts[row['keyword']] += 1
        
total = 0
for key in kw_counts:
    if kw_counts[key] != 0:
        total += kw_counts[key]


print (kw_counts)
print(total)

df = pandas.read_csv("data/posts.csv")
print(f"Total posts: {len(df)}")
print(f"Duplicates: {df['uri'].duplicated().sum()}")
print(f"Is reply True: {df['is_reply'].sum()}")
print(f"Is reply False: {(df['is_reply'] == False).sum()}")
print(f"\nReply count stats:")
print(df['reply_count'].describe())