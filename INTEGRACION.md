# Guía de Integración - Frontend con Node.js

Esta guía te muestra cómo integrar el nuevo cliente API con tus páginas HTML existentes.

## 📝 Pasos de Integración

### 1. Agregar Referencias a los Scripts

En el `<head>` de cada página HTML (antes de cerrar `</head>`):

```html
<!-- API Client -->
<script src="/js/api-client.js"></script>

<!-- Form Handlers -->
<script src="/js/form-handlers.js"></script>

<!-- Estilos de Resultados -->
<link rel="stylesheet" href="/css/resultados.css">
```

### 2. Estructura Base del Formulario

Cada formulario debe tener este estructura mínima:

```html
<form id="forma-[nombre-metodo]">
  <!-- Tus inputs aquí -->
  <button type="submit">Calcular</button>
</form>

<!-- Contenedor para resultados -->
<div id="resultados-container"></div>
```

## 🔧 Ejemplos Específicos

### Ejemplo 1: Bisección

```html
<!DOCTYPE html>
<html>
<head>
  <title>Bisección</title>
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/resultados.css">
  <script src="/js/api-client.js"></script>
  <script src="/js/form-handlers.js"></script>
</head>
<body>
  <div class="contenedor">
    <h1>Método de Bisección</h1>
    
    <form id="forma-biseccion">
      <div class="input-group">
        <label>Ecuación (ej: x**2 - 2)</label>
        <input type="text" id="ecuacion" required>
      </div>
      
      <div class="input-group">
        <label>a:</label>
        <input type="number" id="a" step="0.01" required>
      </div>
      
      <div class="input-group">
        <label>b:</label>
        <input type="number" id="b" step="0.01" required>
      </div>
      
      <div class="input-group">
        <label>Tolerancia:</label>
        <input type="number" id="tolerancia" step="0.0001" value="0.0001" required>
      </div>
      
      <button type="submit">Calcular</button>
    </form>
    
    <!-- Contenedor de resultados -->
    <div id="resultados-container"></div>
  </div>
</body>
</html>
```

### Ejemplo 2: Lagrange (con tabla de puntos)

```html
<!DOCTYPE html>
<html>
<head>
  <title>Interpolación de Lagrange</title>
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/resultados.css">
  <script src="/js/api-client.js"></script>
  <script src="/js/form-handlers.js"></script>
</head>
<body>
  <div class="contenedor">
    <h1>Interpolación de Lagrange</h1>
    
    <form id="forma-lagrange">
      <h3>Ingresa los puntos</h3>
      
      <table id="puntos-table">
        <thead>
          <tr>
            <th>x</th>
            <th>y</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><input type="number" class="punto-input" step="0.01"></td>
            <td><input type="number" class="punto-input" step="0.01"></td>
          </tr>
          <tr>
            <td><input type="number" class="punto-input" step="0.01"></td>
            <td><input type="number" class="punto-input" step="0.01"></td>
          </tr>
        </tbody>
      </table>
      
      <button type="submit">Calcular Interpolación</button>
    </form>
    
    <!-- Contenedor de resultados -->
    <div id="resultados-container"></div>
  </div>
</body>
</html>
```

### Ejemplo 3: Newton-Raphson

```html
<!DOCTYPE html>
<html>
<head>
  <title>Newton-Raphson</title>
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/resultados.css">
  <script src="/js/api-client.js"></script>
  <script src="/js/form-handlers.js"></script>
</head>
<body>
  <div class="contenedor">
    <h1>Método de Newton-Raphson</h1>
    
    <form id="forma-newton">
      <div class="input-group">
        <label>Ecuación (ej: x**2 - 2)</label>
        <input type="text" id="ecuacion" required>
      </div>
      
      <div class="input-group">
        <label>Valor inicial (x₀)</label>
        <input type="number" id="x0" step="0.01" required>
      </div>
      
      <div class="input-group">
        <label>Tolerancia</label>
        <input type="number" id="tolerancia" step="0.0001" value="0.0001" required>
      </div>
      
      <div class="input-group">
        <label>Iteraciones máximas</label>
        <input type="number" id="max_iteraciones" value="100">
      </div>
      
      <button type="submit">Calcular</button>
    </form>
    
    <!-- Contenedor de resultados -->
    <div id="resultados-container"></div>
  </div>
</body>
</html>
```

## 🎨 Personalización de Estilos

Los estilos de resultados están en `/css/resultados.css`. Puedes personalizarlos modificando:

```css
/* Cambiar colores principales */
.resultado-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Cambiar tamaño de tablas */
.tabla-iteraciones {
  font-size: 0.9rem;
}

/* Cambiar tamaño de gráficas */
.grafica-imagen {
  max-height: 500px;
}
```

## 🔌 Crear Manejadores Personalizados

Si necesitas personalizar el comportamiento para una página específica:

```html
<script>
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('forma-personalizada');
  
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      try {
        // Tu lógica aquí
        const valor = document.getElementById('mi-input').value;
        
        Utils.mostrarCargando();
        
        // Llamada a API
        const resultado = await APIClient.biseccion(valor, 0, 2, 0.0001);
        
        // Renderizar
        ResultadosRenderer.renderMetodoIterativo(resultado.data);
        
      } catch (error) {
        ResultadosRenderer.mostrarError(error.message);
      }
    });
  }
});
</script>
```

## ⚠️ Validación de Datos

Las utilidades validan automáticamente los campos requeridos:

```javascript
// Esto lanzará error si falta ecuacion, a o b
Utils.validarFormulario(
  { ecuacion, a, b },
  ['ecuacion', 'a', 'b']
);
```

## 🚨 Manejo de Errores

Los errores se muestran automáticamente:

```javascript
try {
  const resultado = await APIClient.biseccion(...);
  if (resultado.success) {
    ResultadosRenderer.renderMetodoIterativo(resultado.data);
  } else {
    ResultadosRenderer.mostrarError(resultado.error);
  }
} catch (error) {
  ResultadosRenderer.mostrarError(error.message);
}
```

## 📊 Estructura de Respuesta

Todas las respuestas tienen este formato:

```json
{
  "success": true,
  "data": {
    "raiz": 1.414213562373095,
    "ecuacion": "x**2 - 2",
    "iteraciones": [
      {
        "iter": 1,
        "a": 0,
        "b": 2,
        "p_n": 1,
        "f_p_n": -1,
        "error": null
      }
    ],
    "estado": "exito",
    "grafica_png": "iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

## 🔄 Ciclo de Ejecución

1. Usuario llena formulario
2. Usuario presiona "Calcular" / "Enviar"
3. Se validan datos con `Utils.validarFormulario()`
4. Se muestra "Calculando..." con `Utils.mostrarCargando()`
5. Se llama a `APIClient.[metodo]()`
6. Node.js hace proxy a Django
7. Django calcula y retorna resultado
8. Se renderiza con `ResultadosRenderer.render[Tipo]()`
9. Se muestra tabla + gráfica + resultados

## 📱 Responsive Design

Todos los estilos son responsive. En móviles:
- Las dos columnas se apilan verticalmente
- La tabla se hace más pequeña
- Las gráficas se adaptan

## 🎯 ID requeridos en Formularios

Cada formulario debe tener estos IDs para que funcione:

| Método | ID Formulario |
|--------|--------------|
| Bisección | `forma-biseccion` |
| Newton | `forma-newton` |
| Taylor | `forma-taylor` |
| Lagrange | `forma-lagrange` |
| Cambio Base | `forma-cambio-base` |
| Diferencias Divididas | `forma-diferencias-divididas` |
| Mínimos Cuadrados | `forma-minimos-cuadrados` |
| Newton Sistemas | `forma-newton-sistemas` |

## ✅ Checklist de Integración

- [ ] Scripts `api-client.js` y `form-handlers.js` incluidos
- [ ] CSS `resultados.css` incluido
- [ ] Formulario tiene ID correcto
- [ ] Existe `<div id="resultados-container"></div>`
- [ ] Inputs tienen IDs correctos
- [ ] Botón tiene `type="submit"`
- [ ] Formulario tiene `<form>` wrapper

## 🆘 Solución de Problemas

### "Undefined variable"
- Verifica que `api-client.js` está cargado antes que el script que lo usa

### "No se muestra resultado"
- Comprueba que `resultados-container` existe en el HTML
- Abre DevTools (F12) y busca errores en la consola

### "API retorna error"
- Verifica que Node.js está corriendo: `npm start`
- Verifica que Django está corriendo en `http://localhost:8000`
- Revisa la variable de entorno `DJANGO_API_URL` en `.env`

### "Los estilos no se ven"
- Asegúrate que `resultados.css` está en `/frontend/css/`
- Limpia la caché del navegador (Ctrl+Shift+Del)

¡Listo! 🎉
