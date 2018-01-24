import nltk

def generates_key_words():
    return nltk.word_tokenize("""more most less least better best worse worst further
     farther furthest farthest beat defeat destroy decimate equal equally kill
     lead obliterate outclass out-class outdo outperform outplay overtake over-take
     smack subdue subpar surpass top trump unmated win equivalent similar dissimilar
     match unequal unlike choose pick favor select like identical as""")

def generates_key_phrases():
    phrases = ["ahead of", "blow away", "blow out of water",  "race against",
               "compete with", "compare with", "compare to", "compare and", "compare over",
               "in comparison", "no comparison", "cannot compare", "edge out", "gain from",
               "inferior to", "superior to", "lag behind", "lead against", "lead by",
               "lose to", "lose against", "number one", "on par", "prefer to", "prefer over",
               "steal from", "suck against", "take over", "take out", "up against",
               "vulnerable to", "weapon against", "win against", "equal to", "the same"]
    return [nltk.word_tokenize(phrase) for phrase in phrases]
