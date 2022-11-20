from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib import messages 
import logging

from django.db import models
from django.db import connection 

from Interface.scriptETL import *
from dataCRUD.models import *

from .forms import DocumentForm

import csv
import codecs
import ast
import re

def uploadCSV(request):
     #tables=models._meta.db_table
     #tables=connection.introspection.table_names()
     
     Models={'PRG_STUDENT_SITE':1,
             'ADR_STUDENTS':2,
             'STUDENT_INTERNSHIP':3,
            }
     #modelPicked = request.POST.get('tablesDropdown',False) 
    
     if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        if  'tableselected' in request.GET:
            tablePicked=request.GET.get('tableselected')
        else:
            tablePicked=request.GET.get('tableselected','empty')
            print(tablePicked)
        #else:
        #    return render(request,'uploadcsv.html',{'tables': Models})

        if not myfile.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse('uploadcsv'))
        elif myfile.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (myfile.size/(1000*1000),))
            return HttpResponseRedirect(reverse('uploadcsv'))
        
        #modelPicked=request.POST.get('tablesDropdown','')
        #modelPicked=request.GET['tablesDropdown']
        for key in Models:
            if key==modelPicked:
                print(modelPicked)
                file_data = myfile.read().decode("utf-8")		
                lines = file_data.split("\n")
                #loop over the lines and save them in db. If error , store as string and then display
                for line in lines:
                    if line.strip():
                    #   line = line.strip().strip('\n')
                        line.strip('\n')
                        fields = line.split(",")
                        prg_student_site=Models['modelPicked'](ID_ANO=fields[1],PRG=fields[2],ANNE_SCOLAIRE=fields[3],SITE=fields[4])
                        try:
                            prg_student_site.save()
                        except Exception as e:
                            messages.error(request,"Unable to upload file. "+repr(e))


  #      file_data = myfile.read().decode("utf-8")		
  #      lines = file_data.split("\n")
		##loop over the lines and save them in db. If error , store as string and then display
  #      for line in lines:
  #          if line.strip():
  #          #line = line.strip().strip('\n')
  #              line.strip('\n')
  #              fields = line.split(",")
  #              prg_student_site= PRG_STUDENT_SITE(ID_ANO=fields[1],PRG=fields[2],ANNE_SCOLAIRE=fields[3],SITE=fields[4])
  #              try:
  #                  prg_student_site.save()
  #              except Exception as e:
  #                  messages.error(request,"Unable to upload file. "+repr(e))
        
        #save file to server
        
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'uploadcsv.html', {
            'uploaded_file_url': uploaded_file_url
        })

     return render(request, 'uploadcsv.html',{'tables': Models})
    

def model_form_upload(request):
    df_PRG=PRG_STUDENT_SITE.pdobjects.all().to_dataframe()
    df_ADR=ADR_STUDENTS.pdobjects.all().to_dataframe()
    df_STU=STUDENT_INTERNSHIP.pdobjects.all().to_dataframe()  
    #Take the last version
    df_PRG_max=max(return_distinct_version(df_PRG))
    df_ADR_max=max(return_distinct_version(df_ADR))
    df_STU_max=max(return_distinct_version(df_PRG))
    next_version=(int) (max( df_PRG_max, df_ADR_max, df_STU_max ) ) +1

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            ptable=form.cleaned_data.get('selectedtable')

            #take the last version of table
            if ptable=="PRG_STUDENT_SITE":
                next_version = (int) (df_PRG_max) + 1
            if ptable=="ADR_STUDENTS":
                next_version = (int) (df_ADR_max) + 1
            if ptable=="STUDENT_INTERNSHIP":
                next_version = (int) (df_STU_max) + 1

            uploadedFile=request.FILES['document']
            fileType=form.cleaned_data.get('fileFormat').lower()
            separator=form.cleaned_data['separator']
            #Process the file
            if uploadedFile.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (myfile.size/(1000*1000),))
            
            if uploadedFile.name.endswith(fileType):
                if fileType=='csv':
                    handle_csv_file(uploadedFile,ptable, next_version)
                if fileType=='txt':
                    handle_uploaded_file(uploadedFile,ptable,separator, next_version)
            else:
                messages.error(request,'File is not CSV & text type')
                return HttpResponseRedirect(reverse('model_form_upload'))

            form.save()
            return HttpResponseRedirect(reverse('model_form_upload'))
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html',{'form': form})

def handle_uploaded_file(f,table,separator, version):
    
    file_data = f.read().decode("utf-8")		
    lines = file_data.split("\n")
    #loop over the lines and save them in db. If error , store as string and then display
    if table=="PRG_STUDENT_SITE":
        if separator=='comma':
            for line in lines:
                if line.strip():
                #   line = line.strip().strip('\n')
                    line.strip('\n')
                    fields = line.split(",")
                    prg_student_site=PRG_STUDENT_SITE(ID_ANO=fields[0],PRG=fields[1],ANNE_SCOLAIRE=fields[2],SITE=fields[3], idCSV=version)
                    try:
                        prg_student_site.save()
                    except Exception as e:
                        messages.error(request,"Unable to upload file. "+repr(e))   
        elif separator=='tab':
            for line in lines:
                if line.strip():
                #   line = line.strip().strip('\n')
                    line.strip('\n')
                    fields=line.split('\t')
                    #fields =re.split(r'\t+', line.rstrip('\t')) 
                    #prg_student_site=eval(table)(ID_ANO=fields[0],PRG=fields[1],ANNE_SCOLAIRE=fields[2],SITE=fields[3])
                    prg_student_site=PRG_STUDENT_SITE(ID_ANO=fields[0],PRG=fields[1],ANNE_SCOLAIRE=fields[2],SITE=fields[3],idCSV=version)
                    try:
                        prg_student_site.save()
                    except Exception as e:
                        messages.error(request,"Unable to upload file. "+repr(e))  
    if table=="ADR_STUDENTS":
            if separator=='comma':
                for line in lines:
                    if line.strip():
                        line.strip('\n')
                        fields = line.split(",")
                        adr_students=ADR_STUDENTS(ADR_CP=fields[0],ADR_VILLE=fields[1],ADR_PAYS=fields[2],ID_ANO=fields[3],idCSV=version)
                        try:
                            adr_students.save()
                        except Exception as e:
                            messages.error(request,"Unable to upload file. "+repr(e))   
            elif separator=='tab':
                for line in lines:
                    if line.strip():
                        line.strip('\n')
                        fields=line.split('\t')
                        adr_students=ADR_STUDENTS(ADR_CP=fields[0],ADR_VILLE=fields[1],ADR_PAYS=fields[2],ID_ANO=fields[3],idCSV=version)
                        try:
                            adr_students.save()
                        except Exception as e:
                            messages.error(request,"Unable to upload file. "+repr(e)) 
    if table=="STUDENT_INTERNSHIP":
            if separator=='comma':
                for line in lines:
                    if line.strip():
                        line.strip('\n')
                        fields = line.split(",")
                        student_intership=STUDENT_INTERNSHIP(ANNEE=fields[0],ANNEE_SCOLAIRE=fields[1],ENTERPRISE=fields[2],CODE_POSTAL=fields[3],
                                                             VILLE=fields[4],PAYS=fields[5],SUJET=fields[6],REMUNERATION=fields[7],ID_ANO=fields[8], idCSV=version)
                        try:
                            student_intership.save()
                        except Exception as e:
                            messages.error(request,"Unable to upload file. "+repr(e))   
            elif separator=='tab':
                for line in lines:
                    if line.strip():
                        line.strip('\n')
                        fields=line.split('\t')
                        student_intership=STUDENT_INTERNSHIP(ANNEE=fields[0],ANNEE_SCOLAIRE=fields[1],ENTERPRISE=fields[2],CODE_POSTAL=fields[3],
                                                             VILLE=fields[4],PAYS=fields[5],SUJET=fields[6],REMUNERATION=fields[7],ID_ANO=fields[8], idCSV=version)                        
                        try:
                            student_intership.save()
                        except Exception as e:
                            messages.error(request,"Unable to upload file. "+repr(e)) 


def handle_csv_file(f,tablePicked, version):
    reader = csv.DictReader(codecs.iterdecode(f, 'latin-1'))
    #reader = csv.DictReader(codecs.iterdecode(f, 'utf-8'))
 
    if tablePicked=='PRG_STUDENT_SITE':
        for row in reader:
            id_ano          =row['ID_ANO']
            prg             =row['PRG']
            anne_scolaire   =row['ANNE_SCOLAIRE']
            site            =row['SITE']
            prg_student_site=PRG_STUDENT_SITE(ID_ANO=id_ano,PRG=prg,ANNE_SCOLAIRE=anne_scolaire,SITE=site, idCSV=version)
            try:
                prg_student_site.save()
            except Exception as e:
                messages.error(request,"Unable to save csv data to the database. "+repr(e))   
    if tablePicked=='ADR_STUDENTS':
        for row in reader:
            adr_cp      =row['ADR_CP']
            adr_ville   =row['ADR_VILLE']
            adr_pays    =row['ADR_PAYS']           
            id_ano      =row['ID_ANO']
            adr_student =ADR_STUDENTS(ADR_CP=adr_cp,ADR_VILLE=adr_ville,ADR_PAYS=adr_pays,ID_ANO=id_ano, idCSV=version)
            try:
                adr_student.save()
            except Exception as e:
                messages.error(request,"Unable to save csv data to the database. "+repr(e)) 
    if tablePicked=='STUDENT_INTERNSHIP':
        for row in reader:
            annee=row['ANNEE']
            annee_scolaire=row['ANNEE_SCOLAIRE'] 
            entreprise=row['ENTREPRISE']
            code_postal=row['CODE_POSTAL']
            ville=row['VILLE']
            pays=row['PAYS']
            sujet=row['SUJET']
            remuneration=row['REMUNERATION'].replace(',', ".")
            #remuneration=ast.literal_eval(row['REMUNERATION'].replace(',', '.'))
            id_ano=row['ID_ANO']
            student_internship=STUDENT_INTERNSHIP(ANNEE=annee,ANNEE_SCOLAIRE=annee_scolaire,ENTREPRISE=entreprise,
                                                  CODE_POSTAL=code_postal,VILLE=ville,PAYS=pays,SUJET=sujet,
                                                  REMUNERATION=float(remuneration),ID_ANO=id_ano, idCSV=version)
            student_internship.save()
            #try:
            #    student_internship.save()
            #except Exception as e:
            #    messages.error(request,"Unable to save csv data to the database. "+repr(e)) 
# Create your views here.
