#!/usr/bin/env python3 -*- coding: utf-8 -*-

"""
This script takes an output from:

	python3 nltk_cli/senna.py --np test.txt > test.np

And process the noun phrases to filter out phrases 

(i)   that don't have the last word tagged as NN
(ii)  has any token that is a stopword
(iii) the first and last word in phrase is not a punctuation

This is part of the Terminator software from 
https://github.com/alvations/Terminator (Tan, 2015)

Usage:

	python3 nltk_cli/clean_np.py test.np test.filtered.np

Reference:

Liling Tan. 2015. EXPERT Innovations in Terminology Extraction and 
Ontology Induction. In Proceedings of Proceedings of the EXPERT Scientific 
and Technological Workshop. Malaga, Spain.
"""

import io, sys
from os.path import expanduser
from string import punctuation

from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tag import PerceptronTagger

tagger = PerceptronTagger()
pos_tag = tagger.tag
STOPWORDS = stopwords.words('english')

def simple_filter(list_of_ngrams):
    return [ng for ng in list_of_ngrams if
            ng.lower() not in STOPWORDS and
            ng[0] not in punctuation and ng[-1] not in punctuation and
            ng.split()[-1].lower() not in STOPWORDS and
            ng.split()[0].lower() not in STOPWORDS and
            not any(i for i in ng.split() if i.lower() in STOPWORDS) and
            any(pos for word,pos in pos_tag(ng.lower().split())
                if pos.startswith('NN')) and
            ')' not in ng and '(' not in ng and ',' not in ng and
            'pinyin' not in ng and
            ng.split()[0] not in ['more', 'less']]

outfile = ""

try:
	if sys.argv[2] == '--output':
		outfile = sys.argv[3]
		fout = io.open(outfile, 'w', encoding='utf8')
except IndexError:
	pass

with io.open(sys.argv[1], 'r', encoding='utf8') as fin:
    for line in fin:
        list_of_ngrams = line.split('\t')[0].split('|')
        for ng in simple_filter(list_of_ngrams):
        	if outfile:
        		fout.write(ng + '\n')
        	else:
        		print(ng)


