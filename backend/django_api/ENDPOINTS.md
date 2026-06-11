# 📚 API REST - Endpoints Completos

## 🔗 URL Base
```
http://localhost:8000/api
```

---

## 📖 Documentación Interactiva
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **Schema OpenAPI**: `http://localhost:8000/api/schema/`

---

## ✅ Endpoints Disponibles

### 1️⃣ **Raíz API (GET)**
```
GET /api/
```
Lista todos los endpoints disponibles.

---

### 2️⃣ **Método de Bisección (POST)**
```
POST /api/calculos/biseccion/
```
**Parámetros:**
```json
{
  "expresion": "x**2 - 2",
  "a_inicial": 0,
  "b_inicial": 2,
  "tolerancia": 0.0001,
  "max_iteraciones": 100
}
```

**Respuesta:**
```json
{
  "raiz": 1.414213562373095,
  "iteraciones": [
    {"iter": 1, "a": 0, "b": 2, "p_n": 1, "f_p_n": -1, "error": null},
    ...
  ],
  "grafica_png": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "estado": "exito"
}
```

---

### 3️⃣ **Método de Newton-Raphson (POST)**
```
POST /api/calculos/newton-raphson/
```
**Parámetros:**
```json
{
  "expresion": "x**3 - 2*x - 5",
  "x_inicial": 2,
  "tolerancia": 0.0001,
  "max_iteraciones": 100
}
```

**Respuesta:**
```json
{
  "raiz": 2.0945514815423265,
  "iteraciones": [...],
  "grafica_png": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "estado": "exito"
}
```

---

### 4️⃣ **Cambios de Base (POST)**
```
POST /api/calculos/cambios-base/
```
**Parámetros:**
```json
{
  "numero": "1011.101",
  "base_origen": 2,
  "base_destino": 10
}
```

**Respuesta:**
```json
{
  "numero_original": "1011.101",
  "base_origen": 2,
  "numero_convertido": "11.625",
  "base_destino": 10,
  "historial": [...]
}
```

---

### 5️⃣ **Cálculo de Errores (POST)**
```
POST /api/calculos/error/
```
**Parámetros:**
```json
{
  "valor_verdadero": 3.141592653589793,
  "valor_aproximado": 3.14
}
```

**Respuesta:**
```json
{
  "valor_verdadero": 3.141592653589793,
  "valor_aproximado": 3.14,
  "error_absoluto": 0.001592653589793,
  "error_relativo": 0.000507, 
  "error_porcentual": 0.0507
}
```

---

### 6️⃣ **Cálculo de Derivadas (POST)**
```
POST /api/calculos/derivada/
```
**Parámetros:**
```json
{
  "expresion": "x**3 + 2*x**2 - 5*x + 3",
  "punto_evaluacion": 2
}
```

**Respuesta:**
```json
{
  "expresion": "x**3 + 2*x**2 - 5*x + 3",
  "punto_evaluacion": 2,
  "derivada_valor": 11,
  "derivada_expresion": "3*x**2 + 4*x - 5"
}
```

---

### 7️⃣ **Polinomio de Taylor (POST)**
```
POST /api/calculos/polinomio-taylor/
```
**Parámetros:**
```json
{
  "expresion": "exp(x)",
  "centro": 0,
  "grado": 4,
  "punto_evaluacion": 1
}
```

**Respuesta:**
```json
{
  "centro": 0,
  "grado": 4,
  "punto_evaluacion": 1,
  "valor_exacto": 2.718281828,
  "valor_taylor": 2.708333333,
  "error": 0.009948495,
  "polinomio": "1 + x + x**2/2 + x**3/6 + x**4/24",
  "historial": [...],
  "grafica_png": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "estado": "exito"
}
```

---

### 8️⃣ **Interpolación de Lagrange (POST)**
```
POST /api/calculos/interpolacion-lagrange/
```
**Parámetros:**
```json
{
  "puntos_x": [1, 2, 3, 4],
  "puntos_y": [1, 4, 9, 16],
  "x_evaluacion": 2.5
}
```

**Respuesta:**
```json
{
  "puntos_x": [1, 2, 3, 4],
  "puntos_y": [1, 4, 9, 16],
  "x_evaluacion": 2.5,
  "y_interpolado": 6.25,
  "grado_polinomio": 3,
  "historial": [...],
  "grafica_png": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "estado": "exito"
}
```

---

### 9️⃣ **Diferencias Divididas de Newton (POST)**
```
POST /api/calculos/diferencias-divididas/
```
**Parámetros:**
```json
{
  "puntos_x": [1, 2, 3, 4],
  "puntos_y": [1, 4, 9, 16],
  "x_evaluacion": 2.5
}
```

**Respuesta:**
```json
{
  "puntos_x": [1, 2, 3, 4],
  "puntos_y": [1, 4, 9, 16],
  "x_evaluacion": 2.5,
  "y_interpolado": 6.25,
  "grado_polinomio": 3,
  "tabla_diferencias": [...],
  "historial": [...],
  "grafica_png": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "estado": "exito"
}
```

---

### 🔟 **Ajuste de Curvas (POST)**
```
POST /api/calculos/ajuste-curvas/
```
**Parámetros:**
```json
{
  "puntos_x": [1, 2, 3, 4, 5],
  "puntos_y": [2.1, 3.9, 6.2, 7.8, 10.1],
  "grado": 1,
  "tipo_ajuste": "polinomio"
}
```

**Tipos de ajuste:**
- `polinomio` (default)
- `exponencial`
- `logaritmica`

**Respuesta:**
```json
{
  "tipo_ajuste": "polinomio",
  "grado": 1,
  "puntos_x": [1, 2, 3, 4, 5],
  "puntos_y": [2.1, 3.9, 6.2, 7.8, 10.1],
  "coeficientes": [1.98, 0.12],
  "ecuacion": "Polinomio de grado 1",
  "r_cuadrado": 0.99842,
  "error_cuadratico_medio": 0.1234,
  "desviacion_estandar": 0.0987,
  "historial": [...],
  "grafica_png": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "estado": "exito"
}
```

---

### 1️⃣1️⃣ **Exportar a Excel (POST)**
```
POST /api/exportar/excel/
```
**Parámetros:**
```json
{
  "titulo": "Reporte Bisección",
  "datos": [
    {"iter": 1, "a": 0, "b": 2, "p_n": 1, "f_p_n": -1},
    {"iter": 2, "a": 1, "b": 2, "p_n": 1.5, "f_p_n": 0.25},
    ...
  ]
}
```

**Respuesta:**
```json
{
  "titulo": "Reporte Bisección",
  "filas": 10,
  "columnas": ["iter", "a", "b", "p_n", "f_p_n"],
  "excel_base64": "UEsDBBQAAAAIAJn...",
  "nombre_archivo": "Reporte_Bisección.xlsx"
}
```

---

### 1️⃣2️⃣ **Exportar Excel Múltiple (POST)**
```
POST /api/exportar/excel-multiplo/
```
**Parámetros:**
```json
{
  "hojas": [
    {
      "nombre": "Iteraciones",
      "datos": [
        {"iter": 1, "x": 1.5, "f_x": 0.1},
        ...
      ]
    },
    {
      "nombre": "Estadísticas",
      "datos": [
        {"metodo": "Newton", "raiz": 1.41421, "error": 0.0001},
        ...
      ]
    }
  ]
}
```

**Respuesta:**
```json
{
  "cantidad_hojas": 2,
  "hojas": ["Iteraciones", "Estadísticas"],
  "excel_base64": "UEsDBBQAAAAIAJn...",
  "nombre_archivo": "Reporte_Completo.xlsx"
}
```

---

## 🖼️ Manejo de Imágenes (base64)

Todos los endpoints que generan gráficas retornan el campo `grafica_png` con la imagen en formato base64.

**Para mostrar en HTML:**
```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA..." alt="Gráfica">
```

**Para descargar en JavaScript:**
```javascript
const link = document.createElement('a');
link.href = 'data:image/png;base64,' + respuesta.grafica_png;
link.download = 'grafica.png';
link.click();
```

---

## 📄 Manejo de Excel (base64)

Todos los endpoints de exportación retornan `excel_base64` con el archivo Excel en base64.

**Para descargar en JavaScript:**
```javascript
const binaryString = atob(respuesta.excel_base64);
const bytes = new Uint8Array(binaryString.length);
for (let i = 0; i < binaryString.length; i++) {
  bytes[i] = binaryString.charCodeAt(i);
}
const blob = new Blob([bytes], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
const url = window.URL.createObjectURL(blob);
const link = document.createElement('a');
link.href = url;
link.download = respuesta.nombre_archivo;
link.click();
```

---

## ⚠️ Códigos de Error

| Código | Significado |
|--------|------------|
| 200 | Éxito |
| 400 | Parámetro inválido |
| 500 | Error del servidor |

---

## 🧮 Notas Importantes

- **Expresiones**: Usa `**` para potencia (no `^`)
  - ✅ `x**2 + 3*x + 2`
  - ❌ `x^2 + 3*x + 2`

- **Funciones soportadas**: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, etc.

- **Base64**: Las imágenes y Excel se codifican en base64 sin almacenamiento en BD

- **Gráficas**: Se generan automáticamente para todos los métodos de búsqueda de raíces

---

## 🚀 Ejemplo Completo (JavaScript)

```javascript
// 1. Calcular bisección
const response = await fetch('http://localhost:8000/api/calculos/biseccion/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    expresion: 'x**2 - 2',
    a_inicial: 0,
    b_inicial: 2
  })
});

const resultado = await response.json();

// 2. Mostrar gráfica
const img = document.createElement('img');
img.src = `data:image/png;base64,${resultado.grafica_png}`;
document.body.appendChild(img);

// 3. Exportar a Excel
const exportResponse = await fetch('http://localhost:8000/api/exportar/excel/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    titulo: 'Bisección',
    datos: resultado.iteraciones
  })
});

const exportResult = await exportResponse.json();

// 4. Descargar Excel
const binaryString = atob(exportResult.excel_base64);
const bytes = new Uint8Array(binaryString.length);
for (let i = 0; i < binaryString.length; i++) {
  bytes[i] = binaryString.charCodeAt(i);
}
const blob = new Blob([bytes], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
const url = window.URL.createObjectURL(blob);
const link = document.createElement('a');
link.href = url;
link.download = exportResult.nombre_archivo;
link.click();
```

---

