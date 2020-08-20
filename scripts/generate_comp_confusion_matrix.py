#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs
import os
from sklearn.metrics import confusion_matrix
import glob
import errno
import numpy as np
from heat_maps_confusion import make_confusion_matrix
import string

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def normalize_files_delta(format1_path, format2_path):
    with codecs.open(format1_path, 'r', 'utf-8') as frmt1_obj:
        sentense_size = []
        format1_tags = []
        format2_tags = []
        exclude_token_index = []
        for line in frmt1_obj:
            exclude_token_ind = []
            if len(line.strip()) == 0:
                continue
            line_tags = line.split('\t')[0]
            line_text = line.split('\t')[1].split(' ')
            while 'RT' in line_text:
                exclude_token_ind.append(line_text.index('RT'))
                line_text[line_text.index('RT')] = 'unk'
            line_tags = line_tags.split(' ')
            if len(line_tags) > 30:
                line_tags = line_tags[:30]
            format1_tags.append(line_tags)
            exclude_token_index.append(exclude_token_ind)
            sentense_size.append(len(line_tags))
    with codecs.open(format2_path, 'r', 'utf-8') as frmt2_obj:
        for i, line in enumerate(frmt2_obj):
            if len(line.strip()) == 0:
                continue
            line_tags = line.replace(
                '[', '').replace(']', '').replace('\n', '').replace(
                '\'', '').replace(' ', '').split(',')[:sentense_size[i]]
            format2_tags.append(line_tags)
    for i,indexes in enumerate(exclude_token_index):
        for ind in indexes:
            del format1_tags[i][ind]
            del format2_tags[i][ind]

    return format1_tags, format2_tags


def normalize_files_dkpro(format1_path, format2_path):
    with codecs.open(format1_path, 'r', 'utf-8') as frmt1_obj:
        format1_tags = []
        format2_tags = []
        exclude_token_index = []
        for line in frmt1_obj:
            exclude_token_ind = []
            if len(line.strip()) == 0:
                continue
            line_tags = line.split('\t')[0]
            line_text = line.split('\t')[1].split(' ')
            while 'RT' in line_text:
                exclude_token_ind.append(line_text.index('RT'))
                line_text[line_text.index('RT')] = 'unk'
            line_tags = line_tags.split(' ')
            if len(line_tags) > 30:
                line_tags = line_tags[:30]
            for ind in exclude_token_ind:
                del line_tags[ind]
            format1_tags.append(line_tags)
            exclude_token_index.append(exclude_token_ind)
    with codecs.open(format2_path, 'r', 'utf-8') as frmt2_obj:
        for line in frmt2_obj:
            if len(line.strip()) == 0:
                continue
            line_tags = line.split('\t')[0]
            line_tags = line_tags.split(' ')
            if len(line_tags) > 30:
                line_tags = line_tags[:30]
            format2_tags.append(line_tags)
    for i,indexes in enumerate(exclude_token_index):
        if len(format2_tags[i]) == 30:
            format2_tags[i] = format2_tags[i][:-len(indexes)]



    return format1_tags, format2_tags


def generate_text_to_consider(dkpro_file):
    dkpro_pos_tags = []
    with codecs.open(dkpro_file, 'r', 'utf-8') as in_obj:
        text_lines = []
        for line in in_obj:
            if len(line.strip()) == 0:
                continue
            text = line.split('\t')[1].split(' ')
            pos_tags = line.split('\t')[0].split(' ')
            if len(pos_tags) > 30:
                pos_tags = pos_tags[:30]
            text_lines.append(text)
            dkpro_pos_tags.append(pos_tags)
    return text_lines, dkpro_pos_tags

def generate_index_to_consider(text_lines, gold_file):
    index_to_consider = []
    gold_pos_tags = []
    with codecs.open(gold_file, 'r', 'utf-8') as gold_obj:
        for i, line in enumerate(gold_obj):
            indexes = []
            pos_tags = []
            gold_text = line.split('\t')[1].split(' ')
            gold_pos = line.split('\t')[0].split(' ')
            text_line_index = 0
            for j, tok in enumerate(gold_text):
                if tok == text_lines[i][text_line_index]:
                    text_line_index += 1
                    indexes.append(j)
                    pos_tags.append(gold_pos[j])
            if len(pos_tags) > 30:
                pos_tags = pos_tags[:30]
            gold_pos_tags.append(pos_tags)
            index_to_consider.append(indexes)
    return index_to_consider, gold_pos_tags

def generate_delta_pos_tags(dkpro_file, gold_file, delta_file):
    delta_pos_tags = []
    text_lines, dkpro_pos_tags = generate_text_to_consider(dkpro_file)
    index_to_consider, gold_pos_tags = generate_index_to_consider(text_lines, gold_file)
    with codecs.open(delta_file, 'r', 'utf-8') as delta_obj:
        for i, line in enumerate(delta_obj):
            actual_tags = []
            line_tags = line.replace(
                '[', '').replace(']', '').replace('\n', '').replace(
                '\'', '').replace(' ', '').split(',')
            for indexes in index_to_consider[i]:
                if indexes < 30:
                    actual_tags.append(line_tags[indexes])
            delta_pos_tags.append(actual_tags)
    return delta_pos_tags, dkpro_pos_tags, gold_pos_tags






def post_processed_generate_delta_pos_tags(delta_pos_tags, dkpro_file, dkpro_pos_tags, gold_pos_tags):
    print(len(delta_pos_tags))
    post_processed_delta_pos_tags = delta_pos_tags
    text_lines, _ = generate_text_to_consider(dkpro_file)
    for i, each_line in enumerate(text_lines):
        if len(gold_pos_tags[i]) == len(dkpro_pos_tags[i]) and len(gold_pos_tags[i]) == len(delta_pos_tags[i]):
            if len(each_line) > 30:
                each_line = each_line[:30]
            for j, tok in enumerate(each_line):
                #if any(ext.replace('\n','') not in string.punctuation for ext in tok): #TODO if all charcater in tok is in string punctuation
                 #    if delta_pos_tags[i][j] == "POS_PUNCT":
                #         print("tonen:%s",tok)
                #         print("dkpro:%s",dkpro_pos_tags[i][j])
                #         print("gold:%s",gold_pos_tags[i][j])
                #         print("delta:%s", delta_pos_tags[i][j])
                      #   post_processed_delta_pos_tags[i][j] = "POS_NOUN"
                if all(ext.replace('\n','') in string.punctuation for ext in tok):
                    if delta_pos_tags[i][j] == "POS_NOUN":
                        #print("tonen:%s",tok)
                        #print("dkpro:%s",dkpro_pos_tags[i][j])
                        #print("gold:%s",gold_pos_tags[i][j])
                        #print("delta:%s", delta_pos_tags[i][j])
                        post_processed_delta_pos_tags[i][j] = "POS_PUNCT"
    print(len(post_processed_delta_pos_tags))
    return post_processed_delta_pos_tags





def generate_confusion_report(pos_tag_gold, pos_tag_delta, pos_tag_dkpro, significance_report_path):
    #pos_labels = ["POS_ADP", "POS_ADV", "POS_CONJ", "POS_NOUN", "POS_PUNCT", "POS_ADJ", "POS_INTJ", "POS_PART",
     #             "POS_DET", "POS_NUM", "POS_X", "POS_PRON", "POS_VERB"]
    pos_labels = ["ADP", "ADV", "CONJ", "NOUN", "PUNCT", "ADJ", "INTJ", "PART",
                  "DET", "NUM", "X", "PRON", "VERB"]
    y_gold = []
    y_pred_dkpro = []
    y_pred_delta = []
    print(len(pos_tag_gold))
    print(len(pos_tag_dkpro))
    count = 0
    if len(pos_tag_gold) == len(pos_tag_dkpro) and len(pos_tag_gold) == len(pos_tag_delta):
        for i, tags in enumerate(pos_tag_gold):
            # print(i)
            # print(tags)
            # print(len(tags))
            # print(pos_tag_dkpro[i])
            # print(len(pos_tag_dkpro[i]))
            # print(pos_tag_delta[i])
            # print(len(pos_tag_delta[i]))
            if len(tags) != len(pos_tag_dkpro[i]) or len(tags) != len(pos_tag_delta[i]):
                count += 1
                continue
            for j, tag in enumerate(tags):
                y_gold.append(tag)
                y_pred_dkpro.append(pos_tag_dkpro[i][j])
                y_pred_delta.append(pos_tag_delta[i][j])
        print('missed %s' %count)
    else:
        raise NotImplementedError

    y_pred_dkpro = [x.replace('POS_','') for x in y_pred_dkpro]
    y_pred_delta = [x.replace('POS_', '') for x in y_pred_delta]
    y_gold = [x.replace('POS_', '') for x in y_gold]

    with codecs.open(significance_report_path, 'w', 'utf-8') as rep_obj:
        rep_obj.write(str(confusion_matrix(y_pred_dkpro, y_pred_delta, labels=pos_labels).ravel()))
        rep_obj.write("\n\n======================\n\n")
        rep_obj.write(str(confusion_matrix(y_pred_dkpro, y_pred_delta, labels=pos_labels)))
    # with codecs.open(report_path_delta, 'w', 'utf-8') as rep_obj:
    #     rep_obj.write(confusion_matrix(y_gold, y_pred_delta, labels=pos_labels).ravel())
    #     rep_obj.write("\n\n======================\n\n")
    #     rep_obj.write(confusion_matrix(y_gold, y_pred_delta, labels=pos_labels).ravel())
    print(len(y_pred_dkpro))
    print(y_pred_dkpro[:10])
    print(len(y_pred_delta))
    print(y_pred_delta[:10])
    return y_pred_dkpro, y_pred_delta, y_gold, pos_labels

def find_delta_file(mystrings, delta_files):
    searched_file = ''
    for f in delta_files:
        flag = 1
        for mystr in mystrings:
            if mystr.lower() not in os.path.basename(f).lower():
                flag = 0
        if flag == 1:
            searched_file = f
            break
    if searched_file == '':
        print(mystrings)

    return searched_file




def main():
    base_path = '/Users/paggarwal/github_repos/model_cloning/data'
    gold_files_path = os.path.join(base_path, 'test_results_gold')
    dkpro_files_path = os.path.join(base_path, 'test_results_dkpro')
    delta_files_path = os.path.join(base_path, 'test_results_delta')
    report_path = os.path.join(base_path, 'report_confusion')
    report_path1 = os.path.join(base_path, 'without_pos_prefix', 'report_structured_confusion')
    taggers = ['ClearNlpPosTagger', 'StanfordPosTagger', 'HepplePosTagger', 'OpenNlpPosTagger', 'MatePosTagger']
    taggers1 = ['HepplePosTagger']
    variants = {'StanfordPosTagger': ['wsj-0-18-caseless-left3words-distsim', 'caseless-left3words-distsim', 'fast.41'],
                'ClearNlpPosTagger': ['mayo', 'ontonotes'],
                'HepplePosTagger': ['novariant'],
                'OpenNlpPosTagger': ['perceptron', 'maxent'],
                'MatePosTagger': ['conll2009']}
    delta_files = []
    for delta_file in glob.glob(os.path.join(delta_files_path, '*')):
        delta_files.append(delta_file)

    testset = ['brown', 'gum-news', 'gum-voyage', 'gum-howto']



    y_news_dkpro = []
    y_news_delta = []
    y_news_gold = []

    for tagger in taggers:
        for variant in variants[tagger]:

            significance_news_report_path = os.path.join(report_path1, tagger, variant,
                                                         'news_confusion.rpt')

            for file in glob.glob(os.path.join(gold_files_path, '*')):
                if variant == 'wsj-0-18-caseless-left3words-distsim':
                    alias_variant = 'stanford_wsj_csls_dislstm'
                elif variant == 'caseless-left3words-distsim':
                    alias_variant = 'stanford_csls_dislstm'
                else:
                    alias_variant = variant
                if tagger in ['MatePosTagger', 'HepplePosTagger']:
                    strings = ['_'.join(os.path.basename(file).split('_')[:-1]).lower(),
                                tagger.lower().replace('postagger', '')]
                else:
                    strings = ['_'.join(os.path.basename(file).split('_')[:-1]).lower(), alias_variant.lower(),
                               tagger.lower().replace('postagger', '')]

                for dkpro_file in glob.glob(os.path.join(dkpro_files_path, '*')):
                    if tagger not in ['MatePosTagger', 'HepplePosTagger']:
                        if '_'.join(os.path.basename(file).split('_')[:-1]).lower() in os.path.basename(
                                dkpro_file).lower() and  tagger.lower().replace('postagger', '') in os.path.basename(
                                dkpro_file).lower() and variant.lower() in os.path.basename(dkpro_file).lower():
                                delta_file = find_delta_file(strings, delta_files)
                                if delta_file == '':
                                    raise NotImplementedError

                                dkpro_report_path = os.path.join(report_path1, tagger, variant,
                                                                 '_'.join(os.path.basename(file).split('_')[:-1]).lower(),
                                                                 '_'.join([tagger, variant, '_'.join(
                                                                     os.path.basename(file).split('_')[:-1]).lower()])+'_orig.rpt')
                                delta_report_path = os.path.join(report_path1, tagger, variant,
                                                                 '_'.join(os.path.basename(file).split('_')[:-1]).lower(),
                                                                 '_'.join([tagger, variant, '_'.join(
                                                                     os.path.basename(file).split('_')[:-1]).lower()])+'_cloned.rpt')
                                significance_report_path = os.path.join(report_path1, tagger, variant,
                                                                 '_'.join(
                                                                     os.path.basename(file).split('_')[:-1]).lower(),
                                                                 '_'.join([tagger, variant, '_'.join(
                                                                     os.path.basename(file).split('_')[
                                                                     :-1]).lower()]) + '_singnicance_confusion.rpt')
                                print(dkpro_report_path)
                                print(delta_report_path)
                                if not os.path.exists(os.path.dirname(dkpro_report_path)):
                                    os.makedirs(os.path.dirname(dkpro_report_path), exist_ok=True)

                                if not os.path.exists(os.path.dirname(delta_report_path)):
                                    os.makedirs(os.path.dirname(delta_report_path), exist_ok=True)

                                if not os.path.exists(os.path.dirname(significance_report_path)):
                                    os.makedirs(os.path.dirname(significance_report_path), exist_ok=True)

                                delta_pos_tags, dkpro_pos_tags, gold_pos_tags = generate_delta_pos_tags(dkpro_file, file,
                                                                                                        delta_file)

                               # post_processed_delta_pos_tags = post_processed_generate_delta_pos_tags(delta_pos_tags,
                                                #                                                       dkpro_file,
                                                 #                                                      dkpro_pos_tags,
                                                  #                                                     gold_pos_tags)

                                y_pred_dkpro, y_pred_delta, y_gold, pos_labels = generate_confusion_report(gold_pos_tags, delta_pos_tags, dkpro_pos_tags,
                                                          significance_report_path)
                                if any(ext in significance_report_path for ext in testset):
                                    y_news_dkpro += y_pred_dkpro
                                    y_news_delta += y_pred_delta
                                    y_news_gold += y_gold

                                #generate_classification_report(gold_pos_tags, delta_pos_tags, dkpro_pos_tags,
                                                              # os.path.join(report_path, os.path.basename(dkpro_file) + '.rpt'),
                                                               #os.path.join(report_path, os.path.basename(delta_file) + '.rpt'))
                    else:
                        if '_'.join(os.path.basename(file).split('_')[:-1]).lower() in os.path.basename(
                                dkpro_file).lower() and tagger.lower().replace('postagger', '') in os.path.basename(
                            dkpro_file).lower():
                            delta_file = find_delta_file(strings, delta_files)
                            if delta_file == '':
                                raise NotImplementedError

                            dkpro_report_path = os.path.join(report_path1, tagger,
                                                             '_'.join(os.path.basename(file).split('_')[:-1]).lower(),
                                                             '_'.join([ tagger, '_'.join(
                                                                 os.path.basename(file).split('_')[
                                                                 :-1]).lower()]) + '_orig.rpt')
                            delta_report_path = os.path.join(report_path1, tagger,
                                                             '_'.join(os.path.basename(file).split('_')[:-1]).lower(),
                                                             '_'.join([ tagger, '_'.join(
                                                                 os.path.basename(file).split('_')[
                                                                 :-1]).lower()]) + '_cloned.rpt')
                            significance_report_path = os.path.join(report_path1, tagger, variant,
                                                                    '_'.join(
                                                                        os.path.basename(file).split('_')[:-1]).lower(),
                                                                    '_'.join([tagger, variant, '_'.join(
                                                                        os.path.basename(file).split('_')[
                                                                        :-1]).lower()]) + '_singnicance_confusion.rpt')


                            print(dkpro_report_path)
                            print(delta_report_path)
                            if not os.path.exists(os.path.dirname(dkpro_report_path)):
                                os.makedirs(os.path.dirname(dkpro_report_path), exist_ok=True)

                            if not os.path.exists(os.path.dirname(delta_report_path)):
                                os.makedirs(os.path.dirname(delta_report_path), exist_ok=True)

                            if not os.path.exists(os.path.dirname(significance_report_path)):
                                os.makedirs(os.path.dirname(significance_report_path), exist_ok=True)

                            delta_pos_tags, dkpro_pos_tags, gold_pos_tags = generate_delta_pos_tags(dkpro_file, file,
                                                                                                    delta_file)

                            #post_processed_delta_pos_tags = post_processed_generate_delta_pos_tags(delta_pos_tags,
                             #                                                                      dkpro_file,
                              #                                                                     dkpro_pos_tags,
                               #                                                                    gold_pos_tags)
                            y_pred_dkpro, y_pred_delta, y_gold, pos_labels = generate_confusion_report(
                                gold_pos_tags, delta_pos_tags, dkpro_pos_tags,
                                                           significance_report_path)

                            if any(ext in significance_report_path for ext in testset):
                                y_news_dkpro += y_pred_dkpro
                                y_news_delta += y_pred_delta
                                y_news_gold += y_gold
            print(len(y_news_dkpro))
            print(len(y_news_delta))

            categories = pos_labels
            print(np.reshape(list(confusion_matrix(y_news_dkpro, y_news_delta, labels=pos_labels).ravel()), (-1, 13)))
            conf_mat = np.reshape(list(confusion_matrix(y_news_dkpro, y_news_delta,
                                                                               labels=pos_labels).ravel()), (-1, 13))
            np.fill_diagonal(conf_mat, 0)
            #print(conf_mat)
            make_confusion_matrix(conf_mat,
                                  categories=categories, xyplotlabels=False, sum_stats=False,
                                  save_path=os.path.join(os.path.dirname(significance_news_report_path), 'heatmap_no_diaginal.png'),
                                  count=False, percent=False, cmap='OrRd', figsize=(10,9))
            with codecs.open(significance_news_report_path, 'w', 'utf-8') as rep_obj:
                rep_obj.write(str(list(confusion_matrix(y_news_dkpro, y_news_delta, labels=pos_labels).ravel())))
                #print(r.stuart.maxwell(r.matrix(r.c(confusion_matrix(y_news_dkpro, y_news_dkpro, labels=pos_labels).ravel()), 13, 13)))

                rep_obj.write("\n\n======================\n\n")
                rep_obj.write(str(confusion_matrix(y_news_dkpro, y_news_delta, labels=pos_labels)))
                            # generate_classification_report(gold_pos_tags, delta_pos_tags, dkpro_pos_tags,
                            # os.path.join(report_path, os.path.basename(dkpro_file) + '.rpt'),
                            # os.path.join(report_path, os.path.basename(delta_file) + '.rpt'))






if __name__ == '__main__':
    main()

