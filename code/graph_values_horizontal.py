import csv
import numpy as np
import matplotlib.pyplot as plt
import numpy as np, scipy.stats as st
from scipy.stats import t
import math

with open('../data/Assignments - Sheet1.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
u=0

annotations_start_row=4
values_start_col=12
values_end_col=94
value_names=data[2][values_start_col:values_end_col+1]
value_counts=np.zeros(values_end_col+1-values_start_col)
num_annotations=0

def calc_ci(data):
    mean=np.mean(data)
    stddev = np.std(data, ddof=1)
    t_bounds = t.interval(0.9, len(data) - 1)
    ci = [mean + critval * stddev / math.sqrt(len(data)) for critval in t_bounds]
    return ci

def conv_to_int(s):
    if not s:
        return 0
    else:
        return int(s)
    
def add_grouped_value_counts(row_counts, groups):
    for group in groups:
        val_sum=0
        for val_ind in groups[group]:
            val_sum+=row_counts[val_ind]
        row_counts.append(val_sum>0)
    return row_counts

def remove_group_vals(labels, counts, value_names, group):
    removed_labels=[labels[i] for i in reversed(group)]
    removed_counts=[counts[i] for i in reversed(group)]
    removed_value_names=[value_names[i] for i in reversed(group)]
    sort_inds=np.argsort(np.array(removed_counts))
    removed_labels=[removed_labels[sort_inds[i]] for i in range(len(removed_labels))]
    removed_counts=[removed_counts[sort_inds[i]] for i in range(len(removed_counts))]
    removed_value_names=[removed_value_names[sort_inds[i]] for i in range(len(removed_value_names))]
    return [3 for i in range(len(removed_labels))], removed_counts, removed_value_names
    
groups={'Generalization Values': [2, 3, 26], 'Performance Values': [24,25,27], 'Efficiency Values': [14,28,29,30,31,32,33,75], "Building on Past Work": [36,37]}

value_eff_and_fr=0

for annotation_row in range(annotations_start_row, 304, 3):
#     if data[annotation_row+1][values_start_col]!="":
#         row_value_counts=[conv_to_int(s)>0 for s in data[annotation_row+1][values_start_col:values_end_col+1]]
#         row_value_counts=add_grouped_value_counts(row_value_counts, groups)
#         value_counts+=np.array(row_value_counts)
#         num_annotations+=1
#     elif data[annotation_row][values_start_col]!="":
    counts_list=[]
    for s in data[annotation_row][values_start_col:values_end_col+1]:
        if s=='':
            counts_list.append(0)
        else:
            counts_list.append(conv_to_int(s)>0)
    #counts_list=add_grouped_value_counts(counts_list, groups)
    value_counts+=np.array(counts_list)
    
    ev=0
    for i in [14,28,29,30,31,32,33,75]:
        if counts_list[i]>0:
            ev=1
    if ev and counts_list[47]:
        value_eff_and_fr+=1
    
    num_annotations+=1



#value_names+=list(groups.keys())
heights = value_counts
bars = value_names
bars[9]="Quantitative evidence"
bars[10]="Qualitative evidence"
bars[32]="Label efficiency"
bars[38]="Unifying Ideas"
# 

bars=bars[:71]
heights=heights[:71]

labels=np.zeros(len(bars))
labels[55:64]=1
labels[64:71]=2

# group_keys=list(groups.keys())
# 
# removed=[remove_group_vals(labels, heights, value_names, groups[group]) for group in group_keys]
# all_removed_inds=[]
# for group in groups:
#     all_removed_inds+=groups[group]
#     
# new_heights=[]
# new_labels=[]
# new_bars=[]
# for ind in range(len(labels)):
#     if not ind in all_removed_inds:
#         new_heights.append(heights[ind])
#         new_labels.append(labels[ind])
#         new_bars.append(bars[ind])
# 
# heights=np.array(new_heights)
# labels=new_labels
# bars=new_bars



sorted=np.argsort(-heights)
heights=heights[sorted]
labels=[labels[sorted[i]] for i in range(len(labels))]
bars=[bars[sorted[i]] for i in range(len(bars))]

cis=[]
for height in heights:
    value_trues=np.zeros(100)
    value_trues[:int(height)]=1
    ci=calc_ci(value_trues)
    cis.append(ci)
    print(height, ci)
cis=np.array(cis)
cis=(cis[:,1]-cis[:,0])/2
cis=cis*100

heights=np.ndarray.tolist(heights)

# for group_ind in range(len(group_keys)):
#     insert_ind=bars.index(group_keys[group_ind])
#     labels[insert_ind:insert_ind]=removed[group_ind][0]
#     heights[insert_ind:insert_ind]=removed[group_ind][1]
#     bars[insert_ind:insert_ind]=removed[group_ind][2]
    
#     labels.insert(insert_ind, removed[group_ind][0])
#     heights.insert(insert_ind, removed[group_ind][1])
#     bars.insert(insert_ind, removed[group_ind][2])



# plt.bar(11.5, 350, width=24, color='#e6e6e6', label='General')
# plt.bar(29.5, 350, width=12, color='#f3d8e7', label='Performance')
# plt.bar(39.5, 350, width=8, color='#d1f0fa', label='Advances in Understanding the Field')
# plt.bar(49, 350, width=11, color='#f4f0d7', label='Practical Application')
# plt.bar(59, 350, width=9, color='#d6f5db', label='User Rights')
# plt.bar(67, 350, width=7, color='#f9d2d6', label='Ethical Principles')

bars=[bars[i].title() for i in range(len(bars))]
bars[66]="Critiquability"
bars[63]="Respect for Law and Public Interest"
bars[29]="Facilitating Use"
bars[18]="Used in Practice/Popular"
#bars[51]="State-of-the-Art"

bars.pop(67)
labels=np.concatenate((labels[:67], labels[68:]))
heights=np.concatenate((heights[:67], heights[68:]))

#drop unused values
#bars=bars[:67-4]
#labels=labels[:67-4]
#heights=heights[:67-4]

plt.ylim(0,100)
plt.xlim(-0.5, len(bars)-0.5)

labels=np.array(labels)
heights=100*np.array(heights)/100.0
y_pos = np.arange(0, len(bars))
a=y_pos[np.argwhere(labels==0)]
plt.bar(y_pos[np.argwhere(labels==0)][:,0], heights[np.argwhere(labels==0)][:,0], yerr=cis[np.argwhere(labels==0)][:,0], ecolor='#333333', color='#1b9e77')
plt.bar(y_pos[np.argwhere(labels==1)][:,0], heights[np.argwhere(labels==1)][:,0], yerr=cis[np.argwhere(labels==1)][:,0], ecolor='#333333', color='#d95f02', label='User Rights')
plt.bar(y_pos[np.argwhere(labels==2)][:,0], heights[np.argwhere(labels==2)][:,0], yerr=cis[np.argwhere(labels==2)][:,0], ecolor='#333333', color='#7570b3', label='Ethical Principles')
plt.bar(y_pos[np.argwhere(labels==3)][:,0], heights[np.argwhere(labels==3)][:,0], yerr=cis[np.argwhere(labels==3)][:,0], ecolor='#333333', color='#B1CCC4')
plt.legend(loc='upper right')
plt.grid(True, axis='y')
plt.ylabel('% Papers with Value')
#plt.ylabel('Value')

colors=[]

# Rotation of the bars names
plt.xticks(y_pos, bars, rotation = -45, ha='left', rotation_mode="anchor", fontsize=11)#, color=colors)
ticks=plt.gca().get_xticklabels()
for label_ind in range(len(labels)):
    if labels[label_ind]==0:
        ticks[label_ind].set_color('#000000')
    elif labels[label_ind]==1:
        ticks[label_ind].set_color('#b14e02')
    elif labels[label_ind]==2:
        ticks[label_ind].set_color('#4b4686')
#plt.yticks(y_pos[np.argwhere(labels==1)][:,0], [bars[i] for i in np.argwhere(labels==1)[:,0]], color='#d95f02')
#plt.yticks(y_pos[np.argwhere(labels==2)][:,0], [bars[i] for i in np.argwhere(labels==2)[:,0]], backgroundcolor='#7570b3')
plt.show()
u=0
