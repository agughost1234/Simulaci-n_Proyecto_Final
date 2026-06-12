/**
 * API Client para consumir endpoints Node.js
 * Maneja todas las llamadas a la API de métodos numéricos
 */

const API_BASE_URL = 'http://localhost:3000/api';

/**
 * Clase para gestionar llamadas a API
 */
class APIClient {
  static async post(endpoint, data) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en API:', error);
      throw error;
    }
  }

  static async biseccion(expresion, a_inicial, b_inicial, tolerancia = 0.0001, max_iteraciones = 100) {
    return this.post('/calculos/biseccion', { expresion, a_inicial, b_inicial, tolerancia, max_iteraciones });
  }

  static async newton(expresion, x_inicial, tolerancia = 0.0001, max_iteraciones = 100) {
    return this.post('/calculos/newton', { expresion, x_inicial, tolerancia, max_iteraciones });
  }

  static async taylor(expresion, centro, grado, punto_evaluacion) {
    return this.post('/calculos/polinomio-taylor/', { 
      expresion, 
      centro, 
      grado, 
      punto_evaluacion
    });
  }

  static async cambioBase(numero, base_origen, base_destino, max_iteraciones = 50) {
    return this.post('/calculos/cambio-base', { numero, base_origen, base_destino, max_iteraciones });
  }

  static async lagrange(puntos, x_evaluacion) {
    return this.post('/calculos/lagrange', { puntos, x_evaluacion });
  }

  static async diferenciasDivididas(puntos, x_evaluacion) {
    return this.post('/calculos/diferencias-divididas', { puntos, x_evaluacion });
  }

  static async minimoscuadrados(puntos, grado = 1, tipo_ajuste = 'polinomio') {
    return this.post('/calculos/minimos-cuadrados', { puntos, grado, tipo_ajuste });
  }

  static async newtonSistemas(ecuaciones, valores_iniciales, tolerancia, max_iteraciones = 100) {
    return this.post('/calculos/newton-sistemas/', { 
      ecuaciones, 
      valores_iniciales, 
      tolerancia, 
      max_iteraciones 
    });
  }
}

/**
 * Clase para renderizar resultados
 */
class ResultadosRenderer {
  /**
   * Renderiza resultados de método iterativo (bisección, newton, etc)
   */
  static renderMetodoIterativo(data, tipo = 'biseccion') {
    const container = document.getElementById('resultados-container');
    if (!container) return;

    const { raiz, iteraciones, estado, grafica_png, expresion } = data;

    // Header con ecuación y raíz
    const header = document.createElement('div');
    header.className = 'resultado-header';
    header.innerHTML = `
      <div class="ecuacion-raiz">
        <div class="ecuacion-box">
          <p class="label">Ecuación</p>
          <p class="valor">${expresion || data.ecuacion || 'f(x) = 0'}</p>
        </div>
        <div class="raiz-box">
          <p class="label">Raíz Calculada</p>
          <p class="valor">${raiz.toFixed(10)}</p>
        </div>
      </div>
    `;

    // Contenedor principal: tabla + gráfica
    const mainContainer = document.createElement('div');
    mainContainer.className = 'resultado-main';

    // Tabla de iteraciones
    const tablaContainer = document.createElement('div');
    tablaContainer.className = 'tabla-container';
    
    const tabla = this.crearTablaIteraciones(iteraciones, tipo);
    tablaContainer.appendChild(tabla);

    // Gráfica
    const graficaContainer = document.createElement('div');
    graficaContainer.className = 'grafica-container';
    
    if (grafica_png) {
      const img = document.createElement('img');
      img.src = `data:image/png;base64,${grafica_png}`;
      img.alt = 'Gráfica del método';
      img.className = 'grafica-imagen';
      graficaContainer.appendChild(img);
    } else {
      graficaContainer.innerHTML = '<p class="sin-grafica">Sin gráfica disponible</p>';
    }

    // Agregar tabla y gráfica al contenedor principal
    mainContainer.appendChild(tablaContainer);
    mainContainer.appendChild(graficaContainer);

    // Limpiar y agregar al DOM
    container.innerHTML = '';
    container.appendChild(header);
    container.appendChild(mainContainer);

    // Mostrar estado
    const statusMsg = document.createElement('p');
    statusMsg.className = 'estado-mensaje';
    statusMsg.textContent = `Estado: ${estado || 'Éxito'}`;
    container.appendChild(statusMsg);
  }

  /**
   * Crea tabla de iteraciones según el tipo de método
   */
  static crearTablaIteraciones(iteraciones, tipo) {
    const tabla = document.createElement('table');
    tabla.className = 'tabla-iteraciones';

    // Headers según el tipo de método
    let headers = [];
    switch(tipo) {
      case 'biseccion':
        headers = ['Iter', 'a', 'b', 'p_n', 'f(p_n)', 'Error'];
        break;
      case 'newton':
        headers = ['Iter', 'x_n', 'f(x_n)', 'f\'(x_n)', 'Error'];
        break;
      default:
        headers = ['Iter', 'Valor', 'Error'];
    }

    // Crear thead
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    headers.forEach(h => {
      const th = document.createElement('th');
      th.textContent = h;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    tabla.appendChild(thead);

    // Crear tbody
    const tbody = document.createElement('tbody');
    iteraciones.forEach((iter, idx) => {
      const row = document.createElement('tr');
      
      switch(tipo) {
        case 'biseccion':
          row.innerHTML = `
            <td>${iter.iter}</td>
            <td>${parseFloat(iter.a).toFixed(6)}</td>
            <td>${parseFloat(iter.b).toFixed(6)}</td>
            <td>${parseFloat(iter.p_n).toFixed(6)}</td>
            <td>${parseFloat(iter.f_p_n).toFixed(6)}</td>
            <td>${iter.error ? parseFloat(iter.error).toFixed(8) : '-'}</td>
          `;
          break;
        case 'newton':
          row.innerHTML = `
            <td>${iter.iter}</td>
            <td>${parseFloat(iter.x_n).toFixed(6)}</td>
            <td>${parseFloat(iter.f_x_n || 0).toFixed(6)}</td>
            <td>${parseFloat(iter.f_prime_x_n || 0).toFixed(6)}</td>
            <td>${iter.error ? parseFloat(iter.error).toFixed(8) : '-'}</td>
          `;
          break;
        default:
          row.innerHTML = `
            <td>${idx + 1}</td>
            <td>${Object.values(iter).join(', ')}</td>
            <td>-</td>
          `;
      }
      
      tbody.appendChild(row);
    });
    tabla.appendChild(tbody);

    return tabla;
  }

  /**
   * Renderiza resultados de interpolación
   */
  static renderInterpolacion(data, tipo = 'lagrange') {
    const container = document.getElementById('resultados-container');
    if (!container) return;

    const { polinomio, puntos, grafica_png } = data;

    const header = document.createElement('div');
    header.className = 'resultado-header';
    header.innerHTML = `
      <div class="ecuacion-raiz">
        <div class="ecuacion-box">
          <p class="label">Polinomio Interpolador</p>
          <p class="valor" style="word-wrap: break-word;">${polinomio || 'No disponible'}</p>
        </div>
      </div>
    `;

    const mainContainer = document.createElement('div');
    mainContainer.className = 'resultado-main';

    // Tabla de puntos
    if (puntos && puntos.length > 0) {
      const tablaContainer = document.createElement('div');
      tablaContainer.className = 'tabla-container';
      
      const tabla = document.createElement('table');
      tabla.className = 'tabla-iteraciones';
      tabla.innerHTML = `
        <thead>
          <tr>
            <th>x</th>
            <th>y</th>
          </tr>
        </thead>
        <tbody>
          ${puntos.map(p => `
            <tr>
              <td>${parseFloat(p.x).toFixed(6)}</td>
              <td>${parseFloat(p.y).toFixed(6)}</td>
            </tr>
          `).join('')}
        </tbody>
      `;
      tablaContainer.appendChild(tabla);
      mainContainer.appendChild(tablaContainer);
    }

    // Gráfica
    const graficaContainer = document.createElement('div');
    graficaContainer.className = 'grafica-container';
    
    if (grafica_png) {
      const img = document.createElement('img');
      img.src = `data:image/png;base64,${grafica_png}`;
      img.alt = 'Gráfica de interpolación';
      img.className = 'grafica-imagen';
      graficaContainer.appendChild(img);
    }

    mainContainer.appendChild(graficaContainer);

    container.innerHTML = '';
    container.appendChild(header);
    container.appendChild(mainContainer);
  }

  /**
   * Renderiza resultado simple (cambio de base, etc)
   */
  /**
   * Renderiza resultados de cambio de base con tabla de historial
   */
  static renderCambioBase(data) {
    const container = document.getElementById('resultados-container');
    if (!container) return;

    const { numero_convertido, numero_original, base_origen, base_destino, historial } = data;

    // Header
    const header = document.createElement('div');
    header.className = 'resultado-header';
    header.innerHTML = `
      <div class="cambio-base-header">
        <div class="conversion-box">
          <p class="label">Conversión</p>
          <p class="valor">${numero_original} (Base ${base_origen}) → ${numero_convertido} (Base ${base_destino})</p>
        </div>
      </div>
    `;

    // Tabla de historial
    const tablaContainer = document.createElement('div');
    tablaContainer.className = 'tabla-historial-container';

    const tabla = document.createElement('table');
    tabla.className = 'tabla-historial';

    // Encabezados
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const columnas = ['Fase', 'Operación', 'Resultado', 'Dígito Extraído'];
    
    columnas.forEach(col => {
      const th = document.createElement('th');
      th.textContent = col;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    tabla.appendChild(thead);

    // Cuerpo de la tabla
    const tbody = document.createElement('tbody');
    if (Array.isArray(historial)) {
      historial.forEach((fila, index) => {
        const tr = document.createElement('tr');
        columnas.forEach(col => {
          const td = document.createElement('td');
          const valor = fila[col];
          td.textContent = valor === null || valor === undefined ? '-' : valor;
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    }
    tabla.appendChild(tbody);

    tablaContainer.appendChild(tabla);

    container.innerHTML = '';
    container.appendChild(header);
    container.appendChild(tablaContainer);
  }

  static renderResultadoSimple(data, titulo) {
    const container = document.getElementById('resultados-container');
    if (!container) return;

    const resultado = document.createElement('div');
    resultado.className = 'resultado-simple';
    resultado.innerHTML = `
      <h3>${titulo}</h3>
      <div class="resultado-contenido">
        ${Object.entries(data).map(([key, value]) => `
          <p><strong>${key}:</strong> ${value}</p>
        `).join('')}
      </div>
    `;

    container.innerHTML = '';
    container.appendChild(resultado);
  }

  /**
   * Renderiza resultados de Newton para Sistemas
   */
  static renderNewtonSistemas(data) {
    const container = document.getElementById('resultados-container');
    if (!container) return;

    // Validar que data existe
    if (!data || typeof data !== 'object') {
      console.error('Datos inválidos para renderNewtonSistemas:', data);
      this.mostrarError('Error: Datos inválidos de la respuesta del servidor');
      return;
    }

    const solucion = data.solucion || [];
    const residuo = data.residuo || 0;
    const iteraciones = data.iteraciones || [];
    const estado = data.estado || 'desconocido';
    const grafica_png = data.grafica_png || null;

    console.log('Rendering Newton-Sistemas:', { solucion, residuo, iteraciones, estado });

    // Header con solución
    const header = document.createElement('div');
    header.className = 'resultado-header';
    
    const solutionStr = Array.isArray(solucion) 
      ? solucion.map((s, i) => `x${i} = ${parseFloat(s).toFixed(6)}`).join(', ')
      : solucion.toFixed(6);
    
    header.innerHTML = `
      <div class="ecuacion-raiz">
        <div class="ecuacion-box">
          <p class="label">Solución del Sistema</p>
          <p class="valor">[${solutionStr}]</p>
        </div>
        <div class="raiz-box">
          <p class="label">Residuo ||F(x)||</p>
          <p class="valor">${residuo.toFixed(10)}</p>
        </div>
      </div>
    `;

    // Tabla de iteraciones
    const mainContainer = document.createElement('div');
    mainContainer.className = 'resultado-main';

    const tablaContainer = document.createElement('div');
    tablaContainer.className = 'tabla-container';
    
    const tabla = document.createElement('table');
    tabla.className = 'tabla-iteraciones';

    // Encabezados
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    const encabezados = ['Iteración', 'Solución', 'Residuo', 'Error Relativo'];
    encabezados.forEach(enc => {
      const th = document.createElement('th');
      th.textContent = enc;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    tabla.appendChild(thead);

    // Cuerpo de la tabla
    const tbody = document.createElement('tbody');
    if (Array.isArray(iteraciones) && iteraciones.length > 0) {
      iteraciones.forEach((iter, idx) => {
        const tr = document.createElement('tr');
        
        const tdIter = document.createElement('td');
        tdIter.textContent = iter.iter !== undefined ? iter.iter : idx;
        tr.appendChild(tdIter);
        
        const tdSol = document.createElement('td');
        const solStr = Array.isArray(iter.solucion)
          ? iter.solucion.map(s => parseFloat(s).toFixed(4)).join(', ')
          : (iter.solucion !== undefined ? iter.solucion.toFixed(4) : '-');
        tdSol.textContent = `[${solStr}]`;
        tr.appendChild(tdSol);
        
        const tdRes = document.createElement('td');
        tdRes.textContent = iter.residuo !== undefined ? iter.residuo.toFixed(8) : '-';
        tr.appendChild(tdRes);
        
        const tdErr = document.createElement('td');
        tdErr.textContent = iter.error !== null && iter.error !== undefined ? iter.error.toFixed(8) : '-';
        tr.appendChild(tdErr);
        
        tbody.appendChild(tr);
      });
    }
    tabla.appendChild(tbody);
    tablaContainer.appendChild(tabla);

    // Gráfica
    const graficaContainer = document.createElement('div');
    graficaContainer.className = 'grafica-container';
    
    if (grafica_png) {
      const img = document.createElement('img');
      img.src = `data:image/png;base64,${grafica_png}`;
      img.alt = 'Gráfica de convergencia';
      img.className = 'grafica-imagen';
      graficaContainer.appendChild(img);
    } else {
      graficaContainer.innerHTML = '<p class="sin-grafica">Sin gráfica disponible</p>';
    }

    // Agregar tabla y gráfica al contenedor principal
    mainContainer.appendChild(tablaContainer);
    mainContainer.appendChild(graficaContainer);

    // Limpiar y agregar al DOM
    container.innerHTML = '';
    container.appendChild(header);
    container.appendChild(mainContainer);

    // Mostrar estado
    const statusMsg = document.createElement('p');
    statusMsg.className = 'estado-mensaje';
    statusMsg.textContent = `Estado: ${estado === 'exito' ? 'Convergencia alcanzada' : 'Máximo de iteraciones alcanzado'}`;
    container.appendChild(statusMsg);
  }

  /**
   * Renderiza resultados de Polinomios de Taylor
   */
  static renderTaylor(data) {
    const container = document.getElementById('resultados-container');
    if (!container) return;

    // Validar que data existe
    if (!data || typeof data !== 'object') {
      console.error('Datos inválidos para renderTaylor:', data);
      this.mostrarError('Error: Datos inválidos de la respuesta del servidor');
      return;
    }

    const aproximacion = data.aproximacion || 0;
    const historial = data.historial || [];
    const expresion = data.expresion || 'f(x) = desconocida';
    const grafica_png = data.grafica_png || null;

    console.log('Rendering Taylor:', { aproximacion, historial, expresion });
    console.log('Historial item 0:', historial[0]);

    // Header con aproximación
    const header = document.createElement('div');
    header.className = 'resultado-header';
    
    header.innerHTML = `
      <div class="ecuacion-raiz">
        <div class="ecuacion-box">
          <p class="label">Función Original</p>
          <p class="valor">${expresion}</p>
        </div>
        <div class="raiz-box">
          <p class="label">Aproximación Taylor</p>
          <p class="valor">${parseFloat(aproximacion).toFixed(10)}</p>
        </div>
      </div>
    `;

    // Tabla de historial de términos
    const mainContainer = document.createElement('div');
    mainContainer.className = 'resultado-main';

    const tablaContainer = document.createElement('div');
    tablaContainer.className = 'tabla-container';
    
    const tabla = document.createElement('table');
    tabla.className = 'tabla-iteraciones';

    // Encabezados
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    const encabezados = ['Orden k', 'Derivada en x0', 'Término k', 'Aproximación Acumulada'];
    encabezados.forEach(enc => {
      const th = document.createElement('th');
      th.textContent = enc;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    tabla.appendChild(thead);

    // Cuerpo de la tabla
    const tbody = document.createElement('tbody');
    if (Array.isArray(historial) && historial.length > 0) {
      historial.forEach((iter, idx) => {
        const tr = document.createElement('tr');
        
        const tdOrden = document.createElement('td');
        tdOrden.textContent = iter.orden_k !== undefined ? iter.orden_k : idx;
        tr.appendChild(tdOrden);
        
        const tdDerivada = document.createElement('td');
        const derivadaVal = iter.derivada_en_x0;
        tdDerivada.textContent = derivadaVal !== undefined && derivadaVal !== null ? parseFloat(derivadaVal).toFixed(6) : '-';
        tr.appendChild(tdDerivada);
        
        const tdTermino = document.createElement('td');
        const terminoVal = iter.termino_k;
        tdTermino.textContent = terminoVal !== undefined && terminoVal !== null ? parseFloat(terminoVal).toFixed(8) : '-';
        tr.appendChild(tdTermino);
        
        const tdAprox = document.createElement('td');
        const aproxVal = iter.aproximacion_acumulada;
        tdAprox.textContent = aproxVal !== undefined && aproxVal !== null ? parseFloat(aproxVal).toFixed(10) : '-';
        tr.appendChild(tdAprox);
        
        tbody.appendChild(tr);
      });
    }
    tabla.appendChild(tbody);
    tablaContainer.appendChild(tabla);

    // Gráfica
    const graficaContainer = document.createElement('div');
    graficaContainer.className = 'grafica-container';
    
    if (grafica_png) {
      const img = document.createElement('img');
      img.src = `data:image/png;base64,${grafica_png}`;
      img.alt = 'Gráfica de aproximación Taylor';
      img.className = 'grafica-imagen';
      graficaContainer.appendChild(img);
    } else {
      graficaContainer.innerHTML = '<p class="sin-grafica">Sin gráfica disponible</p>';
    }

    // Agregar tabla y gráfica al contenedor principal
    mainContainer.appendChild(tablaContainer);
    mainContainer.appendChild(graficaContainer);

    // Limpiar y agregar al DOM
    container.innerHTML = '';
    container.appendChild(header);
    container.appendChild(mainContainer);
  }

  /**
   * Muestra error
   */
  static mostrarError(error) {
    const container = document.getElementById('resultados-container');
    if (!container) return;

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-mensaje';
    errorDiv.innerHTML = `
      <h3>Error</h3>
      <p>${error}</p>
    `;

    container.innerHTML = '';
    container.appendChild(errorDiv);
  }
}

/**
 * Utilidades generales
 */
class Utils {
  static mostrarCargando() {
    const container = document.getElementById('resultados-container');
    if (container) {
      container.innerHTML = '<p class="cargando">Calculando...</p>';
    }
  }

  static validarFormulario(datos, camposRequeridos) {
    for (let campo of camposRequeridos) {
      if (!datos[campo] && datos[campo] !== 0) {
        throw new Error(`Campo requerido: ${campo}`);
      }
    }
  }
}
