import gensim, os, pickle
from gensim.corpora import Dictionary
from gensim.similarities import WmdSimilarity



corpus_file = open(os.path.join(os.pardir, "keywords", "corpus.pkl"), 'rb')
corpus = pickle.load(corpus_file)
corpus_file.close()
sentences_file = open(os.path.join(os.pardir, "keywords", "sentences.pkl"), 'rb')
sentences = pickle.load(sentences_file)
sentences_file.close()

fname = os.path.join(os.pardir, "data", "mymodel")
model = gensim.models.Word2Vec.load(fname)
model.init_sims(replace=True)

num_best = 10
index = WmdSimilarity(corpus, model, num_best=10)

def set_shreshold(a, b):
    if a == b:
        return 0.52
    # elif a > 3 or b > 3:
    #     return 0.55 - 0.1 ** abs(a - b)
    return 0.55 - 0.05 ** abs(a - b)

i = 10
# sims = index[["flexible","multiple"]]
sims = index[corpus[i]]
print("query:")
print(corpus[i])
print(sentences[i])
print("sims:")
for j in range(num_best):
    shreshold = set_shreshold(len(corpus[i]), len(corpus[sims[j][0]]))
    print("shreshold: ", shreshold)
    if sims[j][1] >= shreshold:
        print("yes!")
    print(sims[j][0], sims[j][1])
    print(corpus[sims[j][0]])
    print(sentences[sims[j][0]])
    print()
