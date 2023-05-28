"""expertreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from expertreviewapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.mainhome,name='mainhome'),
    path('login/',views.login,name='login'),
    path('cusreg',views.cusreg,name='cusreg'),
    path('expertreg',views.expertreg,name='expertreg'),
    path('addvehicle',views.addvehicle,name='addvehicle'),
    path('company',views.company,name='company'),
    path('adminviewcus',views.adminviewcus,name='adminviewcus'),
    path('adminviewexpert',views.adminviewexpert,name='adminviewexpert'),
    path('adminviewvehicle',views.adminviewvehicle,name='adminviewvehicle'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('deletevehicle',views.deletevehicle,name='deletevehicle'),
    path('experthome',views.experthome,name='experthome'),
    path('companyhome',views.companyhome,name='companyhome'),
    path('expertviewvehicle',views.expertviewvehicle,name='expertviewvehicle'),
    path('comvvehicle',views.comviewvehicle,name='comvvehicle'),
    path('expertreview',views.expertreview,name='expertreview'),
    path('expertviewreviews',views.expertviewreviews,name='expertviewreviews'),
    path('cushome',views.cushome,name='cushome'),
    path('cusviewreviews',views.cusviewreviews,name='cusviewreviews'),
    path('custviewvehicle',views.custviewvehicle,name='expertreview'),
    
    path('expcardetails',views.expcardetails,name='expcardetails'),
    path('custcardetails',views.custcardetails,name='custcardetails'),
    path('adminreview',views.adminreview,name='adminreview'),
    path('adminreviewmore',views.adminreviewmore,name='adminreviewmore'),
    path('adminupdatereview',views.adminupdatereview,name='adminupdatereview'),
    
    path('expertprofile',views.expertprofile,name='expertprofile'),
    path('cusprofile',views.cusprofile,name='cusprofile'),
    path('req',views.req),
    path('expapp',views.expapp),
    path('exprem',views.exprem),
    path('cusvreq',views.cusvreq),
    path('expertvreq',views.expertvreq),
    path('comviewvehicle',views.comviewvehicle),
    path('inchat',views.inchat,name="inchat"),
    path('sfChatPer',views.sfChatPer,name="sfChatPer"),
    
    
    
    
    
]