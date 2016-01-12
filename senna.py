#!/usr/bin/env python3 -*- coding: utf-8 -*-

"""NLTK Command Line Interface - Senna API

Usage:
  senna.py (-h | --help)
  senna.py --version
  senna.py --sennadir PATH --postag  --input FILE [--output NONE]
  senna.py --sennadir PATH --nertag  --input FILE [--output NONE]
  senna.py --sennadir PATH --chunktag  --input FILE [--output NONE]
  senna.py --sennadir PATH --np FILE
  senna.py --sennadir PATH --chunk CHUNKTYPE FILE
  senna.py --np  FILE [--output NONE]
  senna.py --vp  FILE [--output NONE]
  senna.py --chunk CHUNKTYPE FILE [--output NONE]
  senna.py --postag  FILE [--output NONE]
  senna.py --nertag  FILE [--output NONE]
  senna.py --chunktag  FILE [--output NONE]
  senna.py --chunk2 CHUNKTYPES FILE
  
Options:
  -h --help     		Show this screen.
  --sennadir			Path to jar file (Complusory)
  --input				Path to input file.
  --output				Path to output file [default: None].
  --postag      		Option to POS tag a file.
  --nertag      		Option to NER tag a file.
  --chunktag  			Option to chunk (i.e. BIO tag) a file.
  --chunk CHUNKTYPE  	TL;DR, "I just want to extract CHUNKTYPE from this file".
  --np  	    		TL;DR, "I just want to extract NPs from this file".
  --vp  	    		TL;DR, "I just want to extract NPs from this file".
  --chunk2 CHUNKTYPE     TL;DR, "I just want to combine CHUNKTYPES (e.g. VP+ADJP) from this file".
"""

from __future__ import print_function
import io
import os
import re

from nltk import word_tokenize
from nltk.tag.senna import SennaTagger, SennaNERTagger, SennaChunkTagger

from docopt import docopt

senna_tool = {
'--postag': SennaTagger,
'--nertag': SennaNERTagger,
'--chunktag': SennaChunkTagger,
'--chunk': SennaChunkTagger,
'--chunk2': SennaChunkTagger,
}


def initialize_tool(arguments):
	process = next(k for k,v in arguments.items() if k in senna_tool and v)
	tool = senna_tool[process](arguments['--sennadir'])
	return tool, process
	
def augment_arguments(arguments):
	if arguments['--sennadir'] is None:
		homedir = os.path.expanduser("~")
		arguments['--sennadir'] = homedir + '/senna/'
	if '--np' in arguments and arguments['--np']:	
		arguments['--chunk'] = 'NP'
	if '--vp' in arguments and arguments['--vp']:	
		arguments['--chunk'] = 'VP'
		
		
def initialize_iofiles(arugments):
	infile, outfile = "", ""
	if arguments['FILE']:
		infile = arguments['FILE']
	elif arguments['--input']:
		infile = arguments['--input']
	if arugments['--output']:
		outfile = arugments['--output']
	return infile, outfile
	

def senna_tag_sents(sentences, tool, chunk_type=None):
	tagged_sents = tool.tag_sents(sentences)
	for sent in tagged_sents:
		yield " ".join(word + '#' + pos for word, pos in sent)

def senna_extract_chunks(sentences, chunker, chunk_type):
	tagged_sents = chunker.tag_sents(sentences)
	for tagged_sent in tagged_sents:
		chunk_outputs = list(chunker.bio_to_chunks(tagged_sent, chunk_type))
		if chunk_outputs:
			chunks, positions = zip(*chunk_outputs)
			yield "|".join(chunks)
		else:
			yield str("!!! NO CHUNK of " + chunk_type + " in this sentence !!!")

def senna_extract_combined_chunks(sentences, chunker, chunk_types):
	_chunk_types = chunk_types.split('+')
	tagged_sents = chunker.tag_sents(sentences)

	for tagged_sent in tagged_sents:
		chunks1 = list(chunker.bio_to_chunks(tagged_sent, _chunk_types[0]))
		chunks2 = list(chunker.bio_to_chunks(tagged_sent, _chunk_types[1]))

		chunk_combinations = []
		jumper = 0
		for chunk1 in chunks1:
			chunk1_end_position = int(chunk1[1].split('-')[-1])
			for i, chunk2 in enumerate(chunks2[jumper:]):
				chunk2_start_position = int(chunk2[1].split('-')[0])
				if chunk2_start_position == chunk1_end_position+1:
					jumper = i
					chunks, positions = zip(*[chunk1, chunk2])
					chunk_combinations.append("\t".join(chunks))
		if chunk_combinations:
			yield ('|'.join(chunk_combinations))
		else:
			yield str("!!! NO CHUNK of " + chunk_types + " in this sentence !!!")
			


if __name__ == '__main__':
	arguments = docopt(__doc__, version='NLTK CLI (Senna Tools) version 0.0.1')
	# Augment arguments for TL;DR commands.
	augment_arguments(arguments)
	# Initialize tool.
	tool, process = initialize_tool(arguments)
	infile, outfile = initialize_iofiles(arguments)
	# Initialize output file.
	if outfile:
		fout = io.open(outfile, 'w', encoding='utf8')
		
	if arguments['--chunk']:
		process = senna_extract_chunks
	elif arguments['--chunk2']:
		process = senna_extract_combined_chunks
		arguments['--chunk'] = arguments['--chunk2']
	else:
		process = senna_tag_sents
			
	with io.open(infile, 'r', encoding='utf8') as fin:	
		sentences = [word_tokenize(line.strip()) for line in fin]
		for processed_sent in process(sentences, tool, arguments['--chunk']):
			if outfile:
				fout.write(processed_sent + '\n')
			else:
				print(processed_sent)

