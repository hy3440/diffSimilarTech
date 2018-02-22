from nltk.parse.corenlp import CoreNLPDependencyParser


dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')

while True:
    parse, = dep_parser.raw_parse(input(">>>"))

    for governor, dep, dependent in parse.triples():
        print(governor, dep, dependent)
