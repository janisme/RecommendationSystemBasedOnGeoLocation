import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from math import radians, cos, sin, asin, sqrt
from sklearn.linear_model import LinearRegression

import os
import posixpath
from settings import BASE_DIR
from pathlib import Path

def predict_intership(PRG,Campus,ADR,PRG_ENT_df,Campus_ENT_df,ADR_ENT_df,Ent_nbIntern,w0,w1,w2):
    df_suggestion=pd.DataFrame()
    df_suggestion["PRG"]=PRG_ENT_df[PRG]
    df_suggestion["Campus"]=Campus_ENT_df[Campus]
    df_suggestion["ADR"]=ADR_ENT_df[ADR]

    df_suggestion_normalized=pd.DataFrame()
    for col in df_suggestion.columns:
        df_suggestion_normalized[col]=None
        x=df_suggestion[[col]].values.astype(float)
        min_max_scaler=preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df_suggestion_normalized[col]=pd.Series(x_scaled.reshape(-1))
        
    predicted_y=w0*df_suggestion_normalized["PRG"]+w1*df_suggestion_normalized["Campus"]+w2*df_suggestion_normalized["ADR"]
    
    result = Ent_nbIntern[predicted_y.sort_values(ascending=False).head(10).index]
    print(predicted_y.sort_values(ascending=False).head(10).index.values.tolist())
    df_result = pd.DataFrame(result.index)
    df_result.columns=["ENTREPRISE"]
    df_result["nb students with same PRG"]=PRG_ENT_df.loc[predicted_y.sort_values(ascending=False).head(10).index.values.tolist(),PRG].values
    df_result["nb students with same Campus"]=Campus_ENT_df.loc[predicted_y.sort_values(ascending=False).head(10).index.values.tolist(),Campus].values
    df_result["nb students with same ADR"]=ADR_ENT_df.loc[predicted_y.sort_values(ascending=False).head(10).index.values.tolist(),ADR].values
    
    return df_result

def Regression_DF(df, version):
    #Verify already if exist files:
    PRG_ENT_file=Path( os.path.join(BASE_DIR, 'DjangoWeb V1\Interface\static\PRG_ENT_df_'+str(version)+'.pkl'))
    Campus_ENT_file=Path( os.path.join(BASE_DIR, 'DjangoWeb V1\Interface\static\Campus_ENT_df_'+str(version)+'.pkl'))
    ADR_ENT_file=Path( os.path.join(BASE_DIR, 'DjangoWeb V1\Interface\static\ADR_ENT_df_'+str(version)+'.pkl'))
    Ent_nbIntern_file=Path( os.path.join(BASE_DIR, 'DjangoWeb V1\Interface\static\Ent_nbIntern_'+str(version)+'.pkl'))
    
    if PRG_ENT_file.is_file(): #and
        PRG_ENT_df = pd.read_pickle(PRG_ENT_file)
        Campus_ENT_df = pd.read_pickle(Campus_ENT_file)
        ADR_ENT_df = pd.read_pickle(ADR_ENT_file)
        Ent_nbIntern = pd.read_pickle(Ent_nbIntern_file)

    else:

        #We consider only the enterprises with more than 5 interns
        Ent_nbIntern=df["ENTREPRISE"].value_counts()
        Ent_nbIntern=Ent_nbIntern[Ent_nbIntern>5]

        PRG_ENT={}
        for prg in df["PRG"].unique():
            PRG_ENT[prg]=[]
            for ent in Ent_nbIntern.index:
                PRG_ENT[prg].append(len(df[(df["PRG"]==prg) & (df["ENTREPRISE"]==ent)]))
        PRG_ENT_df=pd.DataFrame(PRG_ENT)
        
        Campus_ENT={}
        for cam in df["SITE"].unique():
            Campus_ENT[cam]=[]
            for ent in Ent_nbIntern.index:
                Campus_ENT[cam].append(len(df[(df["SITE"]==cam) & (df["ENTREPRISE"]==ent)]))  
        Campus_ENT_df=pd.DataFrame(Campus_ENT)

        ADR_ENT={}
        for adr in df["ADR_VILLE"].unique():
            ADR_ENT[adr]=[]
            for ent in Ent_nbIntern.index:
                ADR_ENT[adr].append(len(df[(df["ADR_VILLE"]==adr) & (df["ENTREPRISE"]==ent)]))
        ADR_ENT_df=pd.DataFrame(ADR_ENT)

        # Save DF to File
        PRG_ENT_df.to_pickle( os.path.join(BASE_DIR, 'DjangoWeb V1\Interface\static\PRG_ENT_df_'+str(version)+'.pkl'))
        Campus_ENT_df.to_pickle( os.path.join(BASE_DIR, 'DjangoWeb V1\Interface\static\Campus_ENT_df_'+str(version)+'.pkl'))
        ADR_ENT_df.to_pickle( os.path.join(BASE_DIR, 'DjangoWeb V1\Interface\static\ADR_ENT_df_'+str(version)+'.pkl'))
        Ent_nbIntern.to_pickle( os.path.join(BASE_DIR, 'DjangoWeb V1\Interface\static\Ent_nbIntern_'+str(version)+'.pkl'))

    return PRG_ENT_df, Campus_ENT_df, ADR_ENT_df, Ent_nbIntern

def Regression(df, version):
    
    PRG_ENT_df, Campus_ENT_df, ADR_ENT_df, Ent_nbIntern = Regression_DF(df, version)
  
    M=len(Ent_nbIntern)
    Series_Ent=pd.Series(Ent_nbIntern.index)
    
    w0,w1,w2 = np.random.rand(3)

    df_ENT=pd.DataFrame(columns=df.columns)
    for ent in Ent_nbIntern.index:
        df_ENT=df_ENT.append(df[df["ENTREPRISE"]==ent])

    X=[]
    y=[]
    for i in df_ENT.index:
        PRG=df_ENT.loc[i,"PRG"]
        Campus=df_ENT.loc[i,"SITE"]
        ADR=df_ENT.loc[i,"ADR_VILLE"]
    
        df_suggestion=pd.DataFrame()
        df_suggestion["PRG"]=PRG_ENT_df[PRG]
        df_suggestion["Campus"]=Campus_ENT_df[Campus]
        df_suggestion["ADR"]=ADR_ENT_df[ADR]
    
        df_suggestion_normalized=pd.DataFrame()
        for col in df_suggestion.columns:
            df_suggestion_normalized[col]=None
            x=df_suggestion[[col]].values.astype(float)
            min_max_scaler=preprocessing.MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
            df_suggestion_normalized[col]=pd.Series(x_scaled.reshape(-1))
        
        X.append(df_suggestion_normalized)
    
        zeros=np.zeros(M)
        ent=df_ENT.loc[i,"ENTREPRISE"]
        index=Series_Ent[Series_Ent==ent].index
        zeros[index]=1.0
        y.append(zeros)
    
    w0,w1,w2=GradientDescent(X,y,w0,w1,w2,M)
    
    return w0,w1,w2

def GradientDescent(X,y,w0,w1,w2,M):
    learning_rate=0.05
    for i in range(30):
        w0 = w0 - learning_rate*differncial_w0(X,y,w0,w1,w2,M)
        w1 = w1 - learning_rate*differncial_w1(X,y,w0,w1,w2,M)
        w2 = w2 - learning_rate*differncial_w2(X,y,w0,w1,w2,M)
    return(w0, w1, w2)

def differncial_w0(X,y,w0,w1,w2,M):
    d0=0
    for i in range(len(X)):
        for j in range(M):
            d0=d0+(w0*X[i].iloc[j,0]+w1*X[i].iloc[j,1]+w2*X[i].iloc[j,2]-y[i][j])*X[i].iloc[j,0]/M
    return d0/len(X)

def differncial_w1(X,y,w0,w1,w2,M):
    d1=0
    for i in range(len(X)):
        for j in range(M):
            d1=d1+(w0*X[i].iloc[j,0]+w1*X[i].iloc[j,1]+w2*X[i].iloc[j,2]-y[i][j])*X[i].iloc[j,1]/M
    return d1/len(X)

def differncial_w2(X,y,w0,w1,w2,M):
    d2=0
    for i in range(len(X)):
        for j in range(M):
            d2=d2+(w0*X[i].iloc[j,0]+w1*X[i].iloc[j,1]+w2*X[i].iloc[j,2]-y[i][j])*X[i].iloc[j,2]/M
    return d2/len(X)

def bigEnterp1(df):
    bigs=df.groupby(['ENTREPRISE']).size().nlargest(3)
    label=bigs.index.values

    z=df.groupby('YEAR').size()
    years= z.index

    model = LinearRegression()
    qtd=[]
    qtdModel=[]
    for p in label:
        z=df[ (df['ENTREPRISE']==p) ].groupby('YEAR').size()
        X=pd.DataFrame(z.index)
        y=pd.DataFrame(z[:].values)
        model.fit(X, y)
        yLinear=model.predict(X)
        qtd.append(y)
        qtdModel.append(yLinear)
    
    print(label)
    print(qtd)
    print(qtdModel)
    return years, label, qtd, qtdModel