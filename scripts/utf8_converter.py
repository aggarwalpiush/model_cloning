# !usr/bin/env python
# -*- coding : utf-8 -*-

import codecs
import sys

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    count = 0
    with codecs.open(output_file, 'w', 'ascii', errors='ignore') as output_obj:
        with codecs.open(input_file, 'r', 'utf-8') as input_obj:
            for line in input_obj:
                count += 1
                tokens = line.split('\t')[1].split(' ')
                new_token = []
                for tok in tokens:
                    tok = tok.encode('utf-8').decode('ascii', 'ignore')
                    if tok == '':
                        continue
                    new_token.append(tok)
                output_obj.write(' '.join(new_token))

if __name__ == '__main__':
    main()