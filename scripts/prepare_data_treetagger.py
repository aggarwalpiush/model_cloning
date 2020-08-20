#! usr/bin/env python
# -*- coding : utf-8 -*-

import codecs

END_LINE_INDICATOR = 'abrakadabra'

def generate_train_files(input_file):
    with codecs.open(input_file+'.train.src', 'w', 'utf-8') as src_out_obj:
        with codecs.open(input_file + '.train.dst', 'w', 'utf-8') as dst_out_obj:
            with codecs.open(input_file, 'r', 'utf-8') as in_data_obj:
                src_word = []
                tgt_lemma = []
                for line in in_data_obj:
                    tokens = line.split('\t')
                    if tokens[0] == END_LINE_INDICATOR:
                        src_out_obj.write(' '.join(src_word) + '\n')
                        dst_out_obj.write(' '.join(tgt_lemma) + '\n')
                        src_word = []
                        tgt_lemma = []
                    elif len(tokens) == 3:
                        src_word.append(tokens[0])
                        tgt_lemma.append(tokens[-1])


def generate_test_files_conll(input_file):
    with codecs.open(input_file + '.src', 'w', 'utf-8') as src_out_obj:
        with codecs.open(input_file + '.dst', 'w', 'utf-8') as dst_out_obj:
            with codecs.open(input_file, 'r', 'utf-8') as in_data_obj:
                src_word = []
                tgt_lemma = []
                for line in in_data_obj:
                    tokens = line.split('\t')
                    if len(tokens) == 0:
                        src_out_obj.write(' '.join(src_word) + '\n')
                        dst_out_obj.write(' '.join(tgt_lemma) + '\n')
                        src_word = []
                        tgt_lemma = []
                    else:
                        src_word.append(tokens[1])
                        tgt_lemma.append(tokens[2])



def main():
    train_file_name = ''
    test_file_name = ''
    generate_train_files(train_file_name)
    generate_test_files_conll(test_file_name)


if __name__ == '__main__':
    main()


