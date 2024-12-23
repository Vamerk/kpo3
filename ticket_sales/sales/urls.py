from django.urls import path
from . import views

urlpatterns = [
    path('routes/', views.route_list, name='route_list'),
    path('purchase/<int:route_id>/', views.purchase_ticket, name='purchase_ticket'),
    path('ticket/<int:ticket_id>/', views.success, name='success'),
    path('report/', views.report, name='report'),
    path('about/', views.adout_page, name='about'),
    path('', views.head_page, name='head')
]


