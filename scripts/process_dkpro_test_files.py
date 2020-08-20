#!usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
import subprocess
import shlex
import re
import glob
import os
from tqdm import tqdm


def coarse_mapper(map_path):
    mapper = {}
    extra_mapping = [':', '-LRB-', '-RRB-', '``', '$', 'BES', 'GW', '\'\'', '[', ']', '\"', 'NFP', '#', 'NIL']
    with codecs.open(map_path, 'r', 'utf-8') as mapper_obj:
        for line in mapper_obj:
            line = line.strip().rstrip('\r\n').replace('\n', '')
            if len(line) > 0:
                if line[0] != '#':
                    tags = line.split('=')
                    mapper[tags[0]] = tags[1].split('.')[-1]
    for tags in extra_mapping:
        if not tags in mapper.keys():
            mapper[tags] = 'POS_PUNCT'
    if not 'X' in mapper.keys():
        mapper['X'] = 'POS_NOUN'
    if not 'URL' in mapper.keys():
        mapper['URL'] = 'POS_NOUN'
    if not 'ADD' in mapper.keys():
        mapper['ADD'] = 'POS_X'
    if not 'USR' in mapper.keys():
        mapper['USR'] = 'POS_NOUN'
    if not '^RB' in mapper.keys():
        mapper['^RB'] = 'POS_ADV'
    if not 'XX' in mapper.keys():
        mapper['XX'] = 'POS_X'
    if not 'HT' in mapper.keys():
        mapper['HT'] = 'POS_X'
    if not 'APg' in mapper.keys():
        mapper['APg'] = 'POS_DET'
    if not 'DTg' in mapper.keys():
        mapper['DTg'] = 'POS_DET'
    if not 'RN' in mapper.keys():
        mapper['RN'] = 'POS_ADV'
    if not 'JJg' in mapper.keys():
        mapper['JJg'] = 'POS_ADJ'
    if not 'PRF' in mapper.keys():
        mapper['PRF'] = 'POS_ADP'

    return mapper


def load_control_files(entity, output_path):
    with codecs.open(output_path, 'w', 'utf-8') as entity_obj:
        for i, each_entity in enumerate(entity):
            entity_obj.write('%s\t%s\n' % (each_entity, i))




def parse_leipzig_output(input_path, mapper, output_path):
    print(input_path)
    words = []
    tags = []
    unique_tags = []
    vocab = []
    exclude_tokens = ['$', 'RT']
    exclude_tags = ['AFX', 'HYPH']
    with codecs.open(os.path.join(output_path, 'delta_' + os.path.basename(input_path)), 'w', 'utf-8') as leipgiz_output:
        with codecs.open(input_path, 'r', 'utf-8') as leipzig_obj:
            count = 0
            for line in tqdm(leipzig_obj):
                #print(line)
                count += 1
                line = line.strip().rstrip('\r\n').replace('\n', '')
                if len(line) == 0 and len(words) >= 1:
                    leipgiz_output.write('%s\t%s\n' % (' '.join(tags), ' '.join(words)))
                    words = []
                    tags = []
                elif len(line) == 0 and len(words) == 0:
                    continue
                else:
                    tokens = line.split('\t')
                    if tokens[1] == 'HT':
                        print(len(tokens))
                        print(line)
                        print(count)
                        print(tokens[0])
                    if tokens[0] in exclude_tokens:
                        continue
                    if tokens[1] in exclude_tags:
                        continue
                    if '|' in tokens[1]:
                        tokens[1] = tokens[1].split('|')[0]
                    words.append(tokens[0])
                    tags.append(mapper[tokens[1]])
                   # print(mapper[tokens[1]])
                    vocab.append(tokens[0])
                    unique_tags.append(mapper[tokens[1]])
        leipgiz_output.write('%s\t%s\n' % (' '.join(tags), ' '.join(words)))
    return set(vocab), set(unique_tags)


def main():
    input_path = '/Users/paggarwal/github_repos/model_cloning/data/test_results_dkpro_fine_tags'
    output_path = '/Users/paggarwal/github_repos/model_cloning/data/test_results_dkpro'
    mapper_path = '/Users/paggarwal/github_repos/model_cloning/mapper'

    #prepare train data for delta
    train_input_path = '/Users/paggarwal/github_repos/model_cloning/data/posTaggerEval/delta/train'
    mapper = coarse_mapper(os.path.join(mapper_path, 'en-ptb-pos.map'))
    c5_pos_tagger = ['stanford', 'OpenNlp', 'ClearNlp', 'MateTagger', 'Hepple']
    for shallow_train_file in glob.glob(os.path.join(input_path, '*HepplePosTagger*')):
        if any(tagger.lower() in shallow_train_file.lower() for tagger in c5_pos_tagger):
            print(c5_pos_tagger)
            mapper = coarse_mapper(os.path.join(mapper_path, 'en-ptb-pos.map'))
        elif 'arktweets' in shallow_train_file.lower():
            mapper = coarse_mapper(os.path.join(mapper_path, 'en-arktweet-pos.map'))
        elif 'treetagger' in shallow_train_file.lower():
            mapper = coarse_mapper(os.path.join(mapper_path, 'en-ptb-tt-pos.map'))

        overall_vocab, overall_unique_tags = parse_leipzig_output(shallow_train_file, mapper, output_path)

        # file loadings

        # overall_vocab = list(overall_vocab)
        # overall_vocab.insert(0, "</s>")
        # overall_vocab.insert(0, "<unk>")
        # load_control_files(overall_vocab, os.path.join(output_path, 'control', os.path.basename(shallow_train_file)
        #                                                + '_vocab.txt'))
        # load_control_files(overall_unique_tags, os.path.join(output_path, 'control', os.path.basename(shallow_train_file)
        #                                                      + '_tags.txt'))



if __name__ == '__main__':
    main()

