from django.urls import path, include

from . import views

# urlpatterns ?

urlpatterns = [

    path("", views.home, name="home"),
    path("home",views.home,name='home'),
    path("c_Name",views.c_Name,name="c_Name"),
    path("ll_Name",views.ll_Name,name="ll_Name")
]


