from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    
    path('', views.home, name='home'),

 
    # CRUD Cargo (VBF)
    path('fbv/cargos/', views.cargo_lista_fbv, name='cargo_lista_fbv'),
    path('fbv/cargos/crear/', views.cargo_crear_fbv, name='cargo_crear_fbv'),
    path('fbv/cargos/editar/<int:pk>/', views.cargo_editar_fbv, name='cargo_editar_fbv'),
    path('fbv/cargos/eliminar/<int:pk>/', views.cargo_eliminar_fbv, name='cargo_eliminar_fbv'),

    # CRUD Empleado (VBF)
    path('fbv/empleados/', views.empleado_lista_fbv, name='empleado_lista_fbv'),
    path('fbv/empleados/crear/', views.empleado_crear_fbv, name='empleado_crear_fbv'),
    path('fbv/empleados/editar/<int:pk>/', views.empleado_editar_fbv, name='empleado_editar_fbv'),
    path('fbv/empleados/eliminar/<int:pk>/', views.empleado_eliminar_fbv, name='empleado_eliminar_fbv'),

    # CRUD Cargo (VBC)
    path('cbv/cargos/', views.CargoListView.as_view(), name='cargo_lista_cbv'),
    path('cbv/cargos/crear/', views.CargoCreateView.as_view(), name='cargo_crear_cbv'),
    path('cbv/cargos/editar/<int:pk>/', views.CargoUpdateView.as_view(), name='cargo_editar_cbv'),
    path('cbv/cargos/eliminar/<int:pk>/', views.CargoDeleteView.as_view(), name='cargo_eliminar_cbv'),

    # CRUD Empleado (VBC)
    path('cbv/empleados/', views.EmpleadoListView.as_view(), name='empleado_lista_cbv'),
    path('cbv/empleados/crear/', views.EmpleadoCreateView.as_view(), name='empleado_crear_cbv'),
    path('cbv/empleados/editar/<int:pk>/', views.EmpleadoUpdateView.as_view(), name='empleado_editar_cbv'),
    path('cbv/empleados/eliminar/<int:pk>/', views.EmpleadoDeleteView.as_view(), name='empleado_eliminar_cbv'),
]
