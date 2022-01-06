from django.contrib import admin
from django.urls import path
from indexing import views

urlpatterns = [
    path("", views.home, name="home"),
    path("1m-future", views.Table, name="table_1m-future"),
    path("5m-future", views.Table, name="table_5m-future"),
    path("1h-future", views.Table, name="table_1h-future"),
    path("4h-future", views.Table, name="table_4h-future"),
    path("1d-future", views.Table, name="table_1d-future"),
    path("1w-future", views.Table, name="table_1w-future"),
    path("all_tf-future", views.Table, name="table_all_tf-future"),
    path("1m-spot", views.Table, name="table_1m-spot"),
    path("5m-spot", views.Table, name="table_5m-spot"),
    path("1h-spot", views.Table, name="table_1h-spot"),
    path("4h-spot", views.Table, name="table_4h-spot"),
    path("1d-spot", views.Table, name="table_1d-spot"),
    path("1w-spot", views.Table, name="table_1w-spot"),
    path("all_tf-spot", views.Table, name="table_all_tf-spot"),
    path(
        "refresh_market_dtls", views.market_details_refresh, name="refresh_market_dtls"
    ),
    path("1w-future-kucoin", views.Table, name="table_1w-future-kucoin"),
]
