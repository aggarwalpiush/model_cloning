#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs
import os
import subprocess



CMD_DIR = '/home/LTLab.lan/paggarwal/model_clone/tree_tagger/cmd'
DATA_DIR = '/home/LTLab.lan/paggarwal/model_clone/data/leibzig_wiki/deu_wikipedia_2016_1M'
FILE_NAME = 'leibzig_wiki_data_1M.txt'



def get_lemma(input_line):
    ps = subprocess.Popen(('echo', input_line), stdout=subprocess.PIPE)
    output = subprocess.check_output((os.path.join(CMD_DIR, 'tagger-chunker-german')), stdin=ps.stdout)
    ps.wait()
    in_str = []
    out_str = []
    output = str(output, encoding='utf-8').split('\n')
    for o in output:
        o = o.split('\t')
        if len(o) == 3:
            in_str.append(o[0])
            out_str.append(o[-1])
    return ' '.join(out_str) + '\t' + ' '.join(in_str) + '\n'



def get_lemma_from_file(input_file):
    with codecs.open(input_file+'.tmp', 'r', 'utf-8') as outfile_obj:
        with codecs.open(input_file, 'r', 'utf-8') as infile_obj:
            for line in infile_obj:
                outfile_obj.write(line)
                outfile_obj.write('abrakadabra\n')
    ps = subprocess.Popen(('echo', input_line), stdout=subprocess.PIPE)
    output = subprocess.check_output((os.path.join(CMD_DIR, 'tagger-chunker-german')), stdin=ps.stdout)
    ps.wait()
    in_str = []
    out_str = []
    output = str(output, encoding='utf-8').split('\n')
    for o in output:
        o = o.split('\t')
        if len(o) == 3:
            in_str.append(o[0])
            out_str.append(o[-1])
    return ' '.join(out_str) + '\t' + ' '.join(in_str) + '\n'


def main():
    with codecs.open(os.path.join(DATA_DIR, FILE_NAME+ '.out'), 'w', 'utf-8') as outfile:
        with codecs.open(os.path.join(DATA_DIR, FILE_NAME), 'r', 'utf-8') as infile:
            for line in infile:
                outfile.write(get_lemma(line.encode("utf-8")))


if __name__ == '__main__':
    main()
