import pandas as pd
import os
import xlrd
from openpyxl import load_workbook
import pickle
import math
import xlsxwriter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
np.random.seed(0)

def autolabel(rects, label):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = 0
        ax.annotate(label,
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset pixels",
                    ha='center', va='bottom', rotation=0, position=(0,-37), fontsize=9)
        
with open('/home/willie/workspace/Values_Of_ML/data/paper_affiliations.tsv', newline='') as f:
    reader=csv.reader(f, delimiter="\t")
    data=list(reader)

past_affils=np.zeros(8)
total_past=0
current_affils=np.zeros(8)
total_current=0
for data_row in data[1:]:
    year=data_row[1]
    if year=='2008' or year=='2009':
        a=np.array(data_row[2:-1]).astype(np.float64)
        past_affils+=np.array(data_row[2:-1]).astype(np.float64)
        total_past+=1
    else:
        current_affils+=np.array(data_row[2:-1]).astype(np.float64)
        total_current+=1

total_past+=5
# past_affils[0]+=1
# past_affils[1]+=1
past_affils[0]+=4 #uni
past_affils[1]+=2 #elite uni
past_affils[3]+=2 #non-na uni
past_affils=100*past_affils/total_past
current_affils=100*current_affils/total_current

# dallas_affil_data=np.array(data)
# dallas_affil_data=dallas_affil_data[1:, 2:-1].astype(np.float64)
# dallas_affil_data=np.sum(dallas_affil_data, axis=1)

affiliations_sheet="/home/willie/workspace/Values_Of_ML/data/Corporate Ties.xlsx"

sheets=[]
  
annotations=pd.ExcelFile(affiliations_sheet)
for sheet_name in annotations.sheet_names:
    print('sheet_name', sheet_name)
    sheet=annotations.parse(sheet_name)
    sheets.append(sheet._values)
            
pickle.dump(sheets, open('/home/willie/workspace/Values_Of_ML/data/loaded_affiliations_sheets.p', 'wb'))

sheets=pickle.load(open('/home/willie/workspace/Values_Of_ML/data/loaded_affiliations_sheets.p', 'rb'))
u=0


labels = [sheets[1][i][0][7:] for i in range(22)]
num_affils=sheets[1][0:22,1]
order=np.argsort(-num_affils)
num_affils=num_affils[order]
labels=[labels[order[i]] for i in range(len(labels))]


# x = np.arange(len(labels))  # the label locations
# width = 0.9  # the width of the bars
# 
# fig, ax = plt.subplots()
# rects1 = ax.bar(x, num_affils, width)
# 
# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Number of Papers')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#          rotation_mode="anchor")
# fig.tight_layout()
# plt.show()
 
funding_sheet=sheets[2]
orgs_sheet=sheets[3]
type_list=["TECH COMPANY", "BIG TECH", "MILITARY", "NONPROFIT FUNDER", "RESEARCH INSTITUTE", "AGENCIES"]
funders_map={}
for row_ind in range(126):
    funders_map[orgs_sheet[row_ind][0]]=[]
    for col_ind in range(1,7):
        if isinstance(orgs_sheet[row_ind][col_ind], str):
            funders_map[orgs_sheet[row_ind][0]].append(col_ind-1)

funders_list=list(funders_map.keys())
funders_counts=np.zeros((2, len(funders_list)))
corp_big_tech_affils=np.zeros((2,3))
      
ties_counts=np.zeros((2, 6))
total_per_year=np.zeros((2))
for row_ind in range(6,101):
    year=funding_sheet[row_ind][0]
    if year==2008 or year==2009:
        year_ind=0
    else:
        year_ind=1
        
    for col_ind in range(13,33):
        if funding_sheet[row_ind][col_ind]==1:
            org=funding_sheet[101][col_ind][7:]
            if 0 in funders_map[org] and not (1 in funders_map[org]):
                corp_big_tech_affils[year_ind, 0]+=1
            if 1 in funders_map[org]:
                corp_big_tech_affils[year_ind, 1]+=1
#             if not (0 in funders_map[org]):
#                 corp_big_tech_affils[year_ind, 2]+=1
    
    affil_vec=np.zeros(6)
    for col_ind in range(13,139):
        if funding_sheet[row_ind][col_ind]==1:
            if col_ind>=33:
                org=funding_sheet[101][col_ind][9:]
            else:
                org=funding_sheet[101][col_ind][7:]
            
            if year==2008 or year==2009:
                funders_counts[0, funders_list.index(org)]+=1
            else:
                funders_counts[1, funders_list.index(org)]+=1
            
            types=funders_map[org]
            for org_type in types:
                affil_vec[org_type]=1
            
#                 if year==2008 or year==2009:
#                     ties_counts[0][type]+=1
#                 else:
#                     ties_counts[1][type]+=1
    if year==2008 or year==2009:
        total_per_year[0]+=1
        ties_counts[0]+=affil_vec
    else:
        total_per_year[1]+=1
        ties_counts[1]+=affil_vec

total_per_year[0]+=5
total_per_year[1]+=0
ties_counts[0]+=np.array([1,1,0,0,0,4])
ties_counts[1]+=np.array([0,0,0,0,0,0])
corp_big_tech_affils[0,0]+=1


ties_counts=ties_counts/total_per_year[:,None]


#ties bar chart
srt_ord=np.argsort(-np.sum(funders_counts, axis=0))
funders_counts=funders_counts[:, srt_ord]
funders_list=[funders_list[srt_ord[i]] for i in range(len(funders_list))]

big_tech_labels=[]
big_tech_amts=[]
for funder in funders_list:
    if 1 in funders_map[funder]:
        big_tech_labels.append(funder)
        big_tech_amts.append(funders_counts[:,funders_list.index(funder)])

big_tech_amts[8]+=big_tech_amts[9]
big_tech_amts[11]+=big_tech_amts[13]

big_tech_amts.pop(13)
big_tech_amts.pop(9)

big_tech_labels.pop(13)
big_tech_labels.pop(9)

big_tech_labels=[big_tech_labels[i].title() for i in range(len(big_tech_labels))]
big_tech_labels[-2]="MIT-IBM Watson"

big_tech_amts=np.array(big_tech_amts).transpose()

ties_counts=ties_counts*100
type_list=["Tech\nCompany", "Big\nTech", "Military", "Nonprofit", "Research\nInstitute", "Agencies", "University", "Elite\nUniversity", "Non-N.A.\nUniversity"]
x = np.array([0,1,2,3,4,5,6,7,8])*0.8  # the label locations
width = 0.35  # the width of the bars
 
fig, ax = plt.subplots()
rects1 = ax.bar(x[2:6]-width/2, ties_counts[0,2:], width, color='#E1DAAE')
rects2 = ax.bar(x[2:6]+width/2, ties_counts[1,2:], width, color='#FF934F')
autolabel(rects1, "'08-'09")
autolabel(rects2, "'18-'19")

#colors=["#9F0162", "#009F81", "#FF5AAF", "#00FCCF", "#8400CD", "#008DF9", "#00C2F9", "#FFB2FD", "#A40122", "#E20134", "#FF6E3A", "#FFC33B"]
colors=["#CC2D35", "#058ED9", "#848FA2", "#2D3142", "#FFC857"]

for bt in big_tech_labels[:5]:
    rects1 = ax.bar(x[1]-width/2, big_tech_amts[0,big_tech_labels.index(bt)], width, bottom=np.sum(big_tech_amts[0,:big_tech_labels.index(bt)]), label=bt, color=colors[big_tech_labels.index(bt)])
    rects2 = ax.bar(x[1]+width/2, big_tech_amts[1,big_tech_labels.index(bt)], width, bottom=np.sum(big_tech_amts[1,:big_tech_labels.index(bt)]), color=colors[big_tech_labels.index(bt)])

autolabel(rects1, "'08-'09")
autolabel(rects2, "'18-'19")

rects1 = ax.bar(x[1]-width/2, np.sum(big_tech_amts[0,5:]), width, bottom=np.sum(big_tech_amts[0,:5]), color='#E1DAAE')
rects2 = ax.bar(x[1]+width/2, np.sum(big_tech_amts[1,5:]), width, bottom=np.sum(big_tech_amts[1,:5]), color='#FF934F')
 
rects1 = ax.bar(x[0]-width/2, ties_counts[0,0], width, color='#E1DAAE')
rects2 = ax.bar(x[0]+width/2, ties_counts[1,0], width, color='#FF934F')
autolabel(rects1, "'08-'09")
autolabel(rects2, "'18-'19")

rects1 = ax.bar(x[6:]-width/2, [past_affils[0], past_affils[1], past_affils[3]], width, color='#E1DAAE')
rects2 = ax.bar(x[6:]+width/2, [current_affils[0], current_affils[1], current_affils[3]], width, color='#FF934F')
autolabel(rects1, "'08-'09")
autolabel(rects2, "'18-'19")
plt.xlim([-width, x[-1]+width])
 
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Percent of Papers', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(type_list)
ax.set_ylim(0,100)
plt.setp(ax.get_xticklabels(), rotation=0, ha="center", rotation_mode="anchor", position=(0,-0.05), fontsize=12)


 
autolabel(rects1, "'08-'09")
autolabel(rects2, "'18-'19")

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], fontsize=12, loc="upper center", bbox_to_anchor=(0.3, 1))

#plt.legend()

#fig.tight_layout()
plt.show()
print(ties_counts)

#corp affils
corp_big_tech_affils[:,2]=total_per_year-(corp_big_tech_affils[:,0]+corp_big_tech_affils[:,1])
save=np.copy(corp_big_tech_affils[:,1])
corp_big_tech_affils[:,1]=corp_big_tech_affils[:,0]
corp_big_tech_affils[:,0]=save


colors=["#fa6825", "#b3cde3", "#edf8fb"]
#2008-2009
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.pie(corp_big_tech_affils[0]/total_per_year[0], labels=['Big Tech\nAffiliation', 'Other Corporate\nAffiliation', 'No Corporate\nAffiliation'],
         labeldistance=None, autopct='%1.0f%%', shadow=False, startangle=90, colors=colors)
ax1.axis('equal') 
ax1.set_xlabel("'08-'09")
#plt.show()

#2018-2019
ax2.pie(corp_big_tech_affils[1]/total_per_year[1], labeldistance=None, autopct='%1.0f%%', shadow=False, startangle=90, colors=colors)
ax2.axis('equal')
ax2.set_xlabel("'18-'19")

fig.legend(loc="center")

plt.show()
u=0


            
            
            
            
            
            
            
            
            
            
            
            
            
    
