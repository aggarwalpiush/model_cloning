import seaborn as sns
import os
import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#sns.axes_style()
#sns.set_style("darkgrid", {"grid.color": ".9"})
sns.set(style="whitegrid")

# Load the dataset
crashes = sns.load_dataset("car_crashes")
print(type(crashes))
print(crashes.head(5))

# Load report data

report_path = '/Users/paggarwal/github_repos/model_cloning/data/report_structured'
vis_report_path = '/Users/paggarwal/github_repos/model_cloning/data/report_visualization'

files = []
dirs = []
# r=root, d=directories, f = files
for r, d, f in os.walk(report_path):
    for file in f:
        if '.rpt' in file:
            files.append(os.path.join(r, file))
report_entries = {}

for file in files:
    if 'orig.rpt' in file:
        orig_rpt = []
        cloned_rpt = []
        with codecs.open(file, 'r', 'utf-8') as file_obj:
            for i, line in enumerate(file_obj):
                if i == 0:
                    continue
                if line.strip().replace('\n', '') != '':
                    orig_rpt.append(float(''.join(line[39:44])))
                    # if 'ClearNlpPosTagger_ontonotes_gum-howto' in file:
                    #     print(line[39:44])
                    #     print(''.join(line[39:44]))
                    #     print(float(''.join(line[39:44])))
        with codecs.open(file.replace('orig.rpt', 'cloned.rpt'), 'r', 'utf-8') as file_obj:
            for i, line in enumerate(file_obj):
                if i == 0:
                    continue
                if line.strip().replace('\n', '') != '':
                    cloned_rpt.append(float(''.join(line[39:44])))
                    # if 'ClearNlpPosTagger_ontonotes_gum-howto' in file:
                    #     print(line[40:44])
                    #     print(''.join(line[40:44]))
                    #     print(float(''.join(line[40:44])))
        report_entries['_'.join(os.path.basename(file).split('_')[:-1])] = np.array(orig_rpt) - np.array(cloned_rpt)

taggers = []
for key, value in report_entries.items():
    taggers.append('_'.join(key.replace('brown_tei', 'brown-tei').replace('nps_chat', 'nps-chat').split('_')[:-1]))

print(taggers)

cloned_time_path = '/Users/paggarwal/github_repos/model_cloning/data/time_diff/clone_rates.tsv'
original_time_path='/Users/paggarwal/github_repos/model_cloning/data/time_diff/original_rates.tsv'

taggers = ['ClearNlpPosTagger', 'StanfordPosTagger', 'HepplePosTagger', 'OpenNlpPosTagger', 'MatePosTagger']
variants = {'StanfordPosTagger': ['wsj-0-18-caseless-left3words-distsim', 'caseless-left3words-distsim', 'fast.41'],
            'ClearNlpPosTagger': ['mayo', 'ontonotes'],
            'HepplePosTagger': ['novariant'],
            'OpenNlpPosTagger': ['perceptron', 'maxent'],
            'MatePosTagger': ['conll2009']}

report_entries_clone = {}
report_entries_orig = {}

with codecs.open(cloned_time_path, 'r', 'utf-8') as cl_obj:
    for line in cl_obj:
        report_entries_clone[line.split('\t')[0].replace('brown_tei', 'brown-tei').replace('nps_chat', 'nps-chat')] = line.split('\t')[0].strip().rstrip().replace('\r\n','')

with codecs.open(original_time_path, 'r', 'utf-8') as cl_obj:
    for line in cl_obj:
        report_entries_orig[line.split('\t')[0].replace('brown_tei', 'brown-tei').replace('nps_chat', 'nps-chat')] = line.split('\t')[0].strip().rstrip().replace('\r\n','')









for tagger in set(taggers):
    print(tagger)
    sprint = {}
    sprint['entity'] = ['brown',
                        'gimpbel',
                        'howto',
                        'interview',
                        'news',
                        'voyage',
                        'nps',
                        'swbd',]
    for key, value in report_entries.items():
        if tagger in key:
            sprint[key.replace('brown_tei', 'brown-tei').replace('nps_chat', 'nps-chat').split('_')[-1]] = value
    df = pd.DataFrame.from_dict(sprint)
    print(df.head(5))
    g = sns.PairGrid(df, x_vars=df.columns[1:], y_vars=["entity"],
                     height=5, aspect=.55)
    g.map(sns.stripplot, size=10, orient="h",
           linewidth=1, edgecolor="w") # palette="ch:s=1,r=-.1,h=1_r"
    g.set(xlim=(-1, 1), xlabel="difference", ylabel="")
    titles = list(sprint.keys())[1:]
    for ax, title in zip(g.axes.flat, titles):
        # Set a different title for each axes
        ax.set(title=title)

        # Make the grid horizontal instead of vertical
        ax.xaxis.grid(False)
        ax.yaxis.grid(True)
    sns.despine(left=True, bottom=True)
    plt.savefig(os.path.join(vis_report_path, tagger + '.png'), dpi=200)



# Make the PairGrid
# g = sns.PairGrid(crashes.sort_values("total", ascending=False),
#                  x_vars=crashes.columns[:-3], y_vars=["entity"],
#                  height=10, aspect=.25)
#
# # Draw a dot plot using the stripplot function
# g.map(sns.stripplot, size=10, orient="h",
#       palette="ch:s=1,r=-.1,h=1_r", linewidth=1, edgecolor="w")
#
# # Use the same x axis limits on all columns and add better labels
# g.set(xlim=(0, 25), xlabel="Crashes", ylabel="")
#
# # Use semantically meaningful titles for the columns
# titles = ["Total crashes", "Speeding crashes", "Alcohol crashes",
#           "Not distracted crashes", "No previous crashes"]
#
# for ax, title in zip(g.axes.flat, titles):
#     # Set a different title for each axes
#     ax.set(title=title)
#
#     # Make the grid horizontal instead of vertical
#     ax.xaxis.grid(False)
#     ax.yaxis.grid(True)
#
# sns.despine(left=True, bottom=True)
# import matplotlib.pyplot as plt
#
# plt.show()
