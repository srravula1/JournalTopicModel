import pandas as pd
from collections import defaultdict

import logging

logger = logging.getLogger("split-script")

chunksize = 10 ** 3
df_full = pd.read_csv("/home/project/data/AllArticles.csv", chunksize=chunksize, header=None)
journal_df = pd.read_csv("/home/project/data/journalslist.csv")

field_count = defaultdict(lambda : 0)

print("datasets loaded")

i = 0
for chunk in df_full:
    print("At chunk: {0}".format(i))
    df_chunked = chunk.iloc[:, [1, 2, 9, 10, 13]]
    df_chunked.columns = ["title", "author", "url", "abstract", "journal_id"]
    for id, row in df_chunked.iterrows():
        try:
            topics = journal_df[journal_df["journal_id"] == row["journal_id"]]["field"].values[0].split(";")
            for t in topics:
                field_count[t] += 1
        except:
            continue
    i += 1
print("Sorting and Printing")
import operator
sorted_x = sorted(field_count.items(), key=operator.itemgetter(1))
for x in sorted_x:
    print(x)
