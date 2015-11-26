#!/usr/bin/env python3 -*- coding: utf-8 -*-

"""NLTK Command Line Interface - Stanford API

Usage:
  stanford.py --tool=postagger --jar FILE --model PATH --input FILE [--output NONE]
  stanford.py --tool=neragger --jar FILE --model PATH --input FILE  [--output NONE]
  stanford.py --tool=lexparser --jar FILE --modeljar FILE --model PATH --input FILE [--output NONE]
  stanford.py (-h | --help)
  stanford.py --version
  
  stanford.py --nertag FILE [--lang LANG]
  stanford.py --postag FILE [--lang LANG]
  stanford.py --lexparse FILE [--lang LANG]
  
Options:
  -h --help     Show this screen.
  --tool		Tagger/Parser option (i.e. 'lexparser', 'postagger', etc.)
  --jar			Path to jar file (Complusory)
  --model		Path to model name (Complusory).
  --modeljar	Path to model jar file (Only use with Stanford parsers).
  --input		Path to input file.
  --output		Path to output file [default: None].
  --postag      TL;DR, "I just want to POS tag this file".
  --nertag      TL;DR, "I just want to NER tag this file".
  --lexparse    TL;DR, "I just want to parse this file".
  --lang		The language option for TL;DR options [default: eng].
"""

from __future__ import print_function
import io
import os
import re


from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.parse.stanford import StanfordParser
#from nltk.parse.stanford import StanfordDependencyParser
#from nltk.parse.stanford import StanfordNeuralDependencyParser

from docopt import docopt


taggers = {
'postagger': StanfordPOSTagger, 
'nertagger':StanfordNERTagger
}


parsers = {
'lexparser':StanfordParser, 
#'depparser':StanfordDependencyParser, # Not coded yet.
#'neuralparser':StanfordNeuralDependencyParser # Not coded yet.
}


def stanford_tag_sents(sentences, tagger):
	tagged_sents = tagger.tag_sents(sentences)
	for sent in tagged_sents:
		yield " ".join(word + '#' + pos for word, pos in sent)


def stanford_parse_sents(sentences, parser):
	parsed_sents = sum([list(i) for i in parser.parse_sents(sentences)], [])
	return [re.sub(' +',' ', str(sent).replace('\n', '')) for sent in parsed_sents]

def initialize_tool(arguments):
	"""
	To initalize the Stanford tools given the users arguments from command line.
	"""
	tool_name = arguments['--tool']
	if tool_name in taggers:
		tagger = taggers[tool_name](model_filename=arguments['--model'], path_to_jar=arguments['--jar'])
		return tagger, stanford_tag_sents
	elif tool_name in parsers:
		parser = parsers[tool_name](model_path=arguments['--model'], path_to_models_jar=arguments['--modeljar'], path_to_jar=arguments['--jar'])
		return parser, stanford_parse_sents
								

def initialize_iofiles(arugments):
	infile, outfile = "", ""
	if arguments['FILE']:
		infile = arguments['FILE']
	elif arguments['--input']:
		infile = arguments['--input']
	if arugments['--output']:
		outfile = arugments['--output']
	return infile, outfile
	
def augment_arugments(arguments):
	homedir = os.path.expanduser("~")
	if '--lexparse' in arguments.keys() and arguments['--lexparse']:
		arguments['--tool']	= 'lexparser'
		arguments['--jar']	= homedir +'/stanford-parser/stanford-parser.jar'
		arguments['--modeljar']	= homedir +'/stanford-parser/stanford-parser-3.5.2-models.jar'
		arguments['--model'] = 'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
	elif '--postag' in arguments.keys() and arguments['--postag']:
		arguments['--tool']	= 'postagger'
		arguments['--jar']	= homedir +'/stanford-postagger/stanford-postagger.jar'
		arguments['--model'] = homedir + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
	elif '--nertag' in arguments.keys() and arguments['--nertag']:
		arguments['--tool']	= 'nertagger'
		arguments['--jar']	= homedir +'/stanford-ner/stanford-ner.jar'
		arguments['--model'] = homedir + '/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'

if __name__ == '__main__':
	arguments = docopt(__doc__, version='NLTK CLI (Stanford Tools) version 0.0.1')
	if arguments['--tool'] is None:
		augment_arugments(arguments)
	tool, process = initialize_tool(arguments)
	infile, outfile = initialize_iofiles(arguments)
	if outfile:
		fout = io.open(outfile, 'w', encoding='utf8')
	with io.open(infile, 'r', encoding='utf8') as fin:
		sentences = [line.strip().split() for line in fin]
		for processed_sent in process(sentences, tool):
			if outfile:
				fout.write(processed_sent + '\n')
			else:
				print(processed_sent)


