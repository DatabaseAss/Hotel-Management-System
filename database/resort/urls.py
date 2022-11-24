from django.urls import path
from  . import views

urlpatterns = [
    path('',views.dashboard, name = "dashboard"),
    path('room/',views.room, name = "room"),
    path('addroom/',views.addroom, name = "addroom"),
    path('roomtype/',views.roomtype, name = "roomtype")
]