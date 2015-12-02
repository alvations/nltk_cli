#!/usr/bin/env python3 -*- coding: utf-8 -*-

"""NLTK Command Line Interface - Stanford API

Usage:
  stanford.py --tool=postagger --jar FILE --model PATH --input FILE [--output NONE]
  stanford.py --tool=neragger --jar FILE --model PATH --input FILE  [--output NONE]
  stanford.py --tool=lexparser --jar FILE --modeljar FILE --model PATH --input FILE [--output NONE]
  stanford.py (-h | --help)
  stanford.py --version
  
  stanford.py --postag FILE [--lang LANG] [--output NONE]
  stanford.py --lexparse FILE [--lang LANG] [--output NONE]
  stanford.py --postag FILE [--model PATH] [--output NONE]
  stanford.py --lexparse FILE [--model PATH] [--output NONE]
  stanford.py --nertag FILE [--output NONE]
  
Options:
  -h --help     Show this screen.
  --tool		Tagger/Parser option (i.e. 'lexparser', 'postagger', etc.)
  --jar			Path to jar file (Complusory)
  --model		Path to model name (Complusory).
  --modeljar	Path to model jar file (Only use with Stanford parsers).
  --input		Path to input file.
  --output		Path to output file [default: None].
  --postag      TL;DR, "I just want to POS tag this file" [default: eng].
  --nertag      TL;DR, "I just want to NER tag this file" (only English).
  --lexparse    TL;DR, "I just want to parse this file" [default: eng].
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


lexparser_languages = {
# Arabic
'ara': ['arabicFactored.ser.gz'],
# Chinese
'cmn': ['chinesePCFG.ser.gz', 'chineseFactored.ser.gz',
'xinhuaPCFG.ser.gz', 'xinhuaFactored.ser.gz', 'xinhuaFactoredSegmenting.ser.gz'],
# German
'deu':['germanPCFG.ser.gz', 'germanFactored.ser.gz'],
# English
'eng': ['englishRNN.ser.gz', 'englishPCFG.ser.gz', 
'englishFactored.ser.gz', 'englishPCFG.caseless.ser.gz', 'wsjPCFG.ser.gz',
'wsjRNN.ser.gz', 'wsjFactored.ser.gz'],
# French
'fre': ['frenchFactored.ser.gz'],
# Spanish
'spa': ['spanishPCFG.ser.gz']}

postagger_languages = {
# Arabic
'ara': ['arabic.tagger'], 
# Chinese
'cmn': ['chinese-distsim.tagger', 'chinese-nodistsim.tagger'],
# English
'eng': ['english-bidirectional-distsim.tagger', 
'english-caseless-left3words-distsim.tagger', 
'english-left3words-distsim.tagger', 'wsj-0-18-bidirectional-distsim.tagger', 
'wsj-0-18-bidirectional-nodistsim.tagger', 
'wsj-0-18-caseless-left3words-distsim.tagger', 
'wsj-0-18-left3words-distsim.tagger', 'wsj-0-18-left3words-nodistsim.tagger'],
# French
'fre': ['french.tagger'],
# German
'deu': ['german-dewac.tagger', 'german-fast-caseless.tagger', 
'german-fast.tagger', 'german-hgc.tagger'],
# Spanish
'spa': ['spanish-distsim.tagger', 'spanish.tagger']
}

nertagger_languages = {
# Chinese
'cmn': ['chinese.misc.distsim.crf.ser.gz'],
# German
'deu': ['german.dewac_175m_600.crf.ser.gz', 'german.hgc_175m_600.crf.ser.gz'],
# English
'eng': ['english.all.3class.distsim.crf.ser.gz', 'english.conll.4class.distsim.crf.ser.gz', 
'english.muc.7class.distsim.crf.ser.gz', 'example.serialized.ncc.ncc.ser.gz'],
# Spansih
'spa': ['spanish.ancora.distsim.s512.crf.ser.gz']
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
	# Augment arugments for LexParser.
	if '--lexparse' in arguments.keys() and arguments['--lexparse']:
		arguments['--tool']	= 'lexparser'
		arguments['--jar']	= homedir +'/stanford-parser/stanford-parser.jar'
		arguments['--modeljar']	= homedir +'/stanford-parser/stanford-parser-3.5.2-models.jar'
		if arguments['--model'] is None:		
			if arguments['--lang'] == None:
				arguments['--model'] = 'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
			else:
				arguments['--model'] = 'edu/stanford/nlp/models/lexparser/' 
				arguments['--model']+= lexparser_languages[arguments['--lang']][0]
	# Augment arugments for POSTagger.
	elif '--postag' in arguments.keys() and arguments['--postag']:
		arguments['--tool']	= 'postagger'
		arguments['--jar']	= homedir +'/stanford-postagger/stanford-postagger.jar'
		if arguments['--model'] is None:	
			if arguments['--lang'] == None:
				arguments['--model'] = homedir + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
			else:
				arguments['--model'] =  homedir + '/stanford-postagger/models/'
				arguments['--model']+= postagger_languages[arguments['--lang']][0]
	# Augment arugments for NERTagger.
	elif '--nertag' in arguments.keys() and arguments['--nertag']:
		arguments['--tool']	= 'nertagger'
		arguments['--jar']	= homedir +'/stanford-ner/stanford-ner.jar'
		if arguments['--model'] is None:
			if arguments['--lang'] == None:
				arguments['--model'] = homedir + '/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'
			else:
				arguments['--model'] =  homedir + '/stanford-postagger/models/'
				arguments['--model']+= nertagger_languages[arguments['--lang']][0]
		

if __name__ == '__main__':
	arguments = docopt(__doc__, version='NLTK CLI (Stanford Tools) version 0.0.1')
	# Augment arguments for TL;DR commands.
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


