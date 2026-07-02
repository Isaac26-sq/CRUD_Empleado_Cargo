from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Cargo, Empleado
from .forms import CargoForm, EmpleadoForm


# ==========================================================================
#  PÁGINA DE INICIO
# ==========================================================================
def home(request):
    return render(request, 'gestion/home.html')


# ==========================================================================
#  ETAPA 1 — VISTAS BASADAS EN FUNCIONES (VBF / FBV)
# --------------------------------------------------------------------------
#  Cada operación del CRUD es una función. El programador controla
#  manualmente el flujo: leer el método, validar el formulario, guardar
#  y redirigir.
# ==========================================================================

# ---------- CRUD de CARGO (VBF) ----------

def cargo_lista_fbv(request):
    cargos = Cargo.objects.all()
    return render(request, 'gestion/cargo_list.html', {
        'cargos': cargos,
        'titulo': 'Cargos (Vistas Basadas en Funciones)',
        'url_crear': 'gestion:cargo_crear_fbv',
        'url_editar': 'gestion:cargo_editar_fbv',
        'url_eliminar': 'gestion:cargo_eliminar_fbv',
    })


def cargo_crear_fbv(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion:cargo_lista_fbv')
    else:
        form = CargoForm()
    return render(request, 'gestion/cargo_form.html', {
        'form': form,
        'titulo': 'Registrar cargo (VBF)',
        'url_volver': 'gestion:cargo_lista_fbv',
    })


def cargo_editar_fbv(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('gestion:cargo_lista_fbv')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'gestion/cargo_form.html', {
        'form': form,
        'titulo': 'Editar cargo (VBF)',
        'url_volver': 'gestion:cargo_lista_fbv',
    })


def cargo_eliminar_fbv(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        cargo.delete()
        return redirect('gestion:cargo_lista_fbv')
    return render(request, 'gestion/cargo_confirm_delete.html', {
        'objeto': cargo,
        'titulo': 'Eliminar cargo (VBF)',
        'url_volver': 'gestion:cargo_lista_fbv',
    })


# ---------- CRUD de EMPLEADO (VBF) ----------

def empleado_lista_fbv(request):
    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleado_list.html', {
        'empleados': empleados,
        'titulo': 'Empleados (Vistas Basadas en Funciones)',
        'url_crear': 'gestion:empleado_crear_fbv',
        'url_editar': 'gestion:empleado_editar_fbv',
        'url_eliminar': 'gestion:empleado_eliminar_fbv',
    })


def empleado_crear_fbv(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion:empleado_lista_fbv')
    else:
        form = EmpleadoForm()
    return render(request, 'gestion/empleado_form.html', {
        'form': form,
        'titulo': 'Registrar empleado (VBF)',
        'url_volver': 'gestion:empleado_lista_fbv',
    })


def empleado_editar_fbv(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('gestion:empleado_lista_fbv')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'gestion/empleado_form.html', {
        'form': form,
        'titulo': 'Editar empleado (VBF)',
        'url_volver': 'gestion:empleado_lista_fbv',
    })


def empleado_eliminar_fbv(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('gestion:empleado_lista_fbv')
    return render(request, 'gestion/empleado_confirm_delete.html', {
        'objeto': empleado,
        'titulo': 'Eliminar empleado (VBF)',
        'url_volver': 'gestion:empleado_lista_fbv',
    })


# ==========================================================================
#  ETAPA 2 — VISTAS BASADAS EN CLASES (VBC / CBV)
# --------------------------------------------------------------------------
#  Django trae vistas genéricas que ya implementan el patrón CRUD.
#  Solo se declara el modelo, el formulario y la plantilla; la lógica
#  repetitiva (leer método, validar, guardar, redirigir) ya viene hecha.
# ==========================================================================

# ---------- CRUD de CARGO (VBC) ----------

class CargoListView(ListView):
    model = Cargo
    template_name = 'gestion/cargo_list.html'
    context_object_name = 'cargos'
    extra_context = {
        'titulo': 'Cargos (Vistas Basadas en Clases)',
        'url_crear': 'gestion:cargo_crear_cbv',
        'url_editar': 'gestion:cargo_editar_cbv',
        'url_eliminar': 'gestion:cargo_eliminar_cbv',
    }


class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'gestion/cargo_form.html'
    success_url = reverse_lazy('gestion:cargo_lista_cbv')
    extra_context = {'titulo': 'Registrar cargo (VBC)', 'url_volver': 'gestion:cargo_lista_cbv'}


class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'gestion/cargo_form.html'
    success_url = reverse_lazy('gestion:cargo_lista_cbv')
    extra_context = {'titulo': 'Editar cargo (VBC)', 'url_volver': 'gestion:cargo_lista_cbv'}


class CargoDeleteView(DeleteView):
    model = Cargo
    template_name = 'gestion/cargo_confirm_delete.html'
    success_url = reverse_lazy('gestion:cargo_lista_cbv')
    context_object_name = 'objeto'
    extra_context = {'titulo': 'Eliminar cargo (VBC)', 'url_volver': 'gestion:cargo_lista_cbv'}


# ---------- CRUD de EMPLEADO (VBC) ----------

class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'gestion/empleado_list.html'
    context_object_name = 'empleados'
    extra_context = {
        'titulo': 'Empleados (Vistas Basadas en Clases)',
        'url_crear': 'gestion:empleado_crear_cbv',
        'url_editar': 'gestion:empleado_editar_cbv',
        'url_eliminar': 'gestion:empleado_eliminar_cbv',
    }


class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'gestion/empleado_form.html'
    success_url = reverse_lazy('gestion:empleado_lista_cbv')
    extra_context = {'titulo': 'Registrar empleado (VBC)', 'url_volver': 'gestion:empleado_lista_cbv'}


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'gestion/empleado_form.html'
    success_url = reverse_lazy('gestion:empleado_lista_cbv')
    extra_context = {'titulo': 'Editar empleado (VBC)', 'url_volver': 'gestion:empleado_lista_cbv'}


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'gestion/empleado_confirm_delete.html'
    success_url = reverse_lazy('gestion:empleado_lista_cbv')
    context_object_name = 'objeto'
    extra_context = {'titulo': 'Eliminar empleado (VBC)', 'url_volver': 'gestion:empleado_lista_cbv'}
