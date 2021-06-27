import pandas as pd
import os
import xlrd
from openpyxl import load_workbook
import pickle
import math
import xlsxwriter
import numpy as np
np.random.seed(0)

type=2 #0=hierarchy, 1=no hiearchy, 2=all

annotations_loc="/home//workspace/Values_Of_ML/data/raw_annotations"

sheets=[]
names=[]
 
names, sheets=pickle.load(open('/home//workspace/Values_Of_ML/data/loaded_sheets.p', 'rb'))
start_ind=28

if type==0:
    value_names=["performance", "generalization", "efficiency", "researcher understanding", "building on past work", "novelty", "robustness"]
    value_indss=[[31,32,34], [9,10,33], [21,35,36,37,38,39,40,82], [48], [43,44], [7], [11]]
elif type==1:
    value_names=["performance", "generalization", "efficiency", "researcher understanding", "building on recent work", "novelty", "robustness"]
    value_indss=[[31], [9], [35], [48], [44], [7], [11]]
else:
    value_names=np.ndarray.tolist(sheets[0][27][7:90])
    value_indss=[list(range(7, 90))]

for sheet in sheets:
    for c_ind in range(sheet.shape[1]):
        sheet[16, c_ind]=float('nan')
    for row in range(sheet.shape[0]):
        if isinstance(sheet[row][0], str) and sheet[row][0]=='POWER ANALYSIS':
            for r_ind in range(row, row+10):
                for c_ind in range(sheet.shape[1]):
                    sheet[r_ind, c_ind]=float('nan')

values_list=sheets[0][27]

workbook=xlsxwriter.Workbook(os.path.join(annotations_loc, 'annotations_anon.xlsx'))
for sheet_ind in range(len(sheets)):
    worksheet=workbook.add_worksheet(str(sheet_ind))
    for row_ind in range(min(200, sheets[sheet_ind].shape[0])):
        for col_ind in range(sheets[sheet_ind].shape[1]):
            val=sheets[sheet_ind][row_ind][col_ind]
            if not isinstance(val, str) and math.isnan(val):
                val=""
            worksheet.write(row_ind, col_ind, val)
workbook.close()
