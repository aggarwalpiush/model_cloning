#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs
import xml.etree.ElementTree as ET
import json
import os
import subprocess
import shlex
import glob
import pathlib
import re
from time import sleep
from conllu import parse_tree_incr, parse
from nltk.corpus import brown, nps_chat
from nltk.corpus.reader.bnc import BNCCorpusReader
from nltk.corpus.reader import mte

HOME = '/Users/paggarwal'
LANGUAGE = 'english'
TYPE = 'spoken'
PREFIX = 'gum-interview'

INPUT_PATH = os.path.join(HOME, 'corpora')
OUTPUT_PATH_DELTA = os.path.join(HOME, 'github_repos/model_cloning/data/posTaggerEval/delta')
OUTPUT_PATH = os.path.join(HOME, 'github_repos/model_cloning/data/posTaggerEval/')
# english/formal/gum-howto/GUM_whow_quidditch.conll10'

def gum_parser(input_ptb_file_path, output_path):
	for ptbfile in glob.glob(input_ptb_file_path+'/*.ptb'):
		print(ptbfile)
		if PREFIX.replace('-','_').replace('howto', 'whow') in ptbfile.lower():
			if not os.path.exists(os.path.join(output_path, LANGUAGE, TYPE, PREFIX)):
				pathlib.Path(os.path.join(output_path, LANGUAGE, TYPE, PREFIX)).mkdir(parents=True, exist_ok=True)
			with codecs.open(os.path.join(output_path, LANGUAGE, TYPE, PREFIX, os.path.basename(ptbfile).replace('.ptb','.txt')), 'w', 'utf-8' ) as text_write:
				command = './ptb_parser.sh ' +  str(ptbfile)
				text_format = subprocess.run(shlex.split(command), stdout=subprocess.PIPE)
				for line in text_format.stdout.decode('utf-8'):
					text_write.write(line)

def get_bnc_parser_domain(input_bnc_path):
	news = []
	converstations = []
	for fileid in glob.glob(os.path.join(input_bnc_path,'*/*/*.xml')):
		with codecs.open(fileid, 'r', 'utf-8') as in_obj:
			for line in in_obj:
				if 'stext type=' in line:
					if line.split('\"')[1].strip().upper() == 'CONVRSN':
						converstations.append(fileid)
						break
				if 'wtext type=' in line:
					if line.split('\"')[1].strip().upper() == 'NEWS':
						news.append(fileid)
						break
	with codecs.open(os.path.join(os.path.dirname(input_bnc_path),'news_files.txt'), 'w', 'utf-8') as news_obj:
		for fil in news:
			news_obj.write(fil+'\n')
	with codecs.open(os.path.join(os.path.dirname(input_bnc_path),'cvsn_files.txt'), 'w', 'utf-8') as cvsn_obj:
		for fil in converstations:
			cvsn_obj.write(fil+'\n')
	return set(converstations), set(news)



def bnc_parser(input_bnc_path, output_path):
	# Instantiate the reader like this

	# fileids=r'[A-K]/\w*/\w*\.xml'
	bnc_reader = BNCCorpusReader(root=input_bnc_path, fileids=r'[A-K]/\w*/\w*\.xml')

	#And say you wanted to extract all bigram collocations and 
	#then later wanted to sort them just by their frequency, this is what you would do.
	#Again, take a look at the link to the nltk guide on collocations for more examples.

	#list_of_fileids = ['A/A0/A00.xml', 'A/A0/A01.xml']
	conversation, news = get_bnc_parser_domain(input_bnc_path)
	for fileid in glob.glob(os.path.join(input_bnc_path,'*/*/AL*.xml')):
		print('/'.join(fileid.split('/')[-3:]))
		if fileid in news:
			if not os.path.exists(os.path.join(output_path, LANGUAGE, TYPE, 'bnc-written-news')):
					pathlib.Path(os.path.join(output_path, LANGUAGE, TYPE, 'bnc-written-news')).mkdir(parents=True, exist_ok=True)
			with codecs.open(os.path.join(output_path, LANGUAGE, TYPE, 'bnc-written-news', os.path.basename(fileid).replace('.xml', '.txt')), 'w', 'utf-8' ) as text_write:
				for line in bnc_reader.tagged_words(fileids=['/'.join(fileid.split('/')[-3:])], c5=True):
					#print(line[0]+' '+line[1]+'\n')
					text_write.write(line[0]+' '+line[1]+'\n')

def bnc_parser_delta(input_bnc_path, output_path):
	# Instantiate the reader like this

	# fileids=r'[A-K]/\w*/\w*\.xml'
	bnc_reader = BNCCorpusReader(root=input_bnc_path, fileids=r'[A-K]/\w*/\w*\.xml')

	#And say you wanted to extract all bigram collocations and
	#then later wanted to sort them just by their frequency, this is what you would do.
	#Again, take a look at the link to the nltk guide on collocations for more examples.

	#list_of_fileids = ['A/A0/A00.xml', 'A/A0/A01.xml']
	conversation, news = get_bnc_parser_domain(input_bnc_path)
	for fileid in glob.glob(os.path.join(input_bnc_path,'*/*/KS*.xml')):

		print('/'.join(fileid.split('/')[-3:]))
		if fileid in conversation:
			if not os.path.exists(os.path.join(output_path, LANGUAGE, TYPE, 'bnc-written-news')):
					pathlib.Path(os.path.join(output_path, LANGUAGE, TYPE, 'bnc-written-news')).mkdir(parents=True, exist_ok=True)
			with codecs.open(os.path.join(output_path, LANGUAGE, TYPE, 'bnc-written-news', os.path.basename(fileid).replace('.xml', '.txt')), 'w', 'utf-8' ) as text_write:
				for sent in bnc_reader.tagged_sents(fileids=['/'.join(fileid.split('/')[-3:])], c5=True):
					#print(line[0]+' '+line[1]+'\n')
					word = []
					tags = []
					for word_tag_pair in sent:
						word.append(word_tag_pair[0])
						tags.append(word_tag_pair[1])
					try:
						text_write.write(' '.join(tags) + '\t' + ' '.join(word) + '\n')
					except TypeError:
						print(word)
						print(tags)


def brown_corpus(output_path):
	for cat in brown.categories():
		for docfile in brown.fileids(cat):
			if not os.path.exists(os.path.join(output_path, LANGUAGE, TYPE, 'brown')):
				pathlib.Path(os.path.join(output_path, LANGUAGE, TYPE, 'brown')).mkdir(parents=True, exist_ok=True)
			with codecs.open(os.path.join(output_path, LANGUAGE, TYPE, 'brown', docfile+'.txt'), 'w', 'utf-8' ) as text_write:
				for sentence in brown.tagged_sents(fileids=docfile):
					for tagset in sentence:
						text_write.write(' '.join(list(tagset)) + '\n')


def brown_xml_parser(input_path, output_path):
	with codecs.open(output_path, 'w', 'utf-8') as output_obj:
		with codecs.open(input_path, 'r', 'utf-8') as input_obj:
			for line in input_obj:
				if '<s n=' in line:
					line_tokens = line.split('<')
					for tok in line_tokens:
						if 's n=' in tok:
							word_pair = tok.replace('s n=','').replace('"','').replace('>','')
							print(word_pair.split(' ')[0])
						if 'w type=' in tok:
							word_pair = tok.replace('w type=', '').replace('"', '').replace('>', ' ')
							output_obj.write('%s %s\n'%(word_pair.split(' ')[-1],word_pair.split(' ')[0]))
						if 'c type=' in tok:
							word_pair = tok.replace('c type=', '').replace('"', '').replace('>', ' ')
							output_obj.write('%s %s\n'%(word_pair.split(' ')[-1],word_pair.split(' ')[0]))



def nps_chat_corpus(output_path):

	for fid in nps_chat.fileids():
		if not os.path.exists(os.path.join(output_path, LANGUAGE, TYPE, 'nps-irc')):
				pathlib.Path(os.path.join(output_path, LANGUAGE, TYPE, 'nps-irc')).mkdir(parents=True, exist_ok=True)
		with codecs.open(os.path.join(output_path, LANGUAGE, TYPE, 'nps-irc', fid+'.txt'), 'w', 'utf-8' ) as text_write:
			for tagset in  nps_chat.tagged_words(fileids=fid):
				text_write.write(' '.join(list(tagset)) + '\n')


def nps_chat_corpus_kotoba(input_path, output_path):
	words = []
	pos_tags = []
	for fileid in glob.glob(os.path.join(input_path, '*.xml')):
		with codecs.open(fileid, 'r', 'utf-8') as nps_file_obj:
			for line in nps_file_obj:
				tokens = line.strip().split(' ')
				if len(tokens) == 3:
					if tokens[0] == '<t':
						if not 'apos' in tokens[1].split('=')[1].replace('"', ''):
							if not 'apos' in tokens[2].split('=')[1].replace('"', ''):
								if not '^' in tokens[1].split('=')[1].replace('"', ''):
									if not 'X' == tokens[1].split('=')[1].replace('"', ''):
										if not tokens[2].split('=')[1].replace('"', '').replace('/>', '').rstrip('\r\n').replace('\n', '') == '':
											if not tokens[1].split('=')[1].replace('"', '').rstrip('\r\n').replace('\n', '') == '':
												words.append(tokens[2].split('=')[1].replace('"', '').replace('/>', '').rstrip('\r\n').replace('\n', ''))
												pos_tags.append(tokens[1].split('=')[1].replace('"', '').rstrip('\r\n').replace('\n', ''))
	if not os.path.exists(os.path.join(output_path, LANGUAGE, 'social', 'nps-irc')):
		pathlib.Path(os.path.join(output_path, LANGUAGE, 'social', 'nps-irc')).mkdir(parents=True, exist_ok=True)
	print(os.path.join(output_path, LANGUAGE, 'social', 'nps-irc', 'nps-irc.txt'))
	with codecs.open(os.path.join(output_path, LANGUAGE, 'social', 'nps-irc', 'nps-irc.txt'), 'w', 'utf-8' ) as text_write:
		for i, word in enumerate(words):
			text_write.write('%s %s\n' %(word, pos_tags[i]))



def switchboard_corpus(input_path, output_path):
	for posfile in glob.glob(input_path+'/*/*.pos'):
		print(posfile)
		if not os.path.exists(os.path.join(output_path, LANGUAGE, TYPE, 'switchboard')):
			pathlib.Path(os.path.join(output_path, LANGUAGE, TYPE, 'switchboard')).mkdir(parents=True, exist_ok=True)
		with codecs.open(os.path.join(output_path, LANGUAGE, TYPE,'switchboard',  os.path.basename(posfile).replace('.pos','.txt')), 'w', 'utf-8' ) as text_write:
			with codecs.open(posfile, 'r', 'utf-8') as input_obj:
				for line in input_obj:
					if not '*x*' in line or '==' in line or re.match(r'^\s*$', line):
						tagged_pairs = line.split()
						for tagged_pair in tagged_pairs:
							if '/' in tagged_pair:
								text_write.write('%s %s\n' %(tagged_pair.split('/')[0], tagged_pair.split('/')[1]))


def bnc_parser_token_count(input_bnc_path):
	bnc_reader = BNCCorpusReader(root=input_bnc_path, fileids=r'[A-K]/\w*/\w*\.xml')
	with codecs.open(os.path.join(HOME, 'github_repos/model_cloning/data/posTaggerEval/english/formal/bnc-written-news','new_data.txt')
					 , 'w', 'utf-8') as text_write:
		with codecs.open('/Users/paggarwal/corpora/english/britishNationalCorpus/news_files.txt') as news_obj:
			tokens = []
			for line in news_obj:
				print(line)
				for i, tagged_word in enumerate(bnc_reader.tagged_words(fileids=['/'.join(line.strip().replace('\n','').split('/')[-3:])], c5=True)):
					if i < 100000:
						text_write.write(tagged_word[0]+' '+tagged_word[1]+'\n')



def main():

	#gum_parser(os.path.join(INPUT_PATH,LANGUAGE,'gum'), OUTPUT_PATH)
	#bnc_parser(os.path.join(INPUT_PATH,LANGUAGE,'britishNationalCorpus', 'Texts'), OUTPUT_PATH)
	#bnc_parser_delta(os.path.join(INPUT_PATH, LANGUAGE, 'britishNationalCorpus', 'Texts'), OUTPUT_PATH)
	#brown_corpus(OUTPUT_PATH)
	#nps_chat_corpus(OUTPUT_PATH)
	#switchboard_corpus(os.path.join(INPUT_PATH,LANGUAGE,'switchboard', 'swbd'), OUTPUT_PATH)
	#get_bnc_parser_domain(os.path.join(INPUT_PATH,LANGUAGE,'britishNationalCorpus', 'Texts'))
	#bnc_parser_token_count(os.path.join(INPUT_PATH, LANGUAGE, 'britishNationalCorpus', 'Texts'))
	#brown_xml_parser(os.path.join(INPUT_PATH,LANGUAGE,'brown_tei/corpus/Corpus.xml'), os.path.join
	#(HOME, 'github_repos/model_cloning/data/posTaggerEval/english/formal/brown/new_corpus.txt'))
	nps_chat_corpus_kotoba('/Users/paggarwal/corpora/english/nps_chat', OUTPUT_PATH)

if __name__ == '__main__':
	main()






