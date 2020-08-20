#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs
import os
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


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
        print("median = " + str(bp['medians'][i].get_ydata()[1])+',')
        print("upper quartile = " + str(bp['boxes'][i].get_ydata()[2]) + ',')
        print("lower quartile = " + str(bp['boxes'][i].get_ydata()[1]) + ',')
        print("upper whisker = " + str(bp['whiskers'][(i * 2) + 1].get_ydata()[1]) + ',')
        print("lower whisker = " + str(bp['whiskers'][i * 2].get_ydata()[1]))
    return pd.DataFrame(rows_list)


def generate_box_plot(data_points):
    labels = ['f1']
    bp = plt.boxplot(data_points, labels=labels)
    print(get_box_plot_data(labels, bp))
    plt.show()


def calc_score(type_corpus, taggers):
    dir_path = "/Users/paggarwal/github_repos/model_cloning/data/postprocessed_noun/report_structured"
    tag_f1 = {}
    for tag in taggers:
        score = []
        for sp_c in type_corpus:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.endswith(".rpt"):
                        if sp_c in os.path.basename(file) and tag in os.path.basename(file):
                            with codecs.open(os.path.join(root, file), 'r', 'utf-8') as inf_obj:
                                for line in inf_obj:
                                    while '  ' in line:
                                        line = line.replace('  ', ' ')
                                    line = line.replace('\r', '').replace('\n', '')
                                    line = line.strip()
                                    line_tokens = line.split(' ')
                                    if 'weighted' in line_tokens[0]:
                                        score.append(float(line_tokens[-2]))
        tag_f1[tag] = str(sum(score)/len(score))
    print(tag_f1)
    average_f1 = []
    for k,v in tag_f1.items():
        average_f1.append(float(v))
    print('Average: %s' %format(sum(average_f1)/len(average_f1)))

def generate_score(type_corpus, taggers):
    dir_path = "/Users/paggarwal/github_repos/model_cloning/data/postprocessed_noun/report_structured"
    tagger_f1 = []
    for sp_c in type_corpus:
        score = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".rpt"):
                    if sp_c in os.path.basename(file):
                        with codecs.open(os.path.join(root, file), 'r', 'utf-8') as inf_obj:
                            for line in inf_obj:
                                while '  ' in line:
                                    line = line.replace('  ', ' ')
                                line = line.replace('\r', '').replace('\n', '')
                                line = line.strip()
                                line_tokens = line.split(' ')
                                if 'weighted' in line_tokens[0]:
                                    score.append(float(line_tokens[-2]))
        tagger_f1.append(sum(score)/len(score))
    return [tagger_f1]

def main():
    taggers = ['MatePosTagger', 'StanfordPosTagger_fast.41', 'HepplePosTagger', 'OpenNlpPosTagger_perceptron',
               'ClearNlpPosTagger_ontonotes', 'StanfordPosTagger_wsj-0-18-caseless-left3words-distsim',
               'ClearNlpPosTagger_mayo', 'OpenNlpPosTagger_maxent', 'StanfordPosTagger_caseless-left3words-distsim']
    spoken_cloned = ['gum-interview_cloned', 'swbd_cloned']
    spoken_orig = ['gum-interview_orig', 'swbd_orig']
    social_cloned = ['gimpbel_cloned', 'nps_chat_cloned']
    social_orig = ['gimpbel_orig', 'nps_chat_orig']
    formal_cloned = ['gum-news_cloned', 'gum-voyage_cloned', 'brown_tei_cloned', 'gum-howto_cloned']
    formal_orig = ['gum-news_orig', 'gum-voyage_orig', 'brown_tei_orig', 'gum-howto_orig']
    print('\n\nspoken_cloned\n\n')
    calc_score(spoken_cloned, taggers)
    print('\n\nspoken_original\n\n')
    calc_score(spoken_orig, taggers)
    print('\n\nsocial_cloned\n\n')
    calc_score(social_cloned, taggers)
    print('\n\nsocial_original\n\n')
    calc_score(social_orig, taggers)
    print('\n\nformal_cloned\n\n')
    calc_score(formal_cloned, taggers)
    print('\n\nformal_original\n\n')
    calc_score(formal_orig, taggers)
    formal_cloned_f1 = generate_score(formal_cloned, taggers)
    #generate_box_plot(formal_cloned_f1)




if __name__ == '__main__':
    main()


