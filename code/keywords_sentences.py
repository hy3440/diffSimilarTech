"""
Extract comparative sentences containing keywords.
"""

from bs4 import BeautifulSoup
import keywords
import nltk
import os
import pymysql.cursors


curr_path = os.path.abspath(__file__)
root_path = os.path.abspath(os.path.join(curr_path, os.pardir))
# sys.path.append(str(root_path))

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='{}'.format(sys.argv[1]),
                             db='stackoverflow')

try:
    with connection.cursor() as cursor:
        data_file = open(os.path.join(os.path.join(os.pardir, "Data"), "keywords_sentences.txt"), "a")
        count = 0
        sent_count = 0
        key_words = keywords.generates_key_words()
        key_phrases = keywords.generates_key_phrases()
        sql = """SELECT Body FROM Posts WHERE Score >= 0 AND Id <= 3000"""
        cursor.execute(sql)
        for i in range(cursor.rowcount):
            raw = cursor.fetchone()
            soup = BeautifulSoup(str(raw), "lxml")
            for code in soup.find_all("code"):
                code.decompose()
            result = soup.get_text()
            sents = nltk.sent_tokenize(result)
            for sent in sents:
                sent_count += 1
                flag = False
                tokens = nltk.word_tokenize(sent)
                tagged_tokens = nltk.pos_tag(tokens)

                for word in key_words:
                    if word in tokens:
                        flag = True
                        break

                if not flag:
                    for phrase in key_phrases:
                        test = True
                        for w in phrase:
                            if w not in tokens:
                                test = False
                                break
                        if test:
                            flag = True
                            break

                if not flag:
                    for (token, tag) in tagged_tokens:
                        flag = (tag == "JJR") or (tag == "RBR") or (tag == "JJS") or (tag == "RBS")

                if flag:
                    data_file.write("{}: {}\n".format(count, sent))
                    # data_file.write(str(tagged_tokens))
                    count += 1
        print "{} comparative sentences in total {} sentences ({} posts)".format(count, sent_count, cursor.rowcount)
        data_file.close()
finally:
    connection.close()
