import os
from pattern_matcher import PatternMatcher
import time


pattern_matcher = PatternMatcher()
num = 0
try:
    start_time = time.time()
    with open(os.path.join(os.pardir, "out", "tech_v2", "tech_sentences.txt")) as data_file:
        for line in data_file:
            if num % 3 == 0:
                current_id = line
            elif num % 3 == 1:
                tech_pair = line
            else:
                words = line.split(" ")
                pattern_matcher.match_pattern(words, current_id, tech_pair, "keytechs")
            num += 1
finally:
    end_time = time.time()
    summary_file = open(os.path.join(os.pardir, "out", "tech_v2", "classify-v2_summary.txt"), "a")
    summary_file.write("Comparative sentences: {}\n".format(pattern_matcher.compa_sent_count))
    summary_file.write("Sentence number: {}\n".format(num/3))
    # summary_file.write("Post number: {}\n".format(num))
    for key, value in pattern_matcher.count.iteritems():
        summary_file.write("Pattern {}: {} sentences\n".format(key, value))
    summary_file.write("\n")
    summary_file.close()
    pattern_matcher.connection.close()
    data_file.close()
