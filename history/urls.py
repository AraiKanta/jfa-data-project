from django.urls import path
from . import views

app_name = 'history'
urlpatterns = [
    path('', views.top, name='top'),
    path('year/', views.year_search, name='year_search'),
]