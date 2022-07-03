from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('importer',importer,name='importer'),
    path('register_usr',register_usr,name='register_usr'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('add_teacher',add_teacher,name='add_teacher'),
    path('view_teacher',view_teacher,name='view_teacher'),
    path('filter_teacher',filter_teacher,name='filter_teacher'),
    path('edit',edit,name='edit'),
    

     

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
