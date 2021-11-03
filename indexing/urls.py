from django.contrib import admin
from django.urls import path
from indexing import views
  
urlpatterns = [
    path('', views.home, name ="home"),
    path('1m', views.Table, name ="table_1m"),
    path('5m', views.Table, name ="table_5m"),
    path('1h', views.Table, name ="table_1h"),
    path('4h', views.Table, name ="table_4h"),
    path('1d', views.Table, name ="table_1d"),
    path('all_tf', views.Table, name ="table_all_tf"),
    path('refresh_market_dtls', views.market_details_refresh, name = "refresh_market_dtls")
]