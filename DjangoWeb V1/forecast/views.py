from django.shortcuts import render
from django.shortcuts import HttpResponse

#from sklearn.model_selection import kFold
from sklearn.linear_model import LinearRegression
from dataCRUD.models import *
from Interface.scriptETL import *
from Interface.scriptForecast import *

import pandas as pd

def forecastPRG_STUDENT(request):
    df_PRG=PRG_STUDENT_SITE.pdobjects.all().to_dataframe()
    modelLinearRegress=LinearRegression()
    bigs=df_PRG.groupby(['PRG1']).size().nlargest(10)

    #Delete the years 2008 to 2011 (very small data)
    dfy=df_PRG[~df_PRG.index.isin(['2008','2008','2010','2011'])]
    programs=bigs.index.values
    for p in programs:
        #z contains xAxis=years yAxis=quantity students
        z=dfy[(dfy['PRG']==p)].groupby('ANNE').size()
        x=pd.DataFrame(z.index)
        y=pd.DataFrame(z[:].values)
        modelLinearRegress.fit(x,y)
# Create your views here.
