import os, pickle
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np


in_path = os.path.join(os.pardir, "aspects", "new_aspects.pkl")
relations_file = open(in_path, 'rb')
new_aspects = pickle.load(relations_file)
relations_file.close()


def import_to_excel(pair):
    keywords = []
    sentences = []
    for key, values in new_aspects[pair].items():
        keywords.append(", ".join(key.split()))
        for v in values:
            keywords.append("")
            sentences.append(v[4])
        keywords = keywords[:-1]
    df = pd.DataFrame({'Keywords': keywords,
                       'Sentences': sentences})
    out_path = os.path.join(os.pardir, "old_communities", "{}.xlsx".format("&".join(pair)))
    writer = ExcelWriter(out_path)
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()

# pairs = [("3des", "aes"), ("png", "bmp"), ("g++", "gcc"), # < 10
#          ("postgresql", "mysql"), ("udp", "tcp"), # >100
#          ("quicksort", "mergesort"), # 50 ~ 100
#          ("vmware", "virtualbox"), ("datamapper", "activerecord"), ("sortedlist", "sorteddictionary"), # 10 ~ 15
#          ("testng", "junit"), ("jruby", "mri"), # 15 ~ 20
#          ("compiled-language", "interpreted-language"), ("google-chrome", "safari"), ("heapsort", "quicksort")] #20 ~ 50
# pairs = {("google-chrome", "firefox"), ("post", "get"), ("innodb", "myisam")}


# for pair in pairs:
#     import_to_excel(pair)
pair = ("post", "get")
import_to_excel(pair)
