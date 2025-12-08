# Integración en WordPress: Sigue Tu Estrella

Hemos creado un **Plugin de WordPress a medida** (`SigueTuEstrella Core`) que conecta tu diseño "magistral" con la potencia del motor Python.

## Arquitectura Híbrida (Innovadora)

Para lograr lo mejor de ambos mundos (SEO/CMS de WordPress + Potencia de Python/IA), usamos una arquitectura desacoplada:

1.  **Frontend (WordPress)**: Maneja el diseño, SEO, usuarios y contenido.
2.  **Backend (Python API)**: Realiza los cálculos matemáticos complejos y genera los gráficos SVG.

## Instrucciones de Instalación

### 1. El Backend (Python)
Este debe estar ejecutándose para que la calculadora funcione.

**Opción A: Local (Para desarrollo)**
1.  Asegúrate de que `app.py` se está ejecutando (`python app.py`).
2.  La API estará en `http://localhost:5000/api/calculate`.

**Opción B: Producción (Render/Heroku/VPS)**
1.  Despliega el código Python (usando el `Dockerfile` incluido).
2.  Obtén la URL pública (ej: `https://api.siguetuestrella.com`).
3.  **IMPORTANTE**: Edita el archivo del plugin `sigue-tu-estrella-core.php` y actualiza la línea:
    ```php
    'apiUrl' => 'https://api.siguetuestrella.com/api/calculate'
    ```

### 2. El Plugin (WordPress)

1.  Ve a la carpeta `wordpress-plugin` de este proyecto.
2.  Comprime la carpeta `sigue-tu-estrella-core` en un archivo `.zip`.
3.  En tu panel de WordPress, ve a **Plugins > Añadir nuevo > Subir plugin**.
4.  Sube el archivo `.zip` y actívalo.

### 3. Uso

Simplemente coloca este shortcode en cualquier página o entrada donde quieras que aparezca la calculadora:

```
[sigue_tu_estrella_app]
```

El plugin cargará automáticamente:
- El diseño "Magistral" (CSS ultramoderno).
- El formulario interactivo.
- La conexión AJAX con tu motor Python.

## Ventajas de este enfoque

- **SEO Superior**: El contenido se renderiza en tu dominio principal, no en un iframe.
- **Velocidad**: WordPress sirve el HTML estático rápido, y Python calcula los datos pesados en segundo plano.
- **Diseño Unificado**: Los estilos CSS están dentro de tu WordPress, asegurando coherencia visual total.
