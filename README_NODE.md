# Simulación Numérica - Plataforma de Métodos

Plataforma web integrada con Django backend y Node.js frontend server para cálculos matemáticos y métodos numéricos.

## 📋 Requisitos

- **Node.js** (v14 o superior)
- **Python** (v3.8 o superior)
- **Django** y dependencias del backend

## 🚀 Instalación y Ejecución

### 1. Backend Django (Django API)

```bash
# Navega a la carpeta del backend
cd backend/django_api

# Instala las dependencias de Python
pip install -r requirements.txt

# Aplica las migraciones
python manage.py migrate

# Inicia el servidor Django
python manage.py runserver
```

El backend estará disponible en `http://localhost:8000`

### 2. Frontend Node.js Server

```bash
# Navega a la raíz del proyecto
cd .../Simulaci-n_Proyecto_Final

# Instala las dependencias de Node.js
npm install

# Inicia el servidor Node.js
npm start
```

O para desarrollo con reinicio automático:
```bash
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

## 📁 Estructura del Proyecto

```
Simulaci-n_Proyecto_Final/
├── server.js                    # Servidor Express Node.js
├── package.json                 # Dependencias Node.js
├── .env                        # Variables de configuración
├── .gitignore                  # Archivos ignorados por Git
├── frontend/                   # Archivos estáticos del frontend
│   ├── index.html
│   ├── css/
│   │   ├── style.css
│   │   └── resultados.css      # Estilos para resultados
│   ├── js/
│   │   ├── api-client.js       # Cliente API y renderizador
│   │   └── ... (otros scripts)
│   ├── pages/
│   │   ├── biseccion.html
│   │   ├── newton.html
│   │   └── ... (otras páginas)
│   └── assets/
└── backend/
    └── django_api/             # API Django
        ├── config/
        ├── apps/
        │   └── calculadora/
        └── ... (estructura Django)
```

## 🔧 Configuración

### Variables de Entorno (.env)

```env
PORT=3000
DJANGO_API_URL=http://localhost:8000/api
```

## 📡 API Endpoints

### Métodos Iterativos

#### Bisección
```
POST /api/biseccion
Body: {
  "ecuacion": "x**2 - 2",
  "a": 0,
  "b": 2,
  "tolerancia": 0.0001
}
```

#### Newton-Raphson
```
POST /api/newton
Body: {
  "ecuacion": "x**2 - 2",
  "x0": 1,
  "tolerancia": 0.0001,
  "max_iteraciones": 100
}
```

#### Newton para Sistemas
```
POST /api/newton-sistemas
Body: {
  "ecuaciones": ["x**2 + y**2 - 1", "x - y"],
  "valores_iniciales": [0.5, 0.5],
  "tolerancia": 0.0001
}
```

### Métodos de Aproximación

#### Polinomios de Taylor
```
POST /api/taylor
Body: {
  "funcion": "sin(x)",
  "punto_desarrollo": 0,
  "grado": 5,
  "intervalo_inicio": -1,
  "intervalo_fin": 1
}
```

#### Lagrange
```
POST /api/lagrange
Body: {
  "puntos": [
    {"x": 0, "y": 1},
    {"x": 1, "y": 2},
    {"x": 2, "y": 5}
  ]
}
```

#### Diferencias Divididas
```
POST /api/diferencias-divididas
Body: {
  "puntos": [
    {"x": 0, "y": 1},
    {"x": 1, "y": 2},
    {"x": 2, "y": 5}
  ]
}
```

#### Mínimos Cuadrados
```
POST /api/minimos-cuadrados
Body: {
  "puntos": [
    {"x": 0, "y": 1},
    {"x": 1, "y": 2},
    {"x": 2, "y": 5}
  ],
  "grado": 2
}
```

### Métodos de Conversión

#### Cambio de Base
```
POST /api/cambio-base
Body: {
  "numero": "101010",
  "base_origen": 2,
  "base_destino": 10
}
```

## 📊 Respuesta de API

Todos los endpoints retornan una estructura JSON:

```json
{
  "success": true,
  "data": {
    "raiz": 1.414213562373095,
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

## 🎨 Visualización de Resultados

Los resultados se muestran en un layout de dos columnas:

**Columna Izquierda (Tabla):**
- Tabla con todas las iteraciones
- Columnas dinámicas según el método
- Headers sticky para fácil referencia

**Columna Derecha (Gráfica):**
- Imagen en base64 del gráfico
- Renderizada automáticamente
- Responsive para dispositivos móviles

**Header:**
- Ecuación o polinomio calculado
- Resultado final (raíz, valor, etc.)
- Información del método utilizado

## 🔌 Cliente JavaScript

### Uso del APIClient

```javascript
// Llamar a bisección
const resultado = await APIClient.biseccion(
  "x**2 - 2",
  0,
  2,
  0.0001
);

// Renderizar resultados
ResultadosRenderer.renderMetodoIterativo(resultado.data, 'biseccion');
```

### Manejo de Errores

```javascript
try {
  Utils.mostrarCargando();
  const resultado = await APIClient.biseccion(...);
  ResultadosRenderer.renderMetodoIterativo(resultado.data);
} catch (error) {
  ResultadosRenderer.mostrarError(error.message);
}
```

## ✅ Checklist de Funcionalidad

- [x] Servidor Node.js con Express
- [x] Rutas API proxy hacia Django
- [x] Cliente JavaScript para consumir APIs
- [x] Renderización de tabla de iteraciones
- [x] Visualización de gráficas en base64
- [x] Estilos responsive
- [x] Manejo de errores
- [x] Validación de formularios
- [ ] Testing automatizado
- [ ] Deployment a producción

## 🐛 Solución de Problemas

### "Cannot GET /"
- Asegúrate que Node.js está corriendo: `npm start`
- Verifica que el puerto 3000 está disponible

### "Error de conexión a Django"
- Verifica que Django está corriendo: `python manage.py runserver`
- Confirma que `DJANGO_API_URL` en `.env` es correcta

### Gráficas no se muestran
- Verifica que las imágenes en base64 se retornan desde Django
- Revisa la consola del navegador para errores

### CORS errors
- Asegúrate que Django tiene CORS habilitado
- Verifica las configuraciones de CORS en Django

## 📚 Recursos

- [Express Documentation](https://expressjs.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 👨‍💻 Desarrollo

Para continuar con el desarrollo:

1. Edita los archivos en `frontend/` para cambios de interfaz
2. Edita `server.js` para agregar nuevas rutas
3. Reinicia Node.js para ver los cambios: `npm start`

## 📝 Notas Importantes

- El `package-lock.json` está en `.gitignore` como se especificó
- Todos los cálculos se hacen en el backend Django
- Node.js solo sirve como intermediario y servidor estático
- Las gráficas se generan en Python/Matplotlib en Django

¡Listo para usar! 🎉
