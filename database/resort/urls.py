from django.urls import path
from  . import views

urlpatterns = [
    path('',views.home, name = "home"),
    path('room/',views.room, name = "room"),
    path('addroom/',views.addroom, name = "addroom"),
    path('roomtype/',views.roomtype, name = "roomtype"),
    path('branch/<int:branch>', views.dashboard, name = 'dashboard')
]