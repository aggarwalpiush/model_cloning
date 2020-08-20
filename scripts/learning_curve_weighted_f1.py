#! usr/bin/env python
# -*- coding : utf-8 -*-


import codecs
import glob
import os


def get_f1_support(filename):
    f1_scores = []
    support = []
    with codecs.open(filename, 'r', 'utf-8') as inf_obj:
        for line in inf_obj:
            while '  ' in line:
                line = line.replace('  ', ' ')
            line = line.replace('\r', '').replace('\n', '')
            line = line.strip()
            line_tokens = line.split(' ')
            if line_tokens[0].split('_')[0] == 'POS' and len(line_tokens) > 2:
                #print(line)
                f1_scores.append(line_tokens[3])
                support.append(line_tokens[4])
    return f1_scores, support


def weighted_f1_over_pos_method(each_pos_f1_list, each_pos_support_list):
    print(each_pos_f1_list)
    print(each_pos_support_list)
    pos_weighted_f1_score = []
    for i, element in enumerate(each_pos_f1_list):
        pos_size_weighted_f1_score = []
        for j, f1_score in enumerate(element):
            pos_size_weighted_f1_score.append(float(f1_score)*float(each_pos_support_list[i][j]))
        print(float(pos_size_weighted_f1_score[i]))
        print(sum([int(x) for x in each_pos_support_list[i]]))
        pos_weighted_f1_score.append(sum(pos_size_weighted_f1_score) / sum([int(x) for x in each_pos_support_list[i]]))
    return sum(pos_weighted_f1_score) / len(pos_weighted_f1_score)



def main():
    pos_method = ['clearnlp_mayo', 'clearnlp_ontonotes', 'opennlp_maxent', 'opennlp_perceptron', 'stanford_fast.41',
                  'hepple', 'mate', 'stanford_csls_dislstm', 'wsj_csls_dislstm']
    data_size_interval = ['10k', '100k', '200k', '250k', '300k',
                  '400k', '500k', '600k', '700k', '800k', '900k']
    input_dir = "/Users/paggarwal/github_repos/model_cloning/data/news_evalset"
    pos_size_weighted_f1 = {}
    for each_pos in pos_method:
        for each_size in data_size_interval:
            each_pos_f1_list = []
            each_pos_support_list = []
            if each_pos == 'hepple' and each_size == '600k':
                continue
            if each_pos == 'clearnlp_mayo' and each_size == '400k':
                continue
            if each_pos == 'clearnlp_ontonotes' and each_size == '600k':
                    continue
            if each_pos == 'opennlp_perceptron' and each_size == '600k':
                    continue
            if each_pos == 'wsj_csls_dislstm' and each_size == '600k':
                    continue
            for each_file in glob.glob(os.path.join(input_dir, '*'+each_pos+'*'+each_size+'*')):
                f1_scores, support = get_f1_support(each_file)
                each_pos_f1_list.append(f1_scores)
                each_pos_support_list.append(support)
            print(each_pos+'_'+each_size)
            pos_size_weighted_f1_score = weighted_f1_over_pos_method(each_pos_f1_list, each_pos_support_list)
            pos_size_weighted_f1[each_pos+'_'+each_size] = pos_size_weighted_f1_score

    with codecs.open(os.path.join(os.path.dirname(input_dir), 'learning_curve_scores.txt'), 'w', 'utf-8') as outf_obj:
        for key,value in pos_size_weighted_f1.items():
            outf_obj.write(str(key) + ', ' + str(value) + '\n')




if __name__ == "__main__":
    main()
