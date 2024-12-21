from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('registrar_maquina/', views.registrar_maquina, name='registrar_maquina'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('eliminar_cliente/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('lista_maquinas/', views.lista_maquinas, name='lista_maquinas'),
    path('lista_reparaciones/', views.lista_reparaciones, name='lista_reparaciones'),
    path('imprimir_reparacion/<int:pk>/', views.imprimir_reparacion, name='imprimir_reparacion'),
]
