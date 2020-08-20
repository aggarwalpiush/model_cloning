#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs


delta_file = '/Users/paggarwal/github_repos/model_cloning/data/test_results_delta/brown_tei_test.txtdelta_leipzig_1M_sent_corpus_clearnlp_mayo_pos_train.txt_infer.res'
dkpro_file = '/Users/paggarwal/github_repos/model_cloning/data/test_results_dkpro/delta_brown_tei_test_wo_lab_ClearNlpPosTagger_mayo.out'
gold_file = '/Users/paggarwal/github_repos/model_cloning/data/test_results_gold/brown_tei_test.txt'


with codecs.open(delta_file, 'r', 'utf-8') as delta_obj:
    delta_tags = []
    for line in delta_obj:
        line = line.strip().replace('\n','')
        tags = line.split(',')
        delta_tags.append(tags)

with codecs.open(dkpro_file, 'r', 'utf-8') as dkpro_obj:
    dkpro_tags = []
    for line in dkpro_obj:
        line = line.strip().replace('\n','')
        tags = line.split('\t')[0].split(' ')
        dkpro_tags.append(tags)

with codecs.open(gold_file, 'r', 'utf-8') as gold_obj:
    gold_tags = []
    sentence = []
    for line in gold_obj:
        line = line.strip().replace('\n','')
        tags = line.split('\t')[0].split(' ')
        tokens = line.split('\t')[1].split(' ')
        gold_tags.append(tags)
        sentence.append(tokens)

for j, sent in enumerate(sentence):
    for i, tok in enumerate(sent):
        try:
            if '.' in tok:
                if not gold_tags[j][i].strip() == delta_tags[j][i].replace('\'', '').strip():
                    print(tok)
                    print("delta tag : %s" %delta_tags[j][i].replace('\'', ''))

                    print("dkpro tag : %s" % dkpro_tags[j][i])
                    print("gold tag : %s" % gold_tags[j][i])
        except IndexError:
            pass
