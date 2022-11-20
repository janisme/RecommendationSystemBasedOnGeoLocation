"""
Definition of urls for DjangoWeb.
"""

from datetime import datetime
from django.urls import re_path, include, path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
#from app import forms, views
from PRG_STUDENT_SITE.views import PRG_STUDENT_SITE_View
from Interface import views
from UploadingFile.views import uploadCSV
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    path('admin/', admin.site.urls),
    path('Interface/', views.home, name='home'),
    path('Interface/descriptiveStats', views.descriptiveStats, name='descriptiveStats'),
    path('Interface/maps', views.maps, name='maps'),
    path('Interface/contact_us',view.contact_us,name='contact_us'),
    # path('', views.home, name='home'),
    # path('contact/', views.contact, name='contact'),
    # path('about/', views.about, name='about'),
    # path('login/',
    #      LoginView.as_view
    #      (
    #          template_name='app/login.html',
    #          authentication_form=forms.BootstrapAuthenticationForm,
    #          extra_context=
    #          {
    #              'title': 'Log in',
    #              'year' : datetime.now().year,
    #          }
    #      ),
    #      name='login'),
    # path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    path('PRGSTUDENTSITE/',PRG_STUDENT_SITE_View, name='PRGSTUDENTSITE'), # Url to programstudentsite module
    #url(r'^upload/csv/$', views.upload_csv, name='upload_csv'),
    path('uploadcsv/',uploadCSV,name='uploadCSV'),

   ######### edit by Indu-- 
    path('',include('homescreen.urls')),
    path('register/',include('users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='homescreen/home.html'),name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view( template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
   #########
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)