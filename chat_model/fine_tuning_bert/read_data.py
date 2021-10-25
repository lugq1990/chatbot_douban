# coding:utf-8

import re
import os
import unicodedata
from pathlib import Path


def read_samples(root_path=None):
	processed_corpus = "sample_data_models\cornell movie-dialogs corpus\processed_movie_diaglog.txt"
	
	if not root_path:
		root_path = Path(os.path.dirname(os.path.abspath(__file__))).parent

	with open(os.path.join(root_path, processed_corpus), 'r', encoding='utf-8') as f:
		data = [x.replace('\n', '') for x in f.readlines()]
	
	return data


# Turn a Unicode string to plain ASCII
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s

def addSep(s):
	return "[CLS] " + s + " [SEP] "

def get_length(line):
	return len(line.split(" "))

def trimm(pairs):
	print("Trim Pairs...")
	count = 0
	new_pairs = []
	for pair in pairs:
		ques_len, answ_len = get_length(pair[0]), get_length(pair[1])
		if ques_len + answ_len > 100:
			continue
		else:
			new_pairs.append(pair)
			count += 1
	print("Trimmed {} Sentence Pair...".format(count))
	return new_pairs

def readPairs():
	print("Reading lines...")
	# combine every two lines into pairs and normalize
	content = read_samples()
	lines = [x.lower().strip() for x in content]
	print("Length:", len(lines))
	pairs = []
	for i in range(len(lines) - 1):
		pairs.append([lines[i], lines[i+1]])

	pairs = trimm(pairs)
	return pairs

	

if __name__ == "__main__":
	pairs = readPairs()
	#print(pairs)
