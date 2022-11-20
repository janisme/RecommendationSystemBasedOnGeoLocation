import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from math import radians, cos, sin, asin, sqrt
from feature_selector import FeatureSelector
import folium
from folium import plugins
from dataCRUD.models import *
from django_pandas.io import read_frame
import gmaps
import gmaps.datasets
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster

import os
import posixpath
from settings import BASE_DIR

def showMissingValues(df):
    df[df == ""] = np.nan
    df_new=df.isnull().sum().reset_index().rename(columns={'index': 'Column', 0: 'count'})
    return(df_new)


# 17-may-19
def return_distinct_prg(df):
    df_prg_uniq=df['PRG'].unique()     ## later try sorting alphabetically
    df_prg_uniq.sort()
    return(df_prg_uniq)

def return_distinct_ville(df):
    df_ville_uniq = df['VILLE'].unique()
    df_ville_uniq.sort()
    return(df_ville_uniq)

def return_distinct_enterp(df):
    df_enterp_uniq = df['ENTREPRISE'].unique()
    df_enterp_uniq.sort()
    return(df_enterp_uniq)

def return_distinct_site(df):
    df_uniq_site = df['SITE'].unique()
    df_uniq_site.sort()
    return(df_uniq_site)

def return_distinct_cp(df):
    df_cp_uniq = df['CODE_POSTAL'].unique().tolist()
    return (df_cp_uniq)

def return_distinct_rem(df):
    df_Rem_uniq = df['REMUNERATION'].unique().tolist()
    return (df_Rem_uniq)

def return_distinct_year(df):
    df_year_uniq = df['ANNEE_SCOLAIRE'].str[:4].unique()
    df_year_uniq.sort()
    return (df_year_uniq)

def return_distinct_version(df):
    df_uniq=df['idCSV'].unique()
    df_uniq.sort()     
    return(df_uniq)

def redefineDFTypes(df):
    for column in df:
        if column in ['ID_ANO']:
            df[column]=pd.to_numeric(df[column], errors='coerce')
            #df[column]= df[column].astype(str).astype(np.int64)
        if column in ['PRG','ANNE_SCOLAIRE','ANNEE_SCOLAIRE']:
            df[column]= df[column].astype(str)
        if column in ['REMUNERATION']:
            df[column]=pd.to_numeric(df[column], errors='coerce')
            # df[df[column] == ""] = "0"
            # df[column]= df[column].astype(np.float64)
            # df[df[column] == 0] = np.nan
    return(df)

def mergeTables(ADR,PRG,STU):
    df=PRG
    df=df.merge(ADR,left_on=['ID_ANO'], right_on=['ID_ANO'])
    df=df.merge(STU,left_on=['ID_ANO','PRG','ANNE_SCOLAIRE'],right_on=['ID_ANO','ANNEE','ANNEE_SCOLAIRE'])
    df['VILLE']=df['VILLE'].str.upper()
    df['PAYS']=df['PAYS'].str.upper()
    df['ADR_VILLE']=df['ADR_VILLE'].str.upper()
    df=df.drop(columns='ANNEE')
    return(df)

def deleteMissingValues(df):
    df=df[pd.notnull(df['REMUNERATION'])]
    df=df[pd.notnull(df['PRG'])]  
    df=df[pd.notnull(df['ANNEE_SCOLAIRE'])]  
    df=df[pd.notnull(df['CODE_POSTAL'])]  
    df=df[pd.notnull(df['ADR_CP'])]  
    df=df[pd.notnull(df['ADR_VILLE'])] 
    return(df)

def writeDF2Table(df, table, version, description):
    
    a=table.count()
    for index, rows in df.iterrows():
      
        table.create(
            ID_ANO          =rows.ID_ANO      ,
            PRG             =rows.PRG         ,
            ANNEE_SCOLAIRE  =rows.ANNEE_SCOLAIRE ,
            SITE            =rows.SITE        ,
            ADR_CP          =rows.ADR_CP      ,
            ADR_VILLE       =rows.ADR_VILLE   ,
            ADR_PAYS        =rows.ADR_PAYS    ,
            ANNEE           =rows.PRG       ,
            ENTREPRISE      =rows.ENTREPRISE  ,
            CODE_POSTAL     =rows.CODE_POSTAL ,
            VILLE           =rows.VILLE       ,
            PAYS            =rows.PAYS        ,
            SUJET           =rows.SUJET       ,
            REMUNERATION    =rows.REMUNERATION,
            ENT_LAT         =rows.ENT_LAT      ,
            ENT_LON         =rows.ENT_LON       ,
            ADR_LAT         =rows.ADR_LAT       ,
            ADR_LON         =rows.ADR_LON       ,
            SITE_LAT        =rows.SITE_LAT      ,
            SITE_LON        =rows.SITE_LON      ,
            home_campus     =rows.home_campus   ,
            home_entreprise =rows.home_entreprise,
            campus_entreprise =rows.campus_entreprise,
            idCSV           =version,
            idCSVDescript   =description
         )
    b=table.count()
    return(b-a)


# If User choose to update lines using algorithms
# By order 'PRG_STUDENT_SITE', 'ADR_STUDENTS', 'STUDENT_INTERNSHIP', 'df_location'
def UpdateMissingValues(ADR,PRG,STU,df_location):
    
    #updating missing values in ANNEE in table STU
    df=STU[STU['ANNEE'].isnull().T]
    for i in (df.index):
        df1=PRG[ PRG['ID_ANO']==STU.loc[i,'ID_ANO'] ]
        df2=df1[ df1['ANNEE_SCOLAIRE']==STU.loc[i,'ANNEE_SCOLAIRE'] ]
        STU.loc[i,'ANNEE']=df2['PRG'].values
    
    #updating missing values in ANNEE_SCOLAIRE in table STU
    df=STU[STU['ANNEE_SCOLAIRE'].isnull().T]
    for i in (df.index):
        df1=PRG[PRG['ID_ANO']==STU.loc[i,'ID_ANO']]
        df2=df1[df1['PRG']==STU.loc[i,'ANNEE']]
        STU.loc[i,'ANNEE_SCOLAIRE']=df2['ANNEE_SCOLAIRE'].values
    
    #updating missing values in CODE_POSTAL in table STU by the table df_location 
    df=STU[STU['CODE_POSTAL'].isnull().T]
    for i in (df.index):
        if df.loc[i,'VILLE']=='NaN':
            continue
        else:
            for j in (df_location.index):
                if df_location.loc[j,'VILLE']==STU.loc[i,'VILLE']:
                    STU.loc[i,'CODE_POSTAL']=df_location.loc[j,'CODE_POSTAL']
                    break
                    
    #updating missing values in VILLE in table STU by the table df_location
    df=STU[STU['VILLE'].isnull().T]
    for i in (df.index):
        if df.loc[i,'CODE_POSTAL']=='NaN':
            continue
        else:
            for j in (df_location.index):
                if df_location.loc[j,'CODE_POSTAL']==STU.loc[i,'CODE_POSTAL']:
                    STU.loc[i,'VILLE']=df_location.loc[j,'VILLE']
                    break
    
    #updating missing values in REMUNERATION in table STU
    re_df = STU[['REMUNERATION', 'ANNEE', 'ANNEE_SCOLAIRE', 'ENTREPRISE', 'PAYS']]
    le = preprocessing.LabelEncoder()
    cols=['ANNEE','ANNEE_SCOLAIRE', 'ENTREPRISE', 'PAYS']
    for col in cols:
        le.fit(re_df[col])
        re_df[col]=le.transform(re_df[col])
    known_re = re_df[re_df.REMUNERATION.notnull()].values
    unknown_re = re_df[re_df.REMUNERATION.isnull()].values
    # Target remuneration
    y = known_re[:, 0]
    # features
    X = known_re[:, 1:]
    # fit in RandomForestRegressor
    rfr = RandomForestRegressor(random_state=0, n_estimators=2000, n_jobs=-1)
    rfr.fit(X, y)
    # estimiation
    predictedRes = rfr.predict(unknown_re[:, 1:])
    # update
    STU.loc[ (STU.REMUNERATION.isnull()), 'REMUNERATION' ] = predictedRes 
 
 
     #updating missing values in ADR_CP in table ADR by df_location
    df=ADR[ADR['ADR_CP'].isnull().T]
    for i in (df.index):
        if df.loc[i,'ADR_VILLE']=='NaN':
            continue
        else:
            for j in (df_location.index):
                if df_location.loc[j,'VILLE']==ADR.loc[i,'ADR_VILLE']:
                    ADR.loc[i,'ADR_CP']=df_location.loc[j,'CODE_POSTAL']
                    break
                    
    #updating missing values in VILLE in table ADR by df_location
    df=ADR[ADR['ADR_VILLE'].isnull().T]
    for i in (df.index):
        if df.loc[i,'ADR_CP']=='NaN':
            continue
        else:
            for j in (df_location.index):
                if df_location.loc[j,'CODE_POSTAL']==ADR.loc[i,'ADR_CP']:
                    ADR.loc[i,'ADR_VILLE']=df_location.loc[j,'VILLE']
                    break
 
    return ADR,PRG,STU




def heatmap_ftr_slcor(df):                    # heatlap feature selector funciton
    le={}
    le_df=df.drop(columns='ANNEE')
    le_df['ADR_CP']=le_df['ADR_CP'].astype(object)
    for col in le_df.columns:                                                   ### cai's code
        if le_df.dtypes[col]=='object':
            le_df[col]=le_df[col].str.upper()
            le[col]=LabelEncoder()
            result=le[col].fit_transform(le_df[le_df[col].notnull()][col])
            le_df.loc[le_df[le_df[col].notnull()].index,col]=result
    
    fs = FeatureSelector(data = le_df, labels = df['REMUNERATION'])
    cor_out=le_df.corr()
    #cor_out.drop(columns=['idCSV','ID_ANO','id','PAYS','SUJET','idCSVDescript'],inplace=True)         ## dropping unwanted columns
    cor_out.drop(columns=['idCSV','ID_ANO','id','PAYS','SUJET','idCSVDescript','SITE_LON','SITE_LAT','ADR_LAT','ADR_LON','ENT_LAT','ENT_LON'],inplace=True)                                                      
    # print(cor_out.columns)
    new_df= pd.DataFrame(columns=['group','variable','value'])                  # new dataframe
    new_df.columns
    k=0
    li=list(cor_out.columns)
    # print(li)
    length=len(li)
    #cor_out.reset_index(inplace=True, drop=True)
    i_ind=0
    k=0
    
    while i_ind<length:                                                 ## to group all the variables according as shown in the "indu.csv", so as to be fead to heatmap
        #print(li[i_ind])
        for i in li:
            new_df.loc[k,'group']=li[i_ind]
            new_df.loc[k,'variable']=i
            new_df.loc[k,'value']=cor_out.loc[i,li[i_ind]]          ##### since all the values are very very less, there aren't showing significant difference in heatmap
            k=k+1                                                      ##### so just multiplied by 10 .... THIS HAS TO BE CHECKED
        i_ind=i_ind+1
    # print(new_df.head(3))
    new_df.to_csv( os.path.join(BASE_DIR, 'DjangoWeb V1\Interface\static\indu.csv') ,index=False)
    return  None

def map2():
    adr=mergedTables.objects.all() 
    qs_adr= adr
    df_of_query_result_adr= read_frame(qs_adr)
    newTable_adr=df_of_query_result_adr
    m= folium.Map(location=[48.8566,2.3522],tiles = "Stamen Toner",zoom_start=2)
    #cergy=['49.034955','2.069925']
    #pau=['43.319568','-0.360571']
    newTable_ent_adr= newTable_adr[['ENT_LAT','ENT_LON']]
    newTable_stu_adr= newTable_adr[['ADR_LAT','ADR_LON']]
    newTable_site_adr= newTable_adr[['SITE_LAT','SITE_LON']]
    newTable_ent_adr= newTable_ent_adr.dropna(axis=0, subset=['ENT_LAT','ENT_LON'])
    newTable_stu_adr= newTable_stu_adr.dropna(axis=0, subset=['ADR_LAT','ADR_LON'])
    newTable_site_adr= newTable_site_adr.dropna(axis=0, subset=['SITE_LAT','SITE_LON'])
    #newTable_ent_adr= [[row['ENT_LAT'],row['ENT_LON']] for index,row in newTable_ent_adr.iterrows() ]
    #newTable_stu_adr= [[row['ADR_LAT'],row['ADR_LON']] for index,row in newTable_stu_adr.iterrows() ]
    #HeatMap(cergy).add_to(m)
    HeatMap(newTable_stu_adr).add_to(m)
    mc = MarkerCluster()
    folium.CircleMarker([49.034955, 2.069925],
                    radius=20,
                    popup='Cergy Campus',
                    color='red',
                    ).add_to(m)
    folium.CircleMarker([43.319568, -0.360571],
                    radius=20,
                    popup='Pau Campus',
                    color='red',
                    ).add_to(m)

    for i in range(0,len(newTable_stu_adr)):
        #mc.add_child(folium.Marker([newTable_ent_adr.iloc[i]['ENT_LAT'],newTable_ent_adr.iloc[i]['ENT_LON']],icon=folium.Icon(icon='cloud'))).add_to(m)
        mc.add_child(folium.Marker([newTable_ent_adr.iloc[i]['ENT_LAT'],newTable_ent_adr.iloc[i]['ENT_LON']])).add_to(m)
        #mc.add_child(folium.Marker([newTable_stu_adr.iloc[i]['ADR_LAT'],newTable_stu_adr.iloc[i]['ADR_LON']],icon=folium.Icon(color='red'))).add_to(m)
        #folium.Marker([newTable_site_adr.iloc[i]['SITE_LAT'],newTable_site_adr.iloc[i]['SITE_LON']],icon=folium.Icon(icon='green')).add_to(m)
        #m.add_children(plugins.HeatMap(newTable_adr_lo, radius=15))

    m.save( os.path.join(BASE_DIR,'DjangoWeb V1\Interface\\templates\map.html') )
    return None
    
def change(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


#num of records
def num_records1(df):
    amount = len(df.index)
    # return(change(amount))
    return((amount))

#num of students
def num_std1(df):
    amount=len(df['ID_ANO'].unique())
    # return(change(amount))
    return((amount))

#num of enterprise
def num_entre1(df):
    amount=len(df['ENTREPRISE'].unique())
    # return (change(amount))
    return ((amount))

#mean of salary
def mean_sal1(df):
    df['REMUNERATION'] = pd.to_numeric(df['REMUNERATION'], errors='coerce')
    meansal = df['REMUNERATION'].mean()
    
    # print(meansal)
    meansal = "€ {:,.2f}".format(meansal)
    return(meansal)

#mean of salary
def mean_sal2(df):
    df['REMUNERATION'] = pd.to_numeric(df['REMUNERATION'], errors='coerce')
    meansal = df['REMUNERATION'].mean()
    # print(meansal)
    meansal = "€ {:,.2f}".format(meansal)
    return(meansal)

def stddist(df,cat):
    le = preprocessing.LabelEncoder()
    le.fit(df[cat][df[cat].notnull()])
    le = np.array(le.classes_)
    col=[]
    for i in le:
        df2=df[df['SITE']==i]
        col.append(len(df2['ID_ANO'].unique()))
    return(col,le)

#std_number
def count_std(df,cat):
    ct=df.groupby(['SITE','PRG']).count()
    ind=ct.index
    ind = np.array(ind.codes)

    le = preprocessing.LabelEncoder()
    le.fit(df[cat][df[cat].notnull()])
    leng=len(le.classes_)
    le = np.array(le.classes_)

    cergy=np.zeros(leng)
    pau=np.zeros(leng)
    count=0
    for i in ind[0]:
        if i == 0:
            if np.isnan(ct['ID_ANO'][count])==False:
                cergy[ind[1][count]]=ct['ID_ANO'][count]

        else:
            if np.isnan(ct['ID_ANO'][count])==False:
                pau[ind[1][count]]=ct['ID_ANO'][count]
            else:
                cergy[ind[1][count]]=0
        count=count+1
    return(cergy,pau,le)

def salary_avg(df,cat):

    le = preprocessing.LabelEncoder()
    le.fit(df[cat][df[cat].notnull()])
    leng = len(le.classes_)
    le = np.array(le.classes_)

    df['REMUNERATION'] = pd.to_numeric(df['REMUNERATION'],errors='coerce')
    mean=df.groupby(['SITE','PRG']).mean()
    ind=mean.index
    ind = np.array(ind.codes)

    cergy=np.zeros(leng)
    pau=np.zeros(leng)
    count=0

    for i in ind[0]:
        if i == 0:
            if np.isnan(mean['REMUNERATION'][count])==False:
                cergy[ind[1][count]]="{:5.2f}".format(mean['REMUNERATION'][count])
        else:
            if np.isnan(mean['REMUNERATION'][count])==False:
                pau[ind[1][count]]="{:5.2f}".format(mean['REMUNERATION'][count])
            else:
                cergy[ind[1][count]]=0
        count=count+1

    return(cergy,pau,le)


# Catch location from table df_location
def CatchLocation(df, df_location):
    df['ADR_LAT']=None
    df['ADR_LON']=None
    df['SITE_LAT']=None
    df['SITE_LON']=None
    df['ENT_LAT']=None
    df['ENT_LON']=None
    
    for i in (df.index):
        for j in (df_location.index):
            if df_location.loc[j,'VILLE']==df.loc[i,'ADR_VILLE']:
                    df.loc[i,'ADR_LAT']=df_location.loc[j,'LAT']
                    df.loc[i,'ADR_LON']=df_location.loc[j,'LON']
                    break

    for i in (df.index):
        for j in (df_location.index):
            if df_location.loc[j,'VILLE']==df.loc[i,'VILLE']:
                    df.loc[i,'ENT_LAT']=df_location.loc[j,'LAT']
                    df.loc[i,'ENT_LON']=df_location.loc[j,'LON']
                    break
                    
    for j in (df_location.index):
        if df_location.loc[j,'VILLE']=='EISTI Cergy':
            lat=df_location.loc[j,'LAT']
            lon=df_location.loc[j,'LON']
            break

    for i in df[df["SITE"]=='Cergy'].index:
                df.loc[i,"SITE_LAT"]=lat
                df.loc[i,"SITE_LON"]=lon
                
    for j in (df_location.index):
        if df_location.loc[j,'VILLE']=='EISTI Pau':
            lat=df_location.loc[j,'LAT']
            lon=df_location.loc[j,'LON'] 
            break   

    for i in df[df["SITE"]=='Pau'].index:
                df.loc[i,"SITE_LAT"]=lat
                df.loc[i,"SITE_LON"]=lon
    
    
    df['ENT_LAT']=df['ENT_LAT'].astype(float)
    df['ENT_LON']=df['ENT_LON'].astype(float)
    df['ADR_LAT']=df['ADR_LAT'].astype(float)
    df['ADR_LON']=df['ADR_LON'].astype(float)
    df['SITE_LAT']=df['SITE_LAT'].astype(float)
    df['SITE_LON']=df['SITE_LON'].astype(float)
    
    df=df.dropna(subset=['ENT_LAT'])
    df=df.dropna(subset=['ADR_LAT'])
    df=df.dropna(subset=['SITE_LAT'])
    
    return df


# Calculate distances
def haversine(lon1, lat1, lon2, lat2): 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r * 1000
    
def UpdateDistance(df):
    df['home_campus']=None
    df['home_entreprise']=None
    df['campus_entreprise']=None
    for i in df.index:
        df.loc[i,"home_campus"]=haversine(df.loc[i,"ADR_LON"],df.loc[i,"ADR_LAT"],df.loc[i,"SITE_LON"],df.loc[i,"SITE_LAT"])
        df.loc[i,"home_entreprise"]=haversine(df.loc[i,"ADR_LON"],df.loc[i,"ADR_LAT"],df.loc[i,"ENT_LON"],df.loc[i,"ENT_LAT"])
        df.loc[i,"campus_entreprise"]=haversine(df.loc[i,"SITE_LON"],df.loc[i,"SITE_LAT"],df.loc[i,"ENT_LON"],df.loc[i,"ENT_LAT"])
    df['home_campus']=df['home_campus'].astype(float)
    df['home_entreprise']=df['home_entreprise'].astype(float)
    df['campus_entreprise']=df['campus_entreprise'].astype(float)
    
    return df
    
def topx(df,cat):
    df2=df[['ID_ANO',cat]]
    df2=df2.groupby([cat]).count().sort_values(['ID_ANO'],ascending=False)
    top=list(df2['ID_ANO'][0:10])
    label = df2.index[0:10]
    return(top,label)
