import seaborn as sns
import os
import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def coloring(x, **kws):
    ax = plt.gca()
    ax.annotate(x.name, xy=(0.05, 0.9), xycoords=ax.transAxes)
    if x > 0.0:
       col = "g"
    elif x < 0.0:
       col= 'r'

    sns.barplot(x, orient="h", color=col)
    return x


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

def tagger_abbrev_apper(tagger):
    if 'mayo' in tagger.lower().strip():
        return 'ma'
    if 'maxent' in tagger.lower().strip():
        return 'mx'
    if 'wsj' in tagger.lower().strip():
        return 'st3'
    if 'tagger_caseless' in tagger.lower().strip():
        return 'st1'
    if 'fast' in tagger.lower().strip():
        return 'st2'
    if 'perceptron' in tagger.lower().strip():
        return 'pp'
    if 'ontonote' in tagger.lower().strip():
        return 'on'
    if 'hepple' in tagger.lower().strip():
        return 'hp'
    if 'mate' in tagger.lower().strip():
        return 'mt'
for tagger in set(taggers):
    print(tagger)
    sprint = {}
    sprint['entity'] = ['ADP',
                        'ADV',
                        'CONJ',
                        'NOUN',
                        'PUNCT',
                        'ADJ',
                        'INTJ',
                        'PART',
                        'DET',
                        'NUM',
                        'X',
                        'PRON',
                        'VERB']
    my_value = []
    for key, value in report_entries.items():
        if tagger in key:
            if 'brown_tei' in key or 'news' in key or 'howto' in key or 'voyage' in key:
                my_value.append(value)
                print(value)
            else:
                continue
    my_value = [x[:-3] for x in my_value]
    print(my_value)
    sprint[tagger_abbrev_apper(tagger)] = np.mean(my_value, axis=0)
    df = pd.DataFrame.from_dict(sprint)
    print(df.head(5))

    color= list(np.where(df[tagger_abbrev_apper(tagger)] < 0, 'red', 'green'))
    g = sns.PairGrid(df, x_vars=df.columns[1], y_vars=["entity"],
                     height=5, aspect=.55 )
    print(color)
    g.map(sns.barplot, orient="h", palette=color)
    #g.map_diag(coloring)
    #g.map(sns.barplot, size=10, orient="h",
     #      linewidth=1, edgecolor="w", palette="ch:2.5,-.2,dark=.3") # palette="ch:s=1,r=-.1,h=1_r"
    g.set(xlim=(-1, 1), xlabel="Orig - Clone", ylabel="")
    titles = list(sprint.keys())[1:]
    for ax, title in zip(g.axes.flat, titles):
        # Set a different title for each axes
        ax.set(title=title)

        # Make the grid horizontal instead of vertical
        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
    sns.despine(left=True, bottom=True)
    plt.savefig(os.path.join(vis_report_path, tagger + 'pertagger.png'), dpi=200)



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
