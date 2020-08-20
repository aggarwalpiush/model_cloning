#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs
import sys
import os
from sklearn.metrics import classification_report
import subprocess
import shlex
import glob


def deltaf_to_pos_tags_evaluation(inputpath) -> list:
    pos_tags = []
    with codecs.open(inputpath, 'r', 'utf-8') as delta_file_obj:
        for line in delta_file_obj:
            parts = line.split('\t')
            tags = parts[0].split(' ')
            words = parts[1].rstrip().replace('\r\n', '').split(' ')
            for i, tag in enumerate(tags):
                pos_tags.append([tag, words[i]])
    return pos_tags


def get_model_pos_tags(input_path):
    pos_tags = []
    with codecs.open(input_path, 'r', 'utf-8') as inp_obj:
        for line in inp_obj:
            line = line.strip().replace('\n', ''). rstrip('\r\n')
            tag_pair = line.split('\t')
            if len(tag_pair) == 2:
                pos_tags.append(tag_pair)
    return pos_tags


def generate_classification_report(pos_tag_gold, pos_tag_pred, report_path):
    pos_labels = ["POS_ADP","POS_ADV","POS_CONJ","POS_NOUN","POS_PUNCT","POS_ADJ","POS_INTJ","POS_PART",
              "POS_DET","POS_NUM","POS_X","POS_PRON","POS_VERB"]
    y_gold = []
    y_pred = []
    if  (len(pos_tag_gold) == len(pos_tag_pred)):
        for i, tag_pair in enumerate(pos_tag_gold):
            y_gold.append(tag_pair[1])
            y_pred.append(pos_tag_pred[i][1])

    with codecs.open(report_path, 'w', 'utf-8') as rep_obj:
        rep_obj.write(classification_report(y_gold, y_pred, labels=pos_labels))




def main():
    taggers = ['ClearNlpPosTagger', 'StanfordPosTagger', 'HepplePosTagger', 'OpenNlpPosTagger', 'MatePosTagger']
    variants = {'StanfordPosTagger': ['wsj-0-18-caseless-left3words-distsim', 'caseless-left3words-distsim', 'fast.41'],
               'ClearNlpPosTagger': ['mayo', 'ontonotes'],
               'HepplePosTagger': [''],
               'OpenNlpPosTagger': ['perceptron', 'maxent'],
               'MatePosTagger': ['conll2009']}

    test_path = ''
    for tagger in taggers:
        for variant in variants[tagger]:
            for test_file in glob.glob(test_path + '/*'):
                output_path = ('.'.join(test_file.split('.')[':-1']) + '_%s_%s.out' % (tagger, variant))
                log_path =  ('.'.join(test_file.split('.')[':-1']) + '_%s_%s.log' % (tagger, variant))
                cmd = shlex.split("java -Xmx30g -jar clearnlp-0.0.1-SNAPSHOT-standalone.jar %s %s %s %s"
                                  % (test_file, tagger, variant, output_path))
                with codecs.open(log_path, 'w', 'utf-8') as f:
                    p = subprocess.Popen(cmd, stdout=f, stderr=f)
                    p.wait()
    original_path = 'some delta_path_testfiles'
    report_path = 'some report path'
    for eachfile in glob.glob(test_path + '/*.out'):
        model_pos_tags = get_model_pos_tags(eachfile)
        gold_pos_tags = deltaf_to_pos_tags_evaluation(os.path.join(original_path, os.path.basename(eachfile)))
        generate_classification_report(model_pos_tags, gold_pos_tags, os.path.join(report_path, os.path.basename(eachfile), '.rpt'))


if __name__ == '__main__':
    main()






