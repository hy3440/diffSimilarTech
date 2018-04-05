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
flag = False # all sentences
f = "2"
default_distance = 0.5
pos_flag = True
if pos_flag:
    pos = ""
else:
    pos = "_without_pos_"
# pair = ("postgresql", "mysql")
pair = ("udp", "tcp")
# pair = ("datamapper", "activerecord")
# pair = ("sortedlist", "sorteddictionary")
# pair = ("png", "bmp")

# Prepare POS tagger
pos_tag_set = {"JJR", "JJ", "NN", "NNS", "NNP", "NNPS", "RBR", "RBS"}
keywords_path = os.path.join(os.pardir, "communities", "{}_{}.txt".format("&".join(pair), f))
# stopwords_path = os.path.join(os.pardir, "communities", "stopwords.txt")

# Prepare stop words list
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
download('stopwords')
stop_words = stopwords.words('english')
stop_words.append("much")
stop_words.remove("more")
stop_words.append("reason")
stop_words.append("reasons")
stop_words.append("case")
stop_words.append("cases")
stop_words.append("etc")
stop_words.append("question")
stop_words.append("questions")
# with open(stopwords_path, "a") as stopwords_file:
#     for w in stop_words:
#         stopwords_file.write(w+"\n")
# stop_words.append("more")
# stop_words.append("less")

# Prepare stop phrases
stop_phrases = [["for", "example"], ["in", "terms", "of"], ["keep", "in", "mind"],
                ["in", "this", "case"], ["a", "lot"], ["a", "lot", "of"], ["lots", "of"]]

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
        # print(tagged_words)
        # print(sentence.strip())
        for phrase in stop_phrases:
            n = len(phrase)
            for i in range(len(tagged_words) - n + 1):
                if phrase == words[i:i+n]:
                    for j in range(i, i+n):
                        tagged_words[j] = (None, tagged_words[j][1])
        i = 0
        indices = []
        keywords = []
        for (word, tag) in tagged_words:
            if word in pair:
                indices.append(i)
                keywords.append(word)
                i += 1
            elif word not in stop_words and tag in pos_tag_set and word is not None:
                keywords.append(word)
                i += 1
        if len(keywords) <= 10 and flag:
            ws = [w for w in keywords if w not in pair]
        else:
            ws = []
            # if len(indices) == 2:
            #     for j in range(len(keywords)):
            #
            #         if j > indices[0] and j <= indices[0] + 4 and keywords[j] not in pair and j < indices[1]:
            #             ws.append(keywords[j])
            #         elif j >= indices[1] - 2 and j <= indices[1] + 2 and keywords[j] not in pair:
            #             ws.append(keywords[j])
            # else:
            if True:
                for j in range(len(keywords)):
                    for i in indices:
                        if j >= i - 2 and j <= i + 2 and keywords[j] not in pair:
                            ws.append(keywords[j])
                            break
                print(ws)
                print(sentence+"\n")
        with open(keywords_path, "a") as keywords_file:
            keywords_file.write(",".join(ws)+"\n")
            keywords_file.write(sentence+"\n")
        corpus.append(ws)
    else:
        corpus.append([w for w in sentence.split() if w not in stop_words])

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

out_path = os.path.join(os.pardir, "communities", "{}_{}_{}_{}{}{}.txt".format("&".join(pair), G.number_of_nodes(), l, default_distance, pos, f))
image_path = os.path.join(os.pardir, "communities", "{}_{}_{}_{}{}{}.png".format("&".join(pair), G.number_of_nodes(), l, default_distance, pos, f))
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
graph_indices = set()
with open(out_path, "a") as out_file:
    for com in communities:
        out_file.write("{}---------------------------------------------------\n\n".format(num))
        for i in com:
            out_file.write(",".join(corpus[i])+"\n")
            out_file.write(sentences[i]+"\n")
            graph_indices.add(i)
        num += 1
    out_file.write("other---------------------------------------------------\n\n")
    for i in range(len(sentences)):
        if i not in graph_indices:
            out_file.write(",".join(corpus[i])+"\n")
            out_file.write(sentences[i]+"\n")
