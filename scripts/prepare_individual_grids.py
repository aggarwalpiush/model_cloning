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


sprint = {}
sprint['entity'] = ['mayo', 'ontnts', 'hepple', 'mate', 'maxent', 'prcptrn', 'csls', 'wsj', 'fast']
sprint['formal'] = [0.0275,0.0275,0.025,0.025,0.02,0.0225,0.0225,0.025,0.03]
sprint['social'] = [0.08, 0.105,0.025,0.035,0.03,0.04,0.095,0.055,0.13]
sprint['spoken'] = [0.035,0.055,0.045,0.055,0.06,0.06,0.055,0.055,0.055]
df = pd.DataFrame.from_dict(sprint)
print(df.head(5))
g = sns.PairGrid(df, x_vars=df.columns[1:], y_vars=["entity"],
                 height=5, aspect=.55, )

g.map(sns.barplot, orient="h", color='green')
#g.map_diag(coloring)
#g.map(sns.barplot, size=10, orient="h",
 #      linewidth=1, edgecolor="w", palette="ch:2.5,-.2,dark=.3") # palette="ch:s=1,r=-.1,h=1_r"
g.set(xlim=(0, 0.15), xlabel="Original - Cloned(F1)", ylabel="")
titles = list(sprint.keys())[1:]
for ax, title in zip(g.axes.flat, titles):
    # Set a different title for each axes
    ax.set(title=title)

    # Make the grid horizontal instead of vertical
    ax.xaxis.grid(True)
    ax.yaxis.grid(False)
sns.despine(left=True, bottom=True)
plt.savefig(os.path.join('performance.png'), dpi=400)


