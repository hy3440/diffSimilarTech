from nltk.tag.stanford import CoreNLPPOSTagger
from nltk.parse.corenlp import CoreNLPDependencyParser
import spacy
from spacy.matcher import Matcher


# dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
#
# while True:
#     parse, = dep_parser.raw_parse(input(">>>"))
#
#     for governor, dep, dependent in parse.triples():
#         print(governor, dep, dependent)

line = input(">>>")
print(line.split(" "))
for (word, tag) in CoreNLPPOSTagger(url='http://localhost:9000').tag(line.split(" ")):
    print(word)
    print(tag)
print(tag)
