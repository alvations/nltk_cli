# nltk_cli

This repo contains the **TL;DR** solutions to using Stanford tools with NLTK.

**Disclaimers**: It comes with unexpected caveats that are idiosyncratic to (i) the data you are processing and (ii) how NLTK API and Stanford NLP tools work. 

Installation
====

```
# Downloads the Stanford NLP tools
wget http://nlp.stanford.edu/software/stanford-ner-2015-04-20.zip
wget http://nlp.stanford.edu/software/stanford-postagger-full-2015-04-20.zip
wget http://nlp.stanford.edu/software/stanford-parser-full-2015-04-20.zip
# Extract the zip file.
unzip stanford-ner-2015-04-20.zip 
unzip stanford-parser-full-2015-04-20.zip 
unzip stanford-postagger-full-2015-04-20.zip
# Change to a shorter path.
mv stanford-postagger-full-2015-04-20 stanford-postagger
mv stanford-parser-full-2015-04-20 stanford-parser
mv stanford-ner-2015-04-20 stanford-ner
# Git clone this repository.
git clone https://github.com/alvations/nltk_cli.git
```
