import csv
from collections import defaultdict

with open ("data/posts.csv", "r", newline="", encoding="utf-8") as data:
    reader = csv.DictReader(data)
    kw_counts = defaultdict(int)
    for row in reader:
        kw_counts[row['keyword']] += 1
        
        
print (kw_counts)