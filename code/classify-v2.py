import os
from pattern_matcher import PatternMatcher
import time


pattern_matcher = PatternMatcher()
num = 0
try:
    start_time = time.time()
    with open(os.path.join(os.pardir, "Data", "tech", "tech_sentences_2.txt")) as data_file:
        for line in data_file:
            if num % 2 == 0:
                current_id = line
            else:
                words = line.split(" ")

                pattern_matcher.match_pattern(words, current_id, "keytechs")
            num += 1
finally:
    end_time = time.time()
    summary_file = open(os.path.join(os.pardir, "Data", "tech", "classified_by_tech", "classify-v2_summary.txt"), "a")
    summary_file.write("Comparative sentences: {}\n".format(pattern_matcher.compa_sent_count))
    summary_file.write("Sentence number: {}\n".format(num/2))
    # summary_file.write("Post number: {}\n".format(num))
    for key, value in pattern_matcher.count.iteritems():
        summary_file.write("Pattern {}: {} sentences\n".format(key, value))
    summary_file.write("\n")
    summary_file.close()
    pattern_matcher.connection.close()
    data_file.close()
