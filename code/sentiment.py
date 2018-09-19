import os, pickle
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np


in_path = os.path.join(os.pardir, "aspects", "new_aspects.pkl")
relations_file = open(in_path, 'rb')
relations = pickle.load(relations_file)
relations_file.close()

keywords = set()
for topics in relations.values():
    for sets in topics.values():
        for _, relation, _, _, _ in sets:
            for word in relation.split():
                keywords.add(word)
print(len(keywords))
# out_path = os.path.join(os.pardir, "aspects", "keywords.txt")
# with open(out_path, 'a') as f:
#     for w in keywords:
#         f.write(w+"\n")
df = pd.DataFrame({'keywords': list(keywords)})
out_path = os.path.join(os.pardir, "aspects", "keywords.xlsx")
writer = ExcelWriter(out_path)
df.to_excel(writer,'Sheet1',index=False)
writer.save()
