from sklearn import metrics
import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


in_path = os.path.join(os.pardir, "evaluation", "clusters.xlsx")
df = pd.read_excel(in_path, sheetname='rsa&aes')

# a = df['our model']
# b = df['ground truth']
# a = list(a)
# print(type(a))
# print(a)

labels_true = df['our model']
labels_pred = df['ground truth']
labels_idf = []
labels_doc2vec = []

preds = (("model", labels_pred), ("idf", labels_idf), ("doc2vec", labels_doc2vec))


print("MI\tNMI\tAMI\tHOM\tCOM\tV-m\tFM-s")
for m, pred in preds:
    print(metrics.mutual_info_score(labels_true, pred),
          metrics.normalized_mutual_info_score(labels_true, pred),
          metrics.adjusted_mutual_info_score(labels_true, pred),
          metrics.homogeneity_completeness_v_measure(labels_true, pred),
          metrics.fowlkes_mallows_score(labels_true, pred)
          )
