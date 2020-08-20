#! usr/bin/env python
# -*- coding : utf-8  -*-

import codecs
import glob
import os
import numpy as np


def generate_report(performance_object, output_path):
	column = performance_object[0].keys()
	with codecs.open(output_path, 'w', 'utf-8') as out_obj:
		out_obj.write('%s\n' %('	'.join(column)))
		for each_result in performance_object:
			row = []
			for key in column:
				row.append(each_result[key]) 
			out_obj.write('%s\n' %('	'.join(row)))





def main():	
	performance = []
	for result_file in glob.glob('/Users/paggarwal/github_repos/model_cloning/results/org.dkpro.lab*/repository/RunTaggerTask*/tagger.txt'):
		results = {}
		# get tagger
		with codecs.open(result_file, 'r', 'utf-8') as tag_obj:
			results['tagger'] = ''
			for line in tag_obj:
				if '#' not in line:
					line_fields = line.split('=')
					results['tagger'] += '_'+line_fields[-1].strip().rstrip('\r\n').replace('\n', '')


		# get token count
		with codecs.open(os.path.join(os.path.dirname(result_file), 'tokenCount.txt'), 'r', 'utf-8') as tc_obj:
			for line in tc_obj:
				if '#' not in line:
					line_fields = line.split('=')
					if line_fields[0].strip().lower() == 'tokencount':
						results['tokencount'] = str(int(line_fields[-1].strip().rstrip('\r\n').replace('\n', '')))


		# get normalizedTokenTime
		with codecs.open(os.path.join(os.path.dirname(result_file), 'normalizedTokenTime.txt'), 'r', 'utf-8') as ntt_obj:
			for line in ntt_obj:
				if '#' not in line:
					line_fields = line.split('=')
					if line_fields[0].strip().lower() == 'milliontokenpersecond':
						results['millionTokenPerSecond'] = str(float(line_fields[-1].strip().rstrip('\r\n').replace('\n', '')))

		# get corpus
		with codecs.open(os.path.join(os.path.dirname(result_file), 'corpus.txt'), 'r', 'utf-8') as crps_obj:
			results['corpus'] = ''
			for line in crps_obj:
				if '#' not in line:
					line_fields = line.split('=')
					results['corpus'] += '_'+line_fields[-1].strip().rstrip('\r\n').replace('\n', '')

		# get time mean, sum and standard deviation
		with codecs.open(os.path.join(os.path.dirname(result_file), 'time.txt'), 'r', 'utf-8') as tm_obj:
			for line in tm_obj:
				if '#' not in line:
					line_fields = line.split('=')
					if line_fields[0].strip().lower() == 'mean':
						results['time_mean'] = str(float(line_fields[-1].strip().rstrip('\r\n').replace('\n', '')))
					if line_fields[0].strip().lower() == 'sum':
						results['time_sum'] = str(float(line_fields[-1].strip().rstrip('\r\n').replace('\n', '')))
					if line_fields[0].strip().lower() == 'stddev':
						results['time_stddev'] = str(float(line_fields[-1].strip().rstrip('\r\n').replace('\n', '')))

		# get fine accuracy
		with codecs.open(os.path.join(os.path.dirname(result_file), 'accFine.txt'), 'r', 'utf-8') as acf_obj:
			for line in acf_obj:
				if '#' not in line:
					line_fields = line.split('=')
					if line_fields[0].strip().lower() == 'accfine':
						results['accFine'] = str(float(line_fields[-1].strip().rstrip('\r\n').replace('\n', '')))

		# get coarse accuracy
		with codecs.open(os.path.join(os.path.dirname(result_file), 'accCoarse.txt'), 'r', 'utf-8') as accrse_obj:
			for line in accrse_obj:
				if '#' not in line:
					line_fields = line.split('=')
					if line_fields[0].strip().lower() == 'acccoarse':
						results['accCoarse'] = str(float(line_fields[-1].strip().rstrip('\r\n').replace('\n', '')))

		# get fine macro f1
		with codecs.open(os.path.join(os.path.dirname(result_file), 'fineTagResults.txt'), 'r', 'utf-8') as finef1_obj:
			f1_tags = []
			for i, line in enumerate(finef1_obj):
				if not i == 0:
					line_fields = line.split('\t')
					if str(line_fields[3]).strip().lower() == 'nan':
						f1_tags.append(0.0)
					else:
						f1_tags.append(float(line_fields[3]))
						results['finef1_mac'] = str(np.average(np.array(f1_tags)))


		with codecs.open(os.path.join(os.path.dirname(result_file), 'coarseTagResults.txt'), 'r', 'utf-8') as coarsef1_obj:
			f1_tags = []
			for i, line in enumerate(coarsef1_obj):
				if not i == 0:
					line_fields = line.split('\t')
					if str(line_fields[3]).strip().lower() == 'nan':
						f1_tags.append(0.0)
					else:
						f1_tags.append(float(line_fields[3]))
						results['coarsef1_mac'] = str(np.average(np.array(f1_tags)))
		performance.append(results)

	generate_report(performance, '/Users/paggarwal/github_repos/model_cloning/results/commonly_used_pos_results.tsv')




if __name__ == '__main__':
	main()
