#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs
import subprocess
import shlex
import glob
from tqdm import tqdm



def main():
    taggers = ['ClearNlpPosTagger', 'StanfordPosTagger', 'HepplePosTagger', 'OpenNlpPosTagger', 'MatePosTagger']
    variants = {'StanfordPosTagger': ['wsj-0-18-caseless-left3words-distsim', 'caseless-left3words-distsim', 'fast.41'],
               'ClearNlpPosTagger': ['mayo', 'ontonotes'],
               'HepplePosTagger': [''],
               'OpenNlpPosTagger': ['perceptron', 'maxent'],
               'MatePosTagger': ['conll2009']}

    test_path = '/home/LTLab.lan/paggarwal/model_clone/test_files_wo_labels'
    for tagger in taggers:
        print(tagger)
        for variant in variants[tagger]:
            print(variant)
            for test_file in tqdm(glob.glob(test_path + '/*')):
                output_path = ('.'.join(test_file.split('.')[':-1']) + '_%s_%s.out' % (tagger, variant))
                log_path =  ('.'.join(test_file.split('.')[':-1']) + '_%s_%s.log' % (tagger, variant))
                cmd = shlex.split("java -Xmx30g -jar /home/LTLab.lan/paggarwal/model_clone/jars/clearnlp-0.0.1-SNAPSHOT-standalone.jar %s %s %s %s"
                                  % (test_file, tagger, variant, output_path))
                with codecs.open(log_path, 'w', 'utf-8') as f:
                    p = subprocess.Popen(cmd, stdout=f, stderr=f)
                    p.wait()