#!usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
import sys
import os
import glob
import pathlib
import subprocess
import shlex
from nltk.corpus.reader.bnc import BNCCorpusReader

HOME = '/Users/paggarwal'
LANGUAGE = 'english'
TYPE = 'spoken'
PREFIX = 'gum-interview'

INPUT_PATH = os.path.join(HOME, 'corpora')
OUTPUT_PATH_DELTA = os.path.join(HOME, 'github_repos/model_cloning/data/posTaggerEval/delta')
OUTPUT_PATH = os.path.join(HOME, 'github_repos/model_cloning/data/posTaggerEval/')

def gum_parser(input_ptb_file_path, output_path):
	for ptbfile in glob.glob(input_ptb_file_path+'/*.ptb'):
		print(ptbfile)
		if PREFIX.replace('-','_').replace('howto', 'whow') in ptbfile.lower():
			if not os.path.exists(os.path.join(output_path, LANGUAGE, TYPE, PREFIX)):
				pathlib.Path(os.path.join(output_path, LANGUAGE, TYPE, PREFIX)).mkdir(parents=True, exist_ok=True)
			with codecs.open(os.path.join(output_path, LANGUAGE, TYPE, PREFIX, os.path.basename(ptbfile).replace('.ptb','.txt')), 'w', 'utf-8' ) as text_write:
				command = './ptb_parser.sh ' +  str(ptbfile)
				text_format = subprocess.run(shlex.split(command), stdout=subprocess.PIPE)
                statement_word = []
                statement_tag = []
		        for line in text_format.stdout.decode('utf-8'):
                    if line=='SENTENCESTART':
                        if len(statement_word) > 1:
                            text_write.write('%s\ts\t' %(' '.join(statement_tag), ' '.join(statement_word)))
                        statement_word = []
                        statement_tag = []
                    else:
                        statement_word.append(line.split(' ')[0])
                        statement_tag.append(line.split(' ')[1])





def export_files(instance_set, file_path):
    with codecs.open(file_path, 'w', 'utf-8') as conll_conv_obj:
        for line in instance_set:
            conll_conv_obj.write(line)


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

    print(converstations[:3], news[:3])
    return set(converstations), set(news)


def main():
    # train:test:dev = 70:15:15
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    conll_output = []
    with codecs.open(input_file, 'r', 'utf-8') as conll_reader_obj:
        new_record_tag = []
        new_record_word = []
        labels = []
        vocab = []
        for i,line in enumerate(conll_reader_obj):
            tokens = line.split('\t')
            if len(tokens) == 10:
                if int(tokens[0]) == 1 and i != 0:
                    conll_output.append(' '.join(new_record_tag) + '\t' + ' '.join(new_record_word)+'\n')
                    new_record_tag = []
                    new_record_word = []
                if tokens[3].isalnum():
                    new_record_tag.append(tokens[3])
                    labels.append(tokens[3])
                else:
                    new_record_tag.append('PUN')
                    labels.append('PUN')
                new_record_word.append(tokens[1])
                vocab.append(tokens[1])

    test_instances = []
    input_bnc_path = '/Users/paggarwal/corpora/english/britishNationalCorpus/Texts'
    bnc_reader = BNCCorpusReader(root=input_bnc_path, fileids=r'[A-K]/\w*/\w*\.xml')
    conversation, news = get_bnc_parser_domain(input_bnc_path)
    for fileid in glob.glob(os.path.join(input_bnc_path, '*/*/KS*.xml')):
        if fileid in conversation:
            for sent in bnc_reader.tagged_sents(fileids=['/'.join(fileid.split('/')[-3:])], c5=True):
                word = []
                tags = []
                for word_tag_pair in sent:
                    if word_tag_pair[0] != '':
                        word.append(word_tag_pair[0])
                        vocab.append(word_tag_pair[0])
                        tags.append(word_tag_pair[1])
                        labels.append(word_tag_pair[1])
                test_instances.append(' '.join(tags) + '\t' + ' '.join(word) + '\n')
    export_files(test_instances, output_file + '_test.txt')



    train_ratio = 0.85
    total_instances = len(conll_output)
    print(round(train_ratio*total_instances))
    train_instances = conll_output[:int(round(train_ratio*total_instances))]
    val_instances = conll_output[int(round(train_ratio*total_instances)):]
    print('%s=%s+%s'%(total_instances, len(train_instances),len(val_instances)))
    export_files(train_instances, output_file+'_train.txt')
    export_files(val_instances, output_file+'_dev.txt')

    with codecs.open(output_file + '_label_vocab.txt', 'w', 'utf-8') as label_obj:
        for i, uniq_label in enumerate(set(labels)):
            label_obj.write('%s\t%s\n' %(uniq_label, i))

    with codecs.open(output_file+'_text_vocab.txt', 'w', 'utf-8') as vocab_obj:
        vocab_obj.write('%s\t%s\n' % ('<unk>', 0))
        vocab_obj.write('%s\t%s\n' % ('</s>', 1))
        for i, uniq_vocab in enumerate(set(vocab)):
            vocab_obj.write('%s\t%s\n' %(uniq_vocab,i+2))


if __name__ == '__main__':
    main()


