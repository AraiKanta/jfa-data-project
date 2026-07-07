from django.urls import path
from . import views

app_name = 'history'
urlpatterns = [
    path('', views.top, name='top'),
    path('year/', views.year_search, name='year_search'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('country/', views.country_record, name='country_record'),
    path('competition/', views.competition_record, name='competition_record')
]