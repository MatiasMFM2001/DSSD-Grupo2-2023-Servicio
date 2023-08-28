# Validación HTML

Se ha validado el [Listado de usuarios](https://admin-grupo20.proyecto2022.linti.unlp.edu.ar/usuarios/listado), con un Administrador y un Operador en la lista

## Error: Duplicate ID `navbarDropdownMenuLink`
From line 82, column 25; to line 82, column 160

From line 104, column 25; to line 104, column 160
```html
<a href="#" class="nav-link dropdown-toggle " id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
```

### Solución
En [`navbar.html`](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2022/Proyectos/grupo20/-/blob/main/admin/src/web/templates/super_templates/navbar/navbar.html), eliminar la ID
```html
<a href="#" class="nav-link dropdown-toggle {{ group.mark_active(request.path) }}" role="button" data-bs-toggle="dropdown" aria-expanded="false">
    {{ group.display_name }}
</a>
```

## Error: Attribute `charset` not allowed on element `meta` at this point.
From line 244, column 9; to line 244, column 30
```html
<meta charset="utf-8">
```

Salieron otros errores relacionados a éste, que preferí omitirlos

### Solución
Mover esa línea al nuevo archivo `pdf_list.html`
```html
<meta charset="utf-8">

{% import "list_only.html" %}
```

En [`__init__.py`](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2022/Proyectos/grupo20/-/blob/main/admin/src/web/templates/super_templates/lists/__init__.py), agregar parámetro `template_path` a `render_list()` y crear función `render_pdf_list()`
```python
def render_list(columns=[], row_buttons=[], items=[], template_path="super_templates/lists/list_only.html"):
    return render_template(
        template_path,
        columns=columns,
        row_buttons=to_button_group(row_buttons),
        items=items
    )
```
```python
def render_pdf_list(columns=[], items=[]):
    return render_list(
        columns=columns,
        items=items,
        template_path="super_templates/lists/pdf_list.html",
    )
```

En [`exporter_pdf.py`](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2022/Proyectos/grupo20/-/blob/main/admin/src/core/business/exporters/exporter_pdf.py), llamar a esa función
```python
def export_list(columns=[], items=[]):
    html = render_pdf_list(columns=columns, items=items)
    css = ['public/css/pdf_list.css']
    
    return pdfkit.from_string(html, css=css)
```

## Error: The element `h3` must not appear as a descendant of the `th` element.
From line 249, column 21; to line 249, column 24

From line 253, column 21; to line 253, column 24

From line 257, column 21; to line 257, column 24

From line 261, column 21; to line 261, column 24

From line 277, column 21; to line 277, column 24
```html
<h3>Nombre</h3>
```

### Solución
En [`list_only.html`](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2022/Proyectos/grupo20/-/blob/main/admin/src/web/templates/super_templates/lists/list_only.html), en cada cabecera de columna de la tabla, reemplazar uso de elementos `<h3>` por clase `h3` de Bootstrap
```html
<th scope="col" class="text-center h3">
    {{ column.display_name }}
</th>
```
```html
{% if ns.show_actions %}
    <th scope="col" class="text-center h3">
        Acciones
    </th>
{% endif %}
```