from django.contrib import admin
from django.urls import path
from indexing import views
  
urlpatterns = [
    path('', views.home, name ="home"),
    path('1m', views.Table_1m, name ="table_1m"),
    path('5m', views.Table_5m, name ="table_5m"),
    path('1h', views.Table_1h, name ="table_1h"),
    path('refresh_market_dtls', views.market_details_refresh, name = "refresh_market_dtls")
]