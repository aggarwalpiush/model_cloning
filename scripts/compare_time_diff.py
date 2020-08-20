#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs


cloned_models_path='/Users/paggarwal/github_repos/model_cloning/data/time_diff/stats_cloned_models_2.txt'
original_models_path='/Users/paggarwal/github_repos/model_cloning/data/time_diff/stats_trivial_pos_taggers_rates.txt'


def parse_cloned_model(in_path):
    tokens = {}
    tokens['brown'] = 985385
    tokens['gimpbel'] = 30073
    tokens['howto'] = 12089
    tokens['interview'] = 11543
    tokens['news'] = 7594
    tokens['voyage'] = 7713
    tokens['nps'] = 32366
    tokens['swbd'] = 2470432
    model_rate=dict()
    with codecs.open(in_path, 'r', 'utf-8') as path_obj:
        object = []
        for line in path_obj:
            if 'Filename' in line:
                if len(object) > 0:
                    time_taken= float(object[4]) - float(object[3])
                    token_count = [v for k, v in tokens.items() if k in object[0]][0]
                    time_aken_per_million_token_insec = (time_taken   / int(token_count)) * 1000
                    model_rate[object[0].replace('_infer_latest.log', '')] = time_aken_per_million_token_insec
                    object = []
                    object.append(line.split(':')[1].strip().replace(' ',''))
                else:
                    object.append(line.split(':')[1].strip().replace(' ',''))
            else:
                object.append(line.split(':')[1].strip().replace(' ', ''))
        if len(object) > 0:
            time_taken = float(object[4]) - float(object[3])
            token_count = [v for k,v in tokens.items() if k in object[0]][0]
            time_taken_per_million_token_insec = (time_taken  / int(token_count)) * 1000
            model_rate[object[0].replace('_infer_latest.log', '')] = time_taken_per_million_token_insec
    return model_rate


def parse_original_models(in_path):
    tokens = {}
    tokens['brown'] = 1155738
    tokens['gimpbel'] = 32973
    tokens['howto'] = 12735
    tokens['interview'] = 12641
    tokens['news'] = 9391
    tokens['voyage'] = 9196
    tokens['nps'] = 31600
    tokens['swbd'] = 2142580
    model_load_time = {}
    model_load_time['ClearNlpPosTagger_mayo'] = 2.8382298476062715
    model_load_time['ClearNlpPosTagger_ontonotes'] = 3.8751833769492805
    model_load_time['StanfordPosTagger_wsj-0-18-caseless-left3words-distsim'] = 2.056268882006407
    model_load_time['StanfordPosTagger_caseless-left3words-distsim'] = 2.4100643200799823
    model_load_time['StanfordPosTagger_fast.41'] = 1.8439785279333591
    model_load_time['HepplePosTagger_novariant'] = 1.2142784083262086
    model_load_time['OpenNlpPosTagger_perceptron'] = 1.6463904585689306
    model_load_time['OpenNlpPosTagger_maxent'] = 1.7569659841246903
    model_load_time['MatePosTagger_conll2009'] = 14.472436117008328

    model_rate=dict()
    with codecs.open(in_path, 'r', 'utf-8') as path_obj:
        object = []
        for line in path_obj:
            if 'out_time' in line or 'Time' in line:
                if 'out_time' in line:
                    if len(object) > 0:
                        time_taken= float(object[1])
                        for key,value in tokens.items():
                            if key in object[0]:
                                token_count = value
                                break
                        for key,value in model_load_time.items():
                            if key in object[0]:
                                loading_time = float(value)
                                break
                        print(time_taken)
                        print(loading_time)
                        print(token_count)
                        time_aken_per_million_token_insec = ((time_taken - loading_time) / token_count) * 1000000
                        model_rate[object[0]] = time_aken_per_million_token_insec
                        object = []
                        object.append(line.split('.out')[-2].strip().replace(' ','').split(']')[-1])
                    else:
                        object.append(line.split('.out')[-2].strip().replace(' ', '').split(']')[-1])
                else:
                    if 'Time:' in line:
                        object.append(line.split(':')[1].strip().replace(' ', ''))
        if len(object) > 0:
            time_taken = float(object[1])
            for key, value in tokens.items():
                if key in object[0]:
                    token_count = value
                    break
            for key, value in model_load_time.items():
                if key in object[0]:
                    loading_time = float(value)
                    break
            time_aken_per_million_token_insec = ((time_taken - loading_time) / token_count) * 1000000
            model_rate[object[0]] = time_aken_per_million_token_insec
    return model_rate


def main():
    with codecs.open('/Users/paggarwal/github_repos/model_cloning/data/time_diff/clone_rates_2_with_load.tsv', 'w', 'utf-8') as outfile:
        for key,value in parse_cloned_model(cloned_models_path).items():
            outfile.write('%s\t%s\n'%(key,value))
    with codecs.open('/Users/paggarwal/github_repos/model_cloning/data/time_diff/original_rates_corrected_without_load.tsv', 'w', 'utf-8') as outfile:
        for key,value in parse_original_models(original_models_path).items():
            outfile.write('%s\t%s\n'%(key,value))


if __name__ == '__main__':
    main()
