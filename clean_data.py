#clean datafiles and export to csv files

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
from feature_selector import FeatureSelector

PRG=pd.read_table('PRG_STUDENT_SITE_2017_2018_DATA_TABLE.txt',encoding='cp1252')
STU=pd.read_table('STUDENT_INTERNSHIP_2013_2018_DATA_TABLE.txt',encoding='cp1252',na_values=None,decimal=b',')
ADR=pd.read_table('ADR_STUDENTS_2017_2018_DATA_TABLE.txt',encoding='cp1252',na_values=["INCONNUE",'0'])

#Change city values to upper case
ADR['ADR_VILLE']=ADR['ADR_VILLE'].str.upper()
STU['VILLE']=STU['VILLE'].str.upper()
STU['PAYS']=STU['PAYS'].str.upper()

#Table STU

#missing values in 'ANNEE', try to fill with values in table PRG
STU[STU['ANNEE'].isnull().T]

#updating missing values in ANNEE
df=STU[STU['ANNEE'].isnull().T]
for i in (df.index):
    df1=PRG[PRG['ID_ANO']==STU.loc[i,'ID_ANO']]
    df2=df1[df1['ANNEE_SCOLAIRE']==STU.loc[i,'ANNEE_SCOLAIRE']]
    STU.loc[i,'ANNEE']=df2['PRG'].values
    
#missing values in ANNEE_SCOLAIRE, try to fill with values in table PRG
STU[STU['ANNEE_SCOLAIRE'].isnull().T]

#updating missing values in ANNEE_SCOLAIRE
df=STU[STU['ANNEE_SCOLAIRE'].isnull().T]
for i in (df.index):
    df1=PRG[PRG['ID_ANO']==STU.loc[i,'ID_ANO']]
    df2=df1[df1['PRG']==STU.loc[i,'ANNEE']]
    STU.loc[i,'ANNEE_SCOLAIRE']=df2['ANNEE_SCOLAIRE'].values
    
#missing values in CODE_POSTAL, try to fill with values already existed in table STU
STU[STU['CODE_POSTAL'].isnull().T]

#updating missing values in CODE_POSTAL
df=STU[STU['CODE_POSTAL'].isnull().T]
for i in (df.index):
    if df.loc[i,'VILLE']=='NaN':
        continue
    else:
        for j in (STU.index):
            if STU.loc[j,'VILLE']==STU.loc[i,'VILLE'] and STU.loc[j,'CODE_POSTAL']!='NaN':
                STU.loc[i,'CODE_POSTAL']=STU.loc[j,'CODE_POSTAL']
                break
                
#missing values in VILLE, try to fill with values already existed in table STU
STU[STU['VILLE'].isnull().T]

#updating missing values in VILLE
df=STU[STU['VILLE'].isnull().T]
for i in (df.index):
    if df.loc[i,'CODE_POSTAL']=='NaN':
        continue
    else:
        for j in (STU.index):
            if STU.loc[j,'CODE_POSTAL']==STU.loc[i,'CODE_POSTAL'] and STU.loc[j,'VILLE']!='NaN':
                STU.loc[i,'VILLE']=STU.loc[j,'VILLE']
                break
                
##updating missing values in REMUNERATION with Random Forest
def set_missing_res(df):
    
    re_df = df[['REMUNERATION', 'ANNEE', 'ANNEE_SCOLAIRE', 'ENTREPRISE', 'PAYS']]
    le = preprocessing.LabelEncoder()
    cols=['ANNEE','ANNEE_SCOLAIRE', 'ENTREPRISE', 'PAYS']
    for col in cols:
        le.fit(re_df[col])
        re_df[col]=le.transform(re_df[col])
 
    known_re = re_df[re_df.REMUNERATION.notnull()].as_matrix()
    unknown_re = re_df[re_df.REMUNERATION.isnull()].as_matrix()
 
    # Target remuneration
    y = known_re[:, 0]
 
    # features
    X = known_re[:, 1:]
 
    # fit in RandomForestRegressor
    rfr = RandomForestRegressor(random_state=0, n_estimators=2000, n_jobs=-1)
    rfr.fit(X, y)
 
    # estimiation
    predictedRes = rfr.predict(unknown_re[:, 1:])
    print (predictedRes)
    # update
    df.loc[ (df.REMUNERATION.isnull()), 'REMUNERATION' ] = predictedRes 
 
    return df, rfr
    
set_missing_res(STU)

#Table ADR
#updating missing values by PRG (If the information of student can be found in table PRG, let's suppose that he lives in Cergy)
df=ADR[ADR['ADR_VILLE'].isnull().T]
for i in df.index:
    if df.loc[i,'ID_ANO'] in list(PRG['ID_ANO'].values):
        ADR.loc[i,'ADR_CP']='95000'
        ADR.loc[i,'ADR_VILLE']='CERGY'
        
#Chech if thses students with NaN are in STU
count=0
df=ADR[ADR['ADR_VILLE'].isnull().T]
for i in df.index:
    if df.loc[i,'ID_ANO'] in list(STU['ID_ANO'].values):
        count=count+1
print(count)        
#Found count=0 which means that these student are not in table PRG or STU, so these lines will not be taken into consideration later
#Just delete these lines
ADR=ADR.dropna(subset=['ADR_VILLE'])

PRG.to_csv("Datafiles/PRG_STUDENT_SITE_2017_2018_DATA_TABLE.csv",index=False,sep=',')
ADR.to_csv("ADR_STUDENTS_2017_2018_DATA_TABLE.csv",index=False,sep=',')
STU.to_csv("STUDENT_INTERNSHIP_2013_2018_DATA_TABLE.csv",index=False,sep=',')
        
        