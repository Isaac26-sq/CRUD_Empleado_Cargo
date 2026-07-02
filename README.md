# CRUD de Empleados y Cargos — Django (VBF y VBC)

Proyecto de la **Guía 3**: un CRUD completo implementado de **dos formas** para comparar **Vistas Basadas en Funciones (VBF/FBV)** y **Vistas Basadas en Clases (VBC/CBV)**.

---

## 📑 Contenido

- [Descripción](#descripción)
- [Modelos](#modelos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Cómo ejecutar](#cómo-ejecutar)
- [Rutas disponibles](#rutas-disponibles)
- [VBF vs VBC: la comparación (para la defensa)](#vbf-vs-vbc-la-comparación-para-la-defensa)
- [Puntos clave para defender](#puntos-clave-para-defender)

---

## Descripción

La aplicación gestiona **Cargos** y **Empleados** con las cuatro operaciones CRUD (listar, crear, editar, eliminar) sobre cada modelo. Todo el CRUD está implementado **dos veces**:

1. **Etapa 1 — VBF:** cada operación es una función en `views.py`.
2. **Etapa 2 — VBC:** las mismas operaciones usando las vistas genéricas de Django (`ListView`, `CreateView`, `UpdateView`, `DeleteView`).

Ambas versiones conviven en la misma app (`gestion`) y comparten modelos, formularios y plantillas, para que la comparación sea directa.

---

## Modelos

**Cargo**

| Campo | Tipo |
|-------|------|
| `nombre` | CharField (máx. 100) |
| `descripcion` | CharField (máx. 200, opcional) |

**Empleado**

| Campo | Tipo |
|-------|------|
| `nombres` | CharField (máx. 100) |
| `apellidos` | CharField (máx. 100) |
| `correo` | EmailField |
| `sueldo` | DecimalField (10 dígitos, 2 decimales) |
| `fecha_ingreso` | DateField |
| `cargo` | ForeignKey → Cargo |

**Relación:** un `Cargo` puede tener varios `Empleado` (uno a muchos). Cada `Empleado` pertenece a un único `Cargo`. La FK usa `on_delete=models.PROTECT`, de modo que no se puede borrar un cargo que aún tenga empleados asignados. Ambos modelos implementan `__str__()`.

---

## Estructura del proyecto

```
crud_empleados/
├── manage.py
├── requirements.txt
├── db.sqlite3                  # incluye datos de ejemplo + superusuario
├── crud_empleados/            # configuración del proyecto
│   ├── settings.py
│   ├── urls.py                # incluye las urls de la app
│   └── wsgi.py / asgi.py
└── gestion/                    # app principal
    ├── models.py              # Cargo y Empleado
    ├── forms.py               # CargoForm y EmpleadoForm (cargo = desplegable)
    ├── views.py               # VBF (funciones) + VBC (clases)
    ├── urls.py                # rutas /fbv/... y /cbv/...
    ├── admin.py               # modelos registrados en el admin
    ├── migrations/
    └── templates/
        ├── base.html
        └── gestion/
            ├── home.html
            ├── cargo_list.html / cargo_form.html / cargo_confirm_delete.html
            └── empleado_list.html / empleado_form.html / empleado_confirm_delete.html
```

---

## Cómo ejecutar

```bash
# 1. Crear y activar el entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones (la BD ya viene incluida, pero por si acaso)
python manage.py migrate

# 4. Ejecutar el servidor
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`.

**Admin:** `http://127.0.0.1:8000/admin/` — usuario `admin`, contraseña `admin123`.

> La base de datos incluida trae 3 cargos y 3 empleados de ejemplo. Si prefieres empezar de cero, borra `db.sqlite3` y corre `python manage.py migrate` de nuevo.

---

## Rutas disponibles

**Etapa 1 — VBF**

| Operación | URL |
|-----------|-----|
| Listar cargos | `/fbv/cargos/` |
| Crear cargo | `/fbv/cargos/crear/` |
| Editar cargo | `/fbv/cargos/editar/<id>/` |
| Eliminar cargo | `/fbv/cargos/eliminar/<id>/` |
| Listar empleados | `/fbv/empleados/` |
| Crear empleado | `/fbv/empleados/crear/` |
| Editar empleado | `/fbv/empleados/editar/<id>/` |
| Eliminar empleado | `/fbv/empleados/eliminar/<id>/` |

**Etapa 2 — VBC** (misma estructura con prefijo `/cbv/`)

| Operación | URL |
|-----------|-----|
| Listar cargos | `/cbv/cargos/` |
| Crear cargo | `/cbv/cargos/crear/` |
| ... | `/cbv/...` |

---

## VBF vs VBC: la comparación (para la defensa)

Este es el objetivo de la guía. La diferencia entre los dos estilos:

**Vista Basada en Función (crear un cargo):**
```python
def cargo_crear_fbv(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion:cargo_lista_fbv')
    else:
        form = CargoForm()
    return render(request, 'gestion/cargo_form.html', {'form': form})
```

**Vista Basada en Clase (equivalente):**
```python
class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'gestion/cargo_form.html'
    success_url = reverse_lazy('gestion:cargo_lista_cbv')
```

Hacen **exactamente lo mismo**, pero la VBC no repite la lógica de "si es POST valida y guarda, si no muestra el formulario": esa lógica ya viene implementada dentro de `CreateView`.

| Aspecto | VBF (funciones) | VBC (clases) |
|---------|-----------------|--------------|
| Cómo se define | Una función por operación | Una clase que hereda de una vista genérica |
| Código | Más líneas, todo explícito | Menos líneas, la lógica común viene heredada |
| Control del flujo | Total y visible | Implícito (se personaliza sobrescribiendo métodos/atributos) |
| Curva de aprendizaje | Más fácil de leer para principiantes | Requiere conocer las vistas genéricas |
| Reutilización | Baja (se copia y pega) | Alta (herencia y mixins) |
| Ideal para | Lógica muy específica o a medida | CRUD estándar y repetitivo |

---

## Puntos clave para defender

- **La relación FK y su navegación:** un cargo tiene muchos empleados (`cargo.empleados.all()` gracias al `related_name='empleados'`); un empleado tiene un cargo (`empleado.cargo`).
- **Por qué `PROTECT` y no `CASCADE`:** con `PROTECT`, borrar un cargo con empleados asignados lanza un error y protege los datos, en vez de borrar en cascada a todos los empleados de ese cargo.
- **El campo `cargo` como desplegable:** en `EmpleadoForm` se define con `forms.Select`, y como es una FK, Django llena automáticamente el desplegable con los cargos registrados (usando su `__str__`).
- **Por qué el `__str__`:** hace que en el desplegable, el admin y el shell se vea el nombre del cargo / el nombre del empleado en vez de `Cargo object (1)`.
- **VBC más corto:** `CreateView`, `UpdateView` y `DeleteView` ya traen el patrón "validar formulario → guardar → redirigir"; por eso las clases son tan cortas.
- **Plantillas compartidas:** ambas versiones (VBF y VBC) usan las mismas plantillas, pasando por contexto los nombres de las rutas a usar. Esto evita duplicar HTML (buena práctica DRY).

---

*Proyecto Django · CRUD de Empleados y Cargos · Guía 3 (VBF y VBC)*
