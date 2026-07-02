from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import Cargo, Empleado


class CrudFlowTest(TestCase):
    def setUp(self):
        self.cargo = Cargo.objects.create(nombre='Desarrollador', descripcion='Programa software')

    # ---------- VBF ----------
    def test_cargo_crud_fbv(self):
        # Crear
        self.client.post(reverse('gestion:cargo_crear_fbv'), {'nombre': 'Analista', 'descripcion': 'Analiza'})
        self.assertTrue(Cargo.objects.filter(nombre='Analista').exists())
        # Listar
        self.assertEqual(self.client.get(reverse('gestion:cargo_lista_fbv')).status_code, 200)
        # Editar
        c = Cargo.objects.get(nombre='Analista')
        self.client.post(reverse('gestion:cargo_editar_fbv', args=[c.pk]), {'nombre': 'Analista Senior', 'descripcion': 'x'})
        self.assertTrue(Cargo.objects.filter(nombre='Analista Senior').exists())
        # Eliminar
        self.client.post(reverse('gestion:cargo_eliminar_fbv', args=[c.pk]))
        self.assertFalse(Cargo.objects.filter(pk=c.pk).exists())

    def test_empleado_crud_fbv(self):
        datos = {'nombres': 'Ana', 'apellidos': 'Lopez', 'correo': 'ana@x.com',
                 'sueldo': '1500.00', 'fecha_ingreso': '2024-01-15', 'cargo': self.cargo.pk}
        self.client.post(reverse('gestion:empleado_crear_fbv'), datos)
        self.assertTrue(Empleado.objects.filter(nombres='Ana').exists())
        e = Empleado.objects.get(nombres='Ana')
        self.assertEqual(self.client.get(reverse('gestion:empleado_lista_fbv')).status_code, 200)
        self.client.post(reverse('gestion:empleado_eliminar_fbv', args=[e.pk]))
        self.assertFalse(Empleado.objects.filter(pk=e.pk).exists())

    # ---------- VBC ----------
    def test_cargo_crud_cbv(self):
        self.client.post(reverse('gestion:cargo_crear_cbv'), {'nombre': 'Gerente', 'descripcion': 'Dirige'})
        self.assertTrue(Cargo.objects.filter(nombre='Gerente').exists())
        self.assertEqual(self.client.get(reverse('gestion:cargo_lista_cbv')).status_code, 200)
        c = Cargo.objects.get(nombre='Gerente')
        self.client.post(reverse('gestion:cargo_editar_cbv', args=[c.pk]), {'nombre': 'Gerente General', 'descripcion': 'y'})
        self.assertTrue(Cargo.objects.filter(nombre='Gerente General').exists())
        self.client.post(reverse('gestion:cargo_eliminar_cbv', args=[c.pk]))
        self.assertFalse(Cargo.objects.filter(pk=c.pk).exists())

    def test_empleado_crud_cbv(self):
        datos = {'nombres': 'Luis', 'apellidos': 'Mora', 'correo': 'luis@x.com',
                 'sueldo': '2000.00', 'fecha_ingreso': '2023-06-01', 'cargo': self.cargo.pk}
        self.client.post(reverse('gestion:empleado_crear_cbv'), datos)
        self.assertTrue(Empleado.objects.filter(nombres='Luis').exists())
        e = Empleado.objects.get(nombres='Luis')
        self.assertEqual(self.client.get(reverse('gestion:empleado_lista_cbv')).status_code, 200)
        self.client.post(reverse('gestion:empleado_eliminar_cbv', args=[e.pk]))
        self.assertFalse(Empleado.objects.filter(pk=e.pk).exists())

    def test_str_methods(self):
        self.assertEqual(str(self.cargo), 'Desarrollador')
        emp = Empleado.objects.create(nombres='Juan', apellidos='Perez', correo='j@x.com',
                                      sueldo=1000, fecha_ingreso=date(2024, 1, 1), cargo=self.cargo)
        self.assertEqual(str(emp), 'Juan Perez')
