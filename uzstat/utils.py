import numpy as np
import pandas as pd

def smoothTriangle(data, degree):
    triangle=np.concatenate((np.arange(degree + 1), np.arange(degree)[::-1])) # up then down
    smoothed=[]

    for i in range(degree, len(data) - degree * 2):
        point=data[i:i + len(triangle)] * triangle
        smoothed.append(np.sum(point)/np.sum(triangle))
    # Handle boundaries
    smoothed=[smoothed[0]]*int(degree + degree/2) + smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    return smoothed



def typek (cement_type):
    residue80_top= df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type), ' помол. 80 мкм' ].iloc[0]
    residue80_low= df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type), ' помол. 80 мкм' ].iloc[0]
    residue45_top = df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type), ' помол, 45 мкм' ].iloc[0]
    residue45_low = df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type), ' помол, 45 мкм' ].iloc[0]
    blain_top = df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type), 'уд.поверхность' ].iloc[0]
    blain_low = df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type), 'уд.поверхность' ].iloc[0]
    so3_top = df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type), 'SO3,%' ].iloc[0]
    so3_low = df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type), 'SO3,%' ].iloc[0]
    resid= df1[' помол. 80 мкм'].loc[df1[' помол. 80 мкм']> (100-residue80_top) ].count()
    resid2 = df1[' помол. 80 мкм'].loc[df1[' помол. 80 мкм']< (100-residue80_low) ].count()
    resid45 = df1[' помол, 45 мкм'].loc[df1[' помол, 45 мкм']> residue45_top ].count()

    reply_positive = 'хорошо, показатели в пределах целевых занчений'
    reply_negative = 'плохо, показтели вне пределов целевых занчений'

    if resid  != 0:
        answer = reply_negative
    else :
        answer = reply_positive
    if resid2 !=0:
        answer_residue = reply_negative
    else :
        answer_residue = reply_positive
    if  resid45 !=0:
        answer_residue45 = reply_negative
    else:
        answer_residue45 = reply_positive

    return  answer,resid,  answer_residue , resid2 , answer_residue45, resid45
