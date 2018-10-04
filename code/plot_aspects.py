# import pandas as pd
# import numpy as np
# import re
import nltk

from gensim.models import word2vec

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import os

labels = []
tokens = []

fname = os.path.join(os.pardir, "data", "mymodel")
model = word2vec.Word2Vec.load(fname)
test_list = ["better", "faster", "performance"]

with open(os.path.join(os.pardir, "aspects", "keywords_filtered.txt"), "r") as f:
    for line in f:
        word = line.strip()
        if word in model:
            tokens.append(model[word])
            labels.append(word)


tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
new_values = tsne_model.fit_transform(tokens)

x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])

plt.figure(figsize=(16, 16))
for i in range(len(x)):
    plt.scatter(x[i],y[i])
    plt.annotate(labels[i],
                 xy=(x[i], y[i]),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom')
plt.show()
