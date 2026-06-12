/**
 * Form handlers para todos los métodos numéricos
 */

// Asegurar que el documento esté completamente cargado
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupAllForms);
} else {
  setupAllForms();
}

function setupAllForms() {
  // Verificar que las clases estén disponibles
  if (typeof APIClient === 'undefined' || typeof ResultadosRenderer === 'undefined' || typeof Utils === 'undefined') {
    console.warn('Clases de API no están disponibles aún. Reintentando en 500ms...');
    setTimeout(setupAllForms, 500);
    return;
  }
  
  setupBiseccionForm();
  setupNewtonForm();
  setupTaylorForm();
  setupCambioBaseForm();
  setupLagrangeForm();
  setupDiferenciasDivididasForm();
  setupMinimosCuadradosForm();
  setupNewtonSistemasForm();
}

// ═══════════════════════════════════════════════════════════
// BISECCIÓN
// ═══════════════════════════════════════════════════════════
function setupBiseccionForm() {
  const form = document.getElementById('forma-biseccion');
  if (!form) {
    console.warn('forma-biseccion no encontrado');
    return;
  }
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    (async () => {
      try {
        const expresion = document.getElementById('ecuacion')?.value;
        const a_inicial = parseFloat(document.getElementById('a')?.value);
        const b_inicial = parseFloat(document.getElementById('b')?.value);
        const tolerancia = parseFloat(document.getElementById('tolerancia')?.value || 0.0001);
        
        if (!expresion || isNaN(a_inicial) || isNaN(b_inicial)) {
          throw new Error('Por favor completa todos los campos requeridos');
        }
        
        Utils.mostrarCargando();
        
        const resultado = await APIClient.biseccion(expresion, a_inicial, b_inicial, tolerancia);
        
        if (resultado.success) {
          resultado.data.expresion = `f(x) = ${expresion}`;
          ResultadosRenderer.renderMetodoIterativo(resultado.data, 'biseccion');
        } else {
          ResultadosRenderer.mostrarError(resultado.error || 'Error en el cálculo');
        }
      } catch (error) {
        console.error('Error:', error);
        ResultadosRenderer.mostrarError(error.message);
      }
    })();
    
    return false;
  });
}

// ═══════════════════════════════════════════════════════════
// NEWTON-RAPHSON
// ═══════════════════════════════════════════════════════════
function setupNewtonForm() {
  const form = document.getElementById('forma-newton');
  if (!form) {
    console.warn('forma-newton no encontrado');
    return;
  }
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    (async () => {
      try {
        const expresion = document.getElementById('ecuacion')?.value;
        const x_inicial = parseFloat(document.getElementById('x0')?.value);
        const tolerancia = parseFloat(document.getElementById('tolerancia')?.value || 0.0001);
        const max_iteraciones = parseInt(document.getElementById('max_iteraciones')?.value || 100);
        
        if (!expresion || isNaN(x_inicial)) {
          throw new Error('Por favor completa todos los campos requeridos');
        }
        
        Utils.mostrarCargando();
        
        const resultado = await APIClient.newton(expresion, x_inicial, tolerancia, max_iteraciones);
        
        if (resultado.success) {
          resultado.data.expresion = `f(x) = ${expresion}`;
          ResultadosRenderer.renderMetodoIterativo(resultado.data, 'newton');
        } else {
          ResultadosRenderer.mostrarError(resultado.error);
        }
      } catch (error) {
        console.error('Error:', error);
        ResultadosRenderer.mostrarError(error.message);
      }
    })();
    
    return false;
  });
}

// ═══════════════════════════════════════════════════════════
// TAYLOR
// ═══════════════════════════════════════════════════════════
function setupTaylorForm() {
  const form = document.getElementById('forma-taylor');
  if (!form) {
    console.warn('forma-taylor no encontrado');
    return;
  }
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    (async () => {
      try {
        const expresion = document.getElementById('funcion')?.value;
        const centro = parseFloat(document.getElementById('punto_desarrollo')?.value);
        const grado = parseInt(document.getElementById('grado')?.value);
        const punto_evaluacion = parseFloat(document.getElementById('punto_evaluacion')?.value || centro);
        
        if (!expresion || isNaN(centro) || isNaN(grado)) {
          throw new Error('Por favor completa todos los campos requeridos');
        }
        
        Utils.mostrarCargando();
        
        const resultado = await APIClient.taylor(expresion, centro, grado, punto_evaluacion);
        
        if (resultado.success) {
          resultado.data.expresion = `f(x) = ${expresion}`;
          ResultadosRenderer.renderTaylor(resultado.data);
        } else {
          ResultadosRenderer.mostrarError(resultado.error);
        }
      } catch (error) {
        console.error('Error:', error);
        ResultadosRenderer.mostrarError(error.message);
      }
    })();
    
    return false;
  });
}

// ═══════════════════════════════════════════════════════════
// CAMBIO DE BASE
// ═══════════════════════════════════════════════════════════
function setupCambioBaseForm() {
  const form = document.getElementById('forma-cambio-base');
  if (!form) {
    console.warn('forma-cambio-base no encontrado');
    return;
  }
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    (async () => {
      try {
        const numero = document.getElementById('numero')?.value;
        const base_origen = parseInt(document.getElementById('base_origen')?.value);
        const base_destino = parseInt(document.getElementById('base_destino')?.value);
        
        if (!numero || isNaN(base_origen) || isNaN(base_destino)) {
          throw new Error('Por favor completa todos los campos requeridos');
        }
        
        Utils.mostrarCargando();
        
        const resultado = await APIClient.cambioBase(numero, base_origen, base_destino);
        
        if (resultado.success) {
          resultado.data.numero_original = numero;
          resultado.data.base_origen = base_origen;
          resultado.data.base_destino = base_destino;
          ResultadosRenderer.renderCambioBase(resultado.data);
        } else {
          ResultadosRenderer.mostrarError(resultado.error);
        }
      } catch (error) {
        console.error('Error:', error);
        ResultadosRenderer.mostrarError(error.message);
      }
    })();
    
    return false;
  });
}

// ═══════════════════════════════════════════════════════════
// LAGRANGE
// ═══════════════════════════════════════════════════════════
function setupLagrangeForm() {
  const form = document.getElementById('forma-lagrange');
  if (!form) {
    console.warn('forma-lagrange no encontrado');
    return;
  }
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    (async () => {
      try {
        const puntos = obtenerPuntos();
        
        if (puntos.length < 2) {
          throw new Error('Se requieren al menos 2 puntos');
        }
        
        const x_evaluacion = puntos[Math.floor(puntos.length / 2)].x;
        
        Utils.mostrarCargando();
        
        const resultado = await APIClient.lagrange(puntos, x_evaluacion);
        
        if (resultado.success) {
          ResultadosRenderer.renderInterpolacion(resultado.data, 'lagrange');
        } else {
          ResultadosRenderer.mostrarError(resultado.error);
        }
      } catch (error) {
        console.error('Error:', error);
        ResultadosRenderer.mostrarError(error.message);
      }
    })();
    
    return false;
  });
}

// ═══════════════════════════════════════════════════════════
// DIFERENCIAS DIVIDIDAS
// ═══════════════════════════════════════════════════════════
function setupDiferenciasDivididasForm() {
  const form = document.getElementById('forma-diferencias-divididas');
  if (!form) {
    console.warn('forma-diferencias-divididas no encontrado');
    return;
  }
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    (async () => {
      try {
        const puntos = obtenerPuntos();
        
        if (puntos.length < 2) {
          throw new Error('Se requieren al menos 2 puntos');
        }
        
        const x_evaluacion = puntos[Math.floor(puntos.length / 2)].x;
        
        Utils.mostrarCargando();
        
        const resultado = await APIClient.diferenciasDivididas(puntos, x_evaluacion);
        
        if (resultado.success) {
          ResultadosRenderer.renderInterpolacion(resultado.data, 'diferencias');
        } else {
          ResultadosRenderer.mostrarError(resultado.error);
        }
      } catch (error) {
        console.error('Error:', error);
        ResultadosRenderer.mostrarError(error.message);
      }
    })();
    
    return false;
  });
}

// ═══════════════════════════════════════════════════════════
// MÍNIMOS CUADRADOS
// ═══════════════════════════════════════════════════════════
function setupMinimosCuadradosForm() {
  const form = document.getElementById('forma-minimos-cuadrados');
  if (!form) {
    console.warn('forma-minimos-cuadrados no encontrado');
    return;
  }
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    (async () => {
      try {
        const puntos = obtenerPuntos();
        const grado = parseInt(document.getElementById('grado')?.value || 1);
        
        if (puntos.length < 2) {
          throw new Error('Se requieren al menos 2 puntos');
        }
        
        Utils.mostrarCargando();
        
        const resultado = await APIClient.minimoscuadrados(puntos, grado, 'polinomio');
        
        if (resultado.success) {
          ResultadosRenderer.renderInterpolacion(resultado.data, 'minimos');
        } else {
          ResultadosRenderer.mostrarError(resultado.error);
        }
      } catch (error) {
        console.error('Error:', error);
        ResultadosRenderer.mostrarError(error.message);
      }
    })();
    
    return false;
  });
}

// ═══════════════════════════════════════════════════════════
// NEWTON SISTEMAS
// ═══════════════════════════════════════════════════════════
function setupNewtonSistemasForm() {
  const form = document.getElementById('forma-newton-sistemas');
  if (!form) {
    console.warn('forma-newton-sistemas no encontrado');
    return;
  }
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    (async () => {
      try {
        // Obtener ecuaciones como string y convertir a array
        const ecuacionesStr = document.getElementById('ecuaciones')?.value;
        const ecuaciones = ecuacionesStr.split(',').map(eq => eq.trim()).filter(eq => eq);
        
        // Obtener valores iniciales como string y convertir a array de números
        const valoresStr = document.getElementById('valores_iniciales')?.value;
        const valores_iniciales = valoresStr.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v));
        
        // Obtener tolerancia y max_iteraciones
        const tolerancia = parseFloat(document.getElementById('tolerancia')?.value || 0.0001);
        const max_iteraciones = parseInt(document.getElementById('max_iteraciones')?.value || 50);
        
        // Validar
        if (ecuaciones.length === 0 || valores_iniciales.length === 0) {
          throw new Error('Por favor ingresa ecuaciones y valores iniciales válidos');
        }
        
        if (ecuaciones.length !== valores_iniciales.length) {
          throw new Error(`Se esperan ${ecuaciones.length} valores iniciales, se recibieron ${valores_iniciales.length}`);
        }
        
        Utils.mostrarCargando();
        
        const resultado = await APIClient.newtonSistemas(ecuaciones, valores_iniciales, tolerancia, max_iteraciones);
        
        console.log('Resultado Newton-Sistemas:', resultado);
        
        if (resultado.success && resultado.data) {
          ResultadosRenderer.renderNewtonSistemas(resultado.data);
        } else if (resultado.error) {
          ResultadosRenderer.mostrarError(resultado.error);
        } else {
          ResultadosRenderer.mostrarError('Error desconocido en la respuesta del servidor');
        }
      } catch (error) {
        console.error('Error:', error);
        ResultadosRenderer.mostrarError(error.message);
      }
    })();
    
    return false;
  });
}


// ═══════════════════════════════════════════════════════════
// UTILIDADES
// ═══════════════════════════════════════════════════════════

/**
 * Extrae puntos de la tabla con id="puntos-table"
 */
function obtenerPuntos() {
  const table = document.querySelector('table#puntos-table');
  if (!table) return [];
  
  const puntos = [];
  const rows = table.querySelectorAll('tbody tr');
  
  rows.forEach(row => {
    const inputs = row.querySelectorAll('input.punto-input');
    if (inputs.length >= 2) {
      const x = parseFloat(inputs[0].value);
      const y = parseFloat(inputs[1].value);
      if (!isNaN(x) && !isNaN(y)) {
        puntos.push({ x, y });
      }
    }
  });
  
  return puntos;
}