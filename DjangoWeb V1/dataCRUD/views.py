from django.shortcuts import render
from django.core.paginator import Paginator

from .models import PRG_STUDENT_SITE
from .models import ADR_STUDENTS
from .models import STUDENT_INTERNSHIP

from django.http import HttpResponse

#@login_required(login_url='/login')
def PRG_STUDENT_SITE_View(request,*args,**kwargs):
    PRG_STUDENT_SITE_list=PRG_STUDENT_SITE.objects.all()
    paginator=Paginator(PRG_STUDENT_SITE_list,25)
    page = request.GET.get('pagePRG')
    PRG_STUDENT_SITE_list=paginator.page(paginator.num_pages)
    #try:
    #    PRG_STUDENT_SITE_list=paginator.get_page(page)
    #except PageNotAnInteger:
    #    PRG_STUDENT_SITE_list=paginator.page(1)
    #except EmptyPage:
    #    PRG_STUDENT_SITE_list=paginator.page(paginator.num_pages)

    ADR_STUDENTS_list=ADR_STUDENTS.objects.all()
    paginator=Paginator(ADR_STUDENTS_list,25)
    page=request.GET.get('pageADR')
    ADR_STUDENTS_list=paginator.page(paginator.num_pages)
    #try:
    #    ADR_STUDENTS_list=paginator.get_page(page)
    #except PageNotAnInteger:
    #    ADR_STUDENTS_list=paginator.page(1)
    #except EmptyPage:
    #    ADR_STUDENTS_list=paginator.page(paginator.num_pages)
    STUDENT_INTERNSHIP_list=STUDENT_INTERNSHIP.objects.all()
    paginator=Paginator(STUDENT_INTERNSHIP_list,25)
    page=request.GET.get('pageSTU')
    STUDENT_INTERNSHIP_list=paginator.page(paginator.num_pages)

    context={'PRG_STUDENT_SITE_list':PRG_STUDENT_SITE_list,
             'ADR_STUDENTS_list':ADR_STUDENTS_list,
             'STUDENT_INTERNSHIP_list':STUDENT_INTERNSHIP_list}
    return render(request,"dataCRUD.html",context)




#def PRG_STUDENT_SITE_View(*args,**kwargs):
#    return HttpResponse('<h1>Display PRG_STUDENT_SITE_view</h1>')

# Create your views here.

