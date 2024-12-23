from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('maquinas/', views.lista_maquinas, name='lista_maquinas'),
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('lista_clientes/', views.lista_clientes, name='lista_clientes'),
    path('eliminar_cliente/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('registrar_reparacion/<int:cliente_id>/', views.registrar_reparacion, name='registrar_reparacion'),
    path('lista_reparaciones/', views.lista_reparaciones, name='lista_reparaciones'),
    path("registrar_cliente_maquina/", views.registrar_cliente_maquina, name="registrar_cliente_maquina"),
    path("agregar_maquina_cliente/", views.agregar_maquina_cliente, name="agregar_maquina_cliente"),
]
