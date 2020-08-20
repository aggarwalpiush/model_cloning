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
    if not '^RB' in mapper.keys():
        mapper['^RB'] = 'POS_ADV'
    if not 'XX' in mapper.keys():
        mapper['XX'] = 'POS_X'
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


def parse_ptb(input_path, mapper):
    command = './ptb_parser.sh ' + str(input_path)
    text_format = subprocess.run(shlex.split(command), stdout=subprocess.PIPE)
    words = []
    tags = []
    unique_tags = []
    vocab = []
    tag_sentences_pairs = []
    lines = text_format.stdout.decode('utf-8').split('\n')
    for line in lines:
        line = line.strip().rstrip('\r\n').replace('\n', '')
        if len(line) > 1:
            #print(line)
            if line == 'SENTENCESTART':
                if len(words) > 1:
                    tag_sentences_pairs.append('%s\t%s' % (' '.join(tags), ' '.join(words)))
                words = []
                tags = []
            else:
                words.append(line.split(' ')[0])
                vocab.append(line.split(' ')[0])
                map_tag = mapper[line.split(' ')[1].rstrip('\r\n').replace('\n','')]
                tags.append(map_tag)
                unique_tags.append(map_tag)
    tag_sentences_pairs.append('%s\t%s' % (' '.join(tags), ' '.join(words)))
    return tag_sentences_pairs, set(vocab), set(unique_tags)


def parse_brown(input_path, mapper):
    tag_sentences_pairs = []
    words = []
    tags = []
    unique_tags = []
    vocab = []
    with codecs.open(input_path, 'r', 'utf-8') as input_obj:
        for line in input_obj:
            if '<s n=' in line:
                line_tokens = line.split('<')
                for tok in line_tokens:
                    if 's n=' in tok:
                        words = []
                        tags = []
                        word_pair = tok.replace('s n=', '').replace('"', '').replace('>', '')
                        print(word_pair.split(' ')[0])
                    if 'w type=' in tok or 'c type=' in tok:
                        word_pair = tok.replace('w type=', '').replace('c type=', '').replace('"', '').replace('>', ' ')
                        if not word_pair.split(' ')[0] == 'NIL':
                            words.append(word_pair.split(' ')[-1])
                            vocab.append(word_pair.split(' ')[-1])
                            map_tag = mapper[word_pair.split(' ')[0]]
                            tags.append(map_tag)
                            unique_tags.append(map_tag)
                if len(words) >= 1:
                    tag_sentences_pairs.append('%s\t%s' % (' '.join(tags), ' '.join(words)))
    return tag_sentences_pairs, set(vocab), set(unique_tags)


def parse_switchboard(input_path, mapper):
    tag_sentences_pairs = []
    words = []
    tags = []
    unique_tags = []
    vocab = []
    with codecs.open(input_path, 'r', 'utf-8') as swbd_obj:
        for line in swbd_obj:
            if not '*x*' in line or '==' in line or re.match(r'^\s*$', line):
                tagged_pairs = line.split(' ')
                if len(words) > 1:
                    tag_sentences_pairs.append('%s\t%s' % (' '.join(tags), ' '.join(words)))
                    words = []
                    tags = []
                for tagged_pair in tagged_pairs:
                    if '/' in tagged_pair:
                        my_tag = tagged_pair.split('/')[1].replace('\n', '')
                        if my_tag in mapper.keys():
                            words.append(tagged_pair.split('/')[0])
                            vocab.append(tagged_pair.split('/')[0])
                            map_tag = mapper[my_tag]
                            tags.append(map_tag)
                            unique_tags.append(map_tag)
    tag_sentences_pairs.append('%s\t%s' % (' '.join(tags), ' '.join(words)))
    return tag_sentences_pairs, set(vocab), set(unique_tags)


def parse_nps_irc(input_path, mapper):
    tag_sentences_pairs = []
    words = []
    tags = []
    unique_tags = []
    vocab = []
    unwanted_tokens = ['apos', '^', 'X']
    with codecs.open(input_path, 'r', 'utf-8') as nps_file_obj:
        for line in nps_file_obj:
            if '<Post class=' in line and len(words) > 1:
                tag_sentences_pairs.append('%s\t%s' % (' '.join(tags), ' '.join(words)))
                words = []
                tags = []
            if 't pos=' in line:
                tokens = line.strip().split(' ')
                if len(tokens) == 3:
                    tag = tokens[1].split('=')[1].replace('"', '')
                    word = tokens[2].split('=')[1].replace('"', '').replace('/>', '').rstrip('\r\n').replace('\n', '')
                    if len(tag) > 0 and len(word) > 0:
                        flag = True
                        for ut in unwanted_tokens:
                            if ut in tag or ut in word:
                                flag = False
                        if flag:
                            words.append(word)
                            tags.append(mapper[tag])
                            vocab.append(word)
                            unique_tags.append(mapper[tag])
        tag_sentences_pairs.append('%s\t%s' % (' '.join(tags), ' '.join(words)))
        return tag_sentences_pairs, set(vocab), set(unique_tags)


def parse_gimpbel(input_path, mapper):
    tag_sentences_pairs = []
    words = []
    tags = []
    unique_tags = []
    vocab = []
    with codecs.open(input_path, 'r', 'utf-8') as gimpbel_obj:
        for line in gimpbel_obj:
            line = line.strip().rstrip('\r\n').replace('\n', '')
            print(line)
            if len(line) == 0 and len(words) >= 1:
                tag_sentences_pairs.append('%s\t%s' % (' '.join(tags), ' '.join(words)))
                words = []
                tags = []
            else:
                if not len(line) == 0:
                    tokens = line.split('\t')
                    if len(tokens) == 2:
                        my_tag = tokens[1].replace('\n', '')
                        if my_tag in mapper.keys():
                            words.append(tokens[0])
                            tags.append(mapper[tokens[1].replace('\n','')])
                            vocab.append(tokens[0])
                            unique_tags.append(mapper[tokens[1].replace('\n','')])
    tag_sentences_pairs.append('%s\t%s' % (' '.join(tags), ' '.join(words)))
    return tag_sentences_pairs, set(vocab), set(unique_tags)


def parse_leipzig_output(input_path, mapper, output_path):
    print(input_path)
    words = []
    tags = []
    unique_tags = []
    vocab = []
    exclude_tokens = ['$', 'RT']
    exclude_tags = ['AFX', 'HYPH', 'ADD']
    with codecs.open(os.path.join(output_path, 'delta_' + os.path.basename(input_path)), 'w', 'utf-8') as leipgiz_output:
        with codecs.open(input_path, 'r', 'utf-8') as leipzig_obj:
            for line in tqdm(leipzig_obj):
                #print(line)
                line = line.strip().rstrip('\r\n').replace('\n', '')
                if len(line) == 0 and len(words) >= 1:
                    leipgiz_output.write('%s\t%s\n' % (' '.join(tags), ' '.join(words)))
                    words = []
                    tags = []
                else:
                    tokens = line.split('\t')
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
    input_path = '/Users/paggarwal/corpora/english'
    output_path = '/Users/paggarwal/github_repos/model_cloning/data/posTaggerEval/delta/english'
    tok_output_path = '/Users/paggarwal/github_repos/model_cloning/data/posTaggerEval/english/formal'
    mapper_path = '/Users/paggarwal/github_repos/model_cloning/mapper'

    #prepare train data for delta
    train_input_path = '/Users/paggarwal/github_repos/model_cloning/data/posTaggerEval/delta/train'
    mapper = coarse_mapper(os.path.join(mapper_path, 'en-ptb-pos.map'))
    c5_pos_tagger = ['stanford', 'OpenNlp', 'ClearNlp', 'MateTagger', 'Hepple']
    for shallow_train_file in glob.glob(os.path.join(train_input_path, 'leipzig_1M_sent_corpus_hepple*_pos_train.txt')):
        if any(tagger.lower() in shallow_train_file for tagger in c5_pos_tagger):
            mapper = coarse_mapper(os.path.join(mapper_path, 'en-ptb-pos.map'))
        elif 'Arktweets' in shallow_train_file:
            mapper = coarse_mapper(os.path.join(mapper_path, 'en-arktweet-pos.map'))
        elif 'TreeTagger' in shallow_train_file:
            mapper = coarse_mapper(os.path.join(mapper_path, 'en-ptb-tt-pos.map'))

        overall_vocab, overall_unique_tags = parse_leipzig_output(shallow_train_file, mapper, output_path)

        # file loadings

        overall_vocab = list(overall_vocab)
        overall_vocab.insert(0, "</s>")
        overall_vocab.insert(0, "<unk>")
        load_control_files(overall_vocab, os.path.join(output_path, 'control', os.path.basename(shallow_train_file)
                                                       + '_vocab.txt'))
        load_control_files(overall_unique_tags, os.path.join(output_path, 'control', os.path.basename(shallow_train_file)
                                                             + '_tags.txt'))



    # prepare test data for delta
    # -----------------------------
    # -----------------------------
    # parse gum corpus for delta
    # overall_vocab = []
    # overall_unique_tags = []
    # mapper = coarse_mapper(os.path.join(mapper_path, 'en-ptb-pos.map'))
    # gum_types = ['gum-howto', 'gum-voyage', 'gum-news', 'gum-interview']
    # for gum_type in gum_types:
    #     overall_sentence_pair = []
    #     for ptbfile in glob.glob(os.path.join(input_path, 'gum', '*.ptb')):
    #         print(ptbfile)
    #         if gum_type.replace('-', '_').replace('howto', 'whow') in ptbfile.lower():
    #             tag_sentences_pairs, vocab, unique_tags = parse_ptb(ptbfile, mapper)
    #             print(len(tag_sentences_pairs))
    #             overall_sentence_pair.append(tag_sentences_pairs)
    #             overall_vocab += vocab
    #             overall_unique_tags += unique_tags
    #
    #     # file loading for comparison with dkpro pos taggers
    #     with codecs.open(os.path.join(tok_output_path, gum_type + '_test_tokens.txt'), 'w', 'utf-8') as gum_tok_output:
    #         for line in overall_sentence_pair:
    #             for each_sent in line:
    #                 tags = each_sent.split('\t')[0].split()
    #                 tokens = each_sent.split('\t')[1].split()
    #                 for i,tok in enumerate(tokens):
    #                     gum_tok_output.write('%s %s\n' %(tok, tags[i]))

        # file loadings
        # with codecs.open(os.path.join(output_path, gum_type + '_test.txt'), 'w', 'utf-8') as gum_output:
        #     for line in overall_sentence_pair:
        #         for each_sent in line:
        #             gum_output.write(each_sent + '\n' )
        # overall_vocab = list(set(overall_vocab))
        # overall_vocab.insert(0, "</s>")
        # overall_vocab.insert(0, "<unk>")
        # overall_unique_tags = list(set(overall_unique_tags))
        # load_control_files(overall_vocab, os.path.join(output_path, 'control', gum_type + '_vocab.txt'))
        # load_control_files(overall_unique_tags, os.path.join(output_path, 'control', gum_type + '_tags.txt'))

    # # parse brown corpus for delta
    # overall_sentence_pair = []
    # overall_vocab = []
    # overall_unique_tags = []
    # mapper = coarse_mapper(os.path.join(mapper_path, 'en-browntei-pos.map'))
    # for brown_tei_file in glob.glob(os.path.join(input_path, 'brown_tei', '*.xml')):
    #     print(brown_tei_file)
    #     tag_sentences_pairs, vocab, unique_tags = parse_brown(brown_tei_file, mapper)
    #     print(len(tag_sentences_pairs))
    #     overall_sentence_pair.append(tag_sentences_pairs)
    #     overall_vocab += vocab
    #     overall_unique_tags += unique_tags
    #
    # # file loadings
    # with codecs.open(os.path.join(output_path, 'brown_tei' + '_test.txt'), 'w', 'utf-8') as brown_output:
    #     for line in overall_sentence_pair:
    #         for each_sent in line:
    #             brown_output.write(each_sent + '\n')
    # overall_vocab = list(set(overall_vocab))
    # overall_vocab.insert(0, "</s>")
    # overall_vocab.insert(0, "<unk>")
    # overall_unique_tags = list(set(overall_unique_tags))
    # load_control_files(overall_vocab, os.path.join(output_path, 'control', 'brown_tei' + '_vocab.txt'))
    # load_control_files(overall_unique_tags, os.path.join(output_path, 'control', 'brown_tei' + '_tags.txt'))
    #
    # # parse switch board
    # overall_sentence_pair = []
    # overall_vocab = []
    # overall_unique_tags = []
    # mapper = coarse_mapper(os.path.join(mapper_path, 'en-ptb-pos.map'))
    # for swbd_file in glob.glob(os.path.join(input_path, 'switchboard', 'swbd', '*/*.pos')):
    #     tag_sentences_pairs, vocab, unique_tags = parse_switchboard(swbd_file, mapper)
    #     overall_sentence_pair.append(tag_sentences_pairs)
    #     overall_vocab += vocab
    #     overall_unique_tags += unique_tags
    #
    # # file loadings
    # with codecs.open(os.path.join(output_path, 'swbd' + '_test.txt'), 'w', 'utf-8') as swbd_output:
    #     for line in overall_sentence_pair:
    #         for each_sent in line:
    #             swbd_output.write(each_sent + '\n')
    # overall_vocab = list(set(overall_vocab))
    # overall_vocab.insert(0, "</s>")
    # overall_vocab.insert(0, "<unk>")
    # overall_unique_tags = list(set(overall_unique_tags))
    # load_control_files(overall_vocab, os.path.join(output_path, 'control', 'swbd' + '_vocab.txt'))
    # load_control_files(overall_unique_tags, os.path.join(output_path, 'control', 'swbd' + '_tags.txt'))
    #
    #
    # # parse nps_irc
    # overall_sentence_pair = []
    # overall_vocab = []
    # overall_unique_tags = []
    # mapper = coarse_mapper(os.path.join(mapper_path, 'en-ptb-pos.map'))
    # for nps_file in glob.glob(os.path.join(input_path, 'nps_chat', '*.xml')):
    #     tag_sentences_pairs, vocab, unique_tags = parse_nps_irc(nps_file, mapper)
    #     overall_sentence_pair.append(tag_sentences_pairs)
    #     overall_vocab += vocab
    #     overall_unique_tags += unique_tags
    #
    # # file loadings
    # with codecs.open(os.path.join(output_path, 'nps_chat' + '_test.txt'), 'w', 'utf-8') as nps_chat_output:
    #     for line in overall_sentence_pair:
    #         for each_sent in line:
    #             nps_chat_output.write(each_sent + '\n')
    # overall_vocab = list(set(overall_vocab))
    # overall_vocab.insert(0, "</s>")
    # overall_vocab.insert(0, "<unk>")
    # overall_unique_tags = list(set(overall_unique_tags))
    # load_control_files(overall_vocab, os.path.join(output_path, 'control', 'nps_chat' + '_vocab.txt'))
    # load_control_files(overall_unique_tags, os.path.join(output_path, 'control', 'nps_chat' + '_tags.txt'))
    #
    #
    # # parse gimpbel
    # mapper = coarse_mapper(os.path.join(mapper_path, 'en-arktweet-pos.map'))
    # gimpel_file = os.path.join(input_path, 'gimpbel', 'gimpel.txt')
    # overall_sentence_pair, overall_vocab, overall_unique_tags = parse_gimpbel(gimpel_file, mapper)
    #
    # # file loadings
    # with codecs.open(os.path.join(output_path, 'gimpbel' + '_test.txt'), 'w', 'utf-8') as gimpbel_output:
    #     for line in overall_sentence_pair:
    #         gimpbel_output.write(line + '\n')
    # overall_vocab = list(overall_vocab)
    # overall_vocab.insert(0, "</s>")
    # overall_vocab.insert(0, "<unk>")
    # overall_unique_tags = list(set(overall_unique_tags))
    # load_control_files(overall_vocab, os.path.join(output_path, 'control', 'gimpbel' + '_vocab.txt'))
    # load_control_files(overall_unique_tags, os.path.join(output_path, 'control', 'gimpbel' + '_tags.txt'))


if __name__ == '__main__':
    main()

