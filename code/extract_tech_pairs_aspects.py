# import community
import gensim, os, pickle
from gensim.corpora import Dictionary
from gensim.similarities import WmdSimilarity
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tag.stanford import CoreNLPPOSTagger
from nltk import download
import ssl


#Setting
default_distance = 0.45
pos_flag = True
if pos_flag:
    pos = "_pos"
else:
    pos = ""
pair = ("postgresql", "mysql")
# pair = ("udp", "tcp")
# pair = ("datamapper", "activerecord")
# pair = ("sortedlist", "sorteddictionary")
# Prepare POS tagger
pos_tag_set = {"JJR", "JJ", "NN", "NNS", "NNP", "NNPS"}


# Prepare stop words list
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
download('stopwords')
stop_words = stopwords.words('english')

# Prepare sentences
in_path = os.path.join(os.pardir, "data", "relations.pkl")
relations_file = open(in_path, 'rb')
relations = pickle.load(relations_file)
relations_file.close()
sentences = set()
for items in relations[pair]:
    sentences.add(items[5])
sentences = list(sentences)
l = len(sentences)
corpus = []
for sentence in sentences:
    if pos_flag:
        words = sentence.split()
        words[-1] = words[-1].strip()
        tagged_words = CoreNLPPOSTagger(url='http://localhost:9000').tag(words)
        if len(words) != len(tagged_words):
            tagged_words = pos_tag(words)
        words = []
        for (word, tag) in tagged_words:
            if word not in stop_words and word not in pair and tag in pos_tag_set:
                words.append(word)
        corpus.append(words)
    else:
        corpus.append([w for w in sentence.split() if w not in stop_words])

# temp_path = os.path.join(os.pardir, "communities", "distance.txt")

# Prepare word2vector model
fname = os.path.join(os.pardir, "data", "mymodel")
model = gensim.models.Word2Vec.load(fname)
model.init_sims(replace=True)

# Build weighted graph
G = nx.Graph()
# dictionary = Dictionary(corpus)
# bow_corpus = [dictionary.doc2bow(document) for document in corpus]
index = WmdSimilarity(corpus, model)
for i in range(l - 1):
    sims = index[corpus[i]]
    for j in range(i + 1, l):
        if sims[j] >= default_distance:
            if i not in G: G.add_node(i)
            if j not in G: G.add_node(j)
            G.add_edge(i, j, weight=sims[j])

out_path = os.path.join(os.pardir, "communities", "{}_{}_{}_{}{}.txt".format("&".join(pair), G.number_of_nodes(), l, default_distance, pos))
image_path = os.path.join(os.pardir, "communities", "{}_{}_{}_{}{}.png".format("&".join(pair), G.number_of_nodes(), l, default_distance, pos))
# G = nx.Graph()
# l = len(sentences)
# for i in range(l - 1):
#     for j in range(i + 1, l):
#         distance = - model.wmdistance(corpus[i], corpus[j])
#         if distance > - default_distance:
#             # if sentences[i] not in G: G.add_node(sentences[i])
#             # if sentences[j] not in G: G.add_node(sentences[j])
#             # G.add_edge(sentences[i], sentences[j], weight=distance)
#             if i not in G: G.add_node(i)
#             if j not in G: G.add_node(j)
#             G.add_edge(i, j, weight=distance)

# Draw graph
pos = nx.spring_layout(G)
plt.figure(figsize=(19,12))
plt.axis('off')
nx.draw_networkx_nodes(G, pos, node_size=50)
nx.draw_networkx_edges(G, pos, width=0.75)
plt.savefig(image_path)
# plt.show()

# Detect communities
communities_generator = community.girvan_newman(G)
top_level_communities = next(communities_generator)
# next_level_communities = next(communities_generator)
communities = sorted(map(sorted, top_level_communities))
# next_communities = sorted(map(sorted, next_level_communities))
num = 0
with open(out_path, "a") as out_file:
    for com in communities:
        out_file.write("{}---------------------------------------------------\n\n".format(num))
        for i in com:
            out_file.write(sentences[i]+"\n")
        num += 1
