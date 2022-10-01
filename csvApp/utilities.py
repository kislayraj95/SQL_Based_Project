import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)

df = pd.read_csv("sample.csv")
df = df[df['Segment'] != 'x']

def getAllData():
    return df

def deleteRow(rowNum):
    df = df.iloc[rowNum:]

def getRowCount():
    return df.shape[0]


def getHighestSales(top=5):
    a = []
    for i in df['  Sales ']:
        a.append(float(i.strip().replace("$","").replace(",","")))
    df_ro = df.copy()
    df_ro['  Sales '] = a
    df_1 = df_ro.sort_values(by=['  Sales '],ascending=False)
    return df_1[['Segment','Country',' Product ',' Discount Band ']].head(top).reset_index(drop=True)

def getMostRecentSales(top=5):
    df_ro = df.copy()
    df_ro['Year'] = df_ro['Year'].astype('int32')
    df_ro['Month Number'] = df_ro['Month Number'].astype('int32')
    df_ro.sort_values(by=['Year'],ascending=False)
    df_ro.sort_values(by=['Month Number'],ascending=False)
    return df_ro[['Segment',' Product ','Date']].head(top)

def getSegmentNames():
    return df['Segment'].unique()


def getHighestProfits(top=5):
    a = []
    count = 0
    for i in df[' Profit ']:
        a.append(float(i.strip().replace("$","").replace(",","")))
        count+=1
        if count == 5:
            break
    df_ro = df.head().copy()
    df_ro[' Profit '] = a
    df_1 = df_ro.sort_values(by=[' Profit '],ascending=False)
    return df_1[['Segment','Country',' Product ',' Discount Band ',' Profit ']].head(top).reset_index(drop=True)

