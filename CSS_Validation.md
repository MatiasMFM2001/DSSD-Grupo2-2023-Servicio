# Validación CSS

Al ejecutar el [validador](https://jigsaw.w3.org/css-validator) con [todos los archivos CSS](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2022/Proyectos/grupo20/-/tree/main/admin/public/css), ninguno dio error

Al validar [`style.css`](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2022/Proyectos/grupo20/-/blob/main/admin/public/css/style.css) mediante entrada directa, dio una advertencia en la línea 1
> Las hojas de estilo importadas no se comprueban en los modos de entrada directa y carga de archivo

```css
@import url('https://fonts.googleapis.com/css?family=Montserrat:400,600,700');
```

Pero al validar el CSS de ese link, tampoco hubieron errores