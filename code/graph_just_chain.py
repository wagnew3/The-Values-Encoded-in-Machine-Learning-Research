import csv
import numpy as np
import matplotlib.pyplot as plt


with open('../data/Assignments - Sheet1_new.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
u=0

annotations_start_row=4
just_chain_scores=[]
just_chain_counts=np.zeros(5)
num_annotations=0

for annotation_row in range(annotations_start_row, 304, 3):
    if data[annotation_row+1][10]!="":
        just_chain_scores.append(int(data[annotation_row+1][10]))
        just_chain_counts[int(data[annotation_row+1][10])]+=1
    else:
        try:
            just_chain_scores.append(int(data[annotation_row][10]))
            just_chain_counts[int(data[annotation_row][10])]+=1
        except:
            u=0

just_chain_scores=np.array(just_chain_scores)
heights = just_chain_counts
bars = np.arange(5)
y_pos = np.arange(0, len(bars))
# plt.ylim(0,90)
# plt.xlim(-0.5, len(bars)-0.5)

plt.bar(y_pos, heights, color='#3a6692')
plt.legend()

# Rotation of the bars names
plt.xticks(y_pos, bars, rotation=0)  
plt.ylabel('number papers')
plt.xlabel('justificatory chain rating')
plt.show()