#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def calc_tokenes_per_sec(corpora):
    cloned_time_report_path = '/Users/paggarwal/github_repos/model_cloning/data/time_diff/clone_rates_2.tsv'
    orig_time_report_path = '/Users/paggarwal/github_repos/model_cloning/data/time_diff/original_rates_corrected_without_load.tsv'

    taggers = ['mayo', 'ontonotes', 'hepple', 'mate', 'dislstm-wsj', 'fast.41', 'maxent', 'perceptron', 'dislstm+wsj']

    tagger_clone_time = []
    tagger_orig_time = []
    percentage_tagger = []
    for tagger in taggers:
        corp_tagger_clone_time = []
        corp_tagger_orig_time = []
        for corp in corpora:
            with codecs.open(cloned_time_report_path, 'r', 'utf-8') as clon_obj:
                for line in clon_obj:
                    line_token = line.split('\t')
                    if tagger == 'dislstm-wsj':
                        if 'dislstm' in line_token[0].lower().strip() and 'nowsj' in line_token[0].lower().strip() \
                                and corp in line_token[0].lower().strip():
                            corp_tagger_clone_time.append(1000 / float(line_token[1].lower().replace('\n','').rstrip('\n\r')))
                    elif tagger == 'dislstm+wsj':
                        if 'dislstm' in line_token[0].lower().strip() and 'nowsj' not in line_token[0].lower().strip() \
                                and corp in line_token[0].lower().strip():
                            corp_tagger_clone_time.append(1000 / float(line_token[1].lower().replace('\n','').rstrip('\n\r')))
                    else:
                        if tagger in line_token[0].lower().strip() and corp in line_token[0].lower().strip():
                            corp_tagger_clone_time.append(1000 / float(line_token[1].lower().replace('\n', '').rstrip('\n\r')))
            with codecs.open(orig_time_report_path, 'r', 'utf-8') as orig_obj:
                for line in orig_obj:
                    line_token = line.split('\t')
                    if tagger == 'dislstm-wsj':
                        if 'distsim' in line_token[0].lower().strip() and 'wsj' not in line_token[0].lower().strip() \
                                and corp in line_token[0].lower().strip():
                            corp_tagger_orig_time.append(1000 / float(line_token[1].lower().replace('\n','').rstrip('\n\r')))
                    elif tagger == 'dislstm+wsj':
                        if 'distsim' in line_token[0].lower().strip() and 'wsj' in line_token[0].lower().strip() \
                                and corp in line_token[0].lower().strip():
                            corp_tagger_orig_time.append(1000 / float(line_token[1].lower().replace('\n','').rstrip('\n\r')))
                    else:
                        if tagger in line_token[0].lower().strip() and corp in line_token[0].lower().strip():
                            corp_tagger_orig_time.append(1000 / float(line_token[1].lower().replace('\n', '').rstrip('\n\r')))
        #print(corp_tagger_clone_time)
        #print(tagger + ' : cloned: ' + str(sum(corp_tagger_clone_time)/len(corp_tagger_clone_time)))
        #print(tagger + ' : original: ' + str(sum(corp_tagger_orig_time) / len(corp_tagger_orig_time)))
     #   print(tagger + ' : ' + str(((sum(corp_tagger_clone_time)/len(corp_tagger_clone_time) - sum(corp_tagger_orig_time) / len(corp_tagger_orig_time))
       #                            / (sum(corp_tagger_orig_time) / len(corp_tagger_orig_time)))*100))
        percentage_tagger.append(((sum(corp_tagger_clone_time)/len(corp_tagger_clone_time) - sum(corp_tagger_orig_time) / len(corp_tagger_orig_time))
                                   / (sum(corp_tagger_orig_time) / len(corp_tagger_orig_time)))*100)
        #print(corp_tagger_orig_time)
        tagger_clone_time.append(sum(corp_tagger_clone_time)/len(corp_tagger_clone_time))
        tagger_orig_time.append(sum(corp_tagger_orig_time) / len(corp_tagger_orig_time))
    #print(sum(percentage_tagger)/len(percentage_tagger))
    return [taggers, tagger_clone_time, tagger_orig_time]

def get_box_plot_data(labels, bp):
    rows_list = []

    for i in range(len(labels)):
        dict1 = {}
        dict1['label'] = labels[i]
        dict1['lower_whisker'] = bp['whiskers'][i * 2].get_ydata()[1]
        dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
        dict1['median'] = bp['medians'][i].get_ydata()[1]
        dict1['upper_quartile'] = bp['boxes'][i].get_ydata()[2]
        dict1['upper_whisker'] = bp['whiskers'][(i * 2) + 1].get_ydata()[1]
        rows_list.append(dict1)

    return pd.DataFrame(rows_list)


def generate_box_plot(data_points):
    labels = ['cloned_models', 'original_models']
    bp = plt.boxplot(data_points, labels=labels)
    print(get_box_plot_data(labels, bp))
    plt.show()


def main():
    spoken_corpus = ['gum-interview', 'swbd']
    social_corpus = ['gimpbel', 'nps_chat']
    formal_corpus = ['gum-news', 'gum-voyage', 'brown', 'gum-howto']
    social_corpus_time = calc_tokenes_per_sec(spoken_corpus)
    #print(formal_corpus_time )
    for i in range(len(social_corpus_time[0])):
        print("%s %s" %(social_corpus_time[1][i], social_corpus_time [0][i]))

    print("% difference")
    for i in range(len(social_corpus_time[0])):
        print("%s & %.2f & %.2f & +%.2f \\\\" %(social_corpus_time[0][i], float(social_corpus_time[1][i]), float(social_corpus_time[2][i]), (float(social_corpus_time[1][i])-float(social_corpus_time[2][i]))))
        #print("%s %s" % (float(formal_corpus_time[1][i])-float(formal_corpus_time[2][i]), formal_corpus_time[0][i]))
    #generate_box_plot(spoken_token_time)
    #social_token_time = calc_tokenes_per_sec(social_corpus)
    #generate_box_plot(social_token_time)
    #formal_token_time = calc_tokenes_per_sec(formal_corpus)
    #generate_box_plot(formal_token_time)
    print(sum(social_corpus_time[1]) / len(social_corpus_time[1]))
    print(sum(social_corpus_time[2])/len(social_corpus_time[2]))


if __name__ == '__main__':
    main()







