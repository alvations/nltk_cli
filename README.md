# nltk_cli

This repo contains the **TL;DR** solutions to using third-party tools 
(e.g. Stanford NLP, SENNA NLP, etc.) with NLTK.

**Disclaimers**: It comes with unexpected caveats that are idiosyncratic to (i) the data you are processing and (ii) how NLTK API and Stanford NLP tools work. 

Installation
====

```bash
cd $HOME

# Download the Stanford NLP tools
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

# Download the Stanford Spanish models.
wget http://nlp.stanford.edu/software/stanford-spanish-corenlp-2015-01-08-models.jar
unzip stanford-spanish-corenlp-2015-01-08-models.jar -d stanford-spanish
cp stanford-spanish/edu/stanford/nlp/models/ner/* stanford-ner/classifiers/

# Download the Stanford German models.
wget http://nlp.stanford.edu/software/stanford-german-2015-01-30-models.jar
unzip stanford-german-2015-01-30-models.jar -d stanford-german
cp stanford-german/edu/stanford/nlp/models/ner/* stanford-ner/classifiers/

# Download the Stanford Chinese models.
wget http://nlp.stanford.edu/software/stanford-chinese-corenlp-2015-04-20-models.jar
unzip stanford-chinese-corenlp-2015-04-20-models.jar -d stanford-chinese-ner
cp stanford-chinese-ner/edu/stanford/nlp/models/ner/* stanford-ner/classifiers/

# Download the SENNA tools.
wget http://ronan.collobert.com/senna/senna-v3.0.tgz
tar zxvf senna-v3.0.tgz
mv senna-v3.0 senna

# Install NLTK
pip install -U nltk
# Git clone this repository.
git clone https://github.com/alvations/nltk_cli.git
```

Usage
====

```bash
cd nltk_cli

###############################################################################
# Stanford NLP Tools
###############################################################################

# Using Stanford LexParser
python3 stanford.py --tool=lexparser \
--jar=$HOME/stanford-parser/stanford-parser.jar \
--modeljar=$HOME/stanford-parser/stanford-parser-3.5.2-models.jar \
--model=edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz \
--input=test.txt

# Using Stanford POSTagger
python3 stanford.py --tool=postagger \
--jar=$HOME/stanford-postagger/stanford-postagger.jar \
--model=$HOME/stanford-postagger/models/english-bidirectional-distsim.tagger \
--input=test.txt

# Using Stanford NERTagger
python3 stanford.py --tool=nertagger \
--jar=$HOME/stanford-ner/stanford-ner.jar \
--model=$HOME/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz \
--input=test.txt

# TL;DR way to use Stanford LexParser, make sure your `stanford-parser` directory
# is in your $HOME directory and you have installed as per the installation
# instruction above, otherwise these TL;DR commands won't work.
python3 stanford.py --postag test.txt
python3 stanford.py --nertag test.txt
python3 stanford.py --lexparser test.txt

# TL;DR with model option.
python3 stanford.py --lexparse test.txt \
--model=edu/stanford/nlp/models/lexparser/wsjPCFG.ser.gz 
python3 stanford.py --postag test.txt \
--model=$HOME/stanford-postagger/models/english-bidirectional-distsim.tagger 
python3 stanford.py --nertag test.txt \
--model=$HOME/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz

###############################################################################
# SENNA NLP Tools
###############################################################################

# Using SENNA POSTagger.
python senna.py --sennadir $HOME/senna --postag --input test.txt

# Using SENNA NERTagger.
python senna.py --sennadir $HOME/senna --nertag --input test.txt

# Using SENNA ChunkTagger.
python senna.py --sennadir $HOME/senna --chunktag --input test.txt

# TL;DR NP Chunk Extractor using SENNA ChunkTagger.
python senna.py --sennadir $HOME/senna --chunk NP test.txt
python senna.py --sennadir $HOME/senna --np test.txt

# Tl;DR way to use SENNA Taggers, make sure your `senna` directory is in your
# $HOME directory and you have installed as per the installation instruction 
# above, otherwise, these Tl;DR might not work.
python senna.py --postag --input test.txt
python senna.py --nertag --input test.txt
python senna.py --chunktag --input test.txt

# Tl;DR way to use SENNA ChunkTagger to extract NPs, make sure your `senna` 
# directory is in your $HOME directory and you have installed as per the 
# installation instruction above, otherwise, these Tl;DR might not work.
python senna.py --np test.txt
python senna.py --vp test.txt
python senna.py --chunk NP test.txt
python senna.py --chunk VP test.txt

##############################################################################
# Terminator Term Extract filters.
##############################################################################

# Extracts NPs using SENNA ChunkTagger.
python3 senna.py --np test.txt --output test.np
# Filter NPs using Terminator semi-rule based cleaner. Input can be either 
# one NP per line or multiple NPs per line separated by pipe, i.e. "|"
python3 clean_np.py test.np
# If you would like to output the filtered NPs:
python3 clean_np.py test.np --output test.filtered.np
# To remove empty lines from the filtered NPs list:
python3 clean_np.py test.np | sed '/^$/d'
# To get unique list of NPs
python3 clean_np.py test.np | sed '/^$/d' | sort | uniq
```

Note: The `test.txt` file is the `fish-head-curry` file from the [NTU-Multilingual Corpus](http://compling.hss.ntu.edu.sg/ntumc/)

FAQ
====

If any of your output from the commands above cannot be output using `>`, e.g.

```bash
$ python senna.py --np test.txt > test.np
Traceback (most recent call last):
  File "senna.py", line 114, in <module>
    print(processed_sent)
UnicodeEncodeError: 'ascii' codec can't encode character u'\u2019' in position 9: ordinal not in range(128)
```

Then try the `--output` parameter, e.g.:

```bash
$ python senna.py --np test.txt --output test.np
```

Alternatively, you can set your STDOUT encoding, e.g.:

```bash
$ export PYTHONIOENCODING=utf-8
$ python senna.py --np test.txt > test.np
```
