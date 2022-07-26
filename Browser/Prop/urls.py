from django.contrib import admin
from django.urls import path,include
from Prop import views

urlpatterns = [
  path("", views.index, name='home'),
  path("search2", views.search2),
  path("search3", views.search3),
  path('create', views.create, name='create'),
  path('imageTab', views.imageTab, name='imageTab'),
  path('videoTab',views.videoTab,name='videoTab')
]