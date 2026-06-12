const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const DJANGO_API_URL = process.env.DJANGO_API_URL || 'http://localhost:8000/api';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'frontend')));

// ═══════════════════════════════════════════════════════════
// RUTAS API - PROXY HACIA DJANGO
// ═══════════════════════════════════════════════════════════

// Bisección
app.post('/api/calculos/biseccion', async (req, res) => {
  try {
    const { expresion, a_inicial, b_inicial, tolerancia = 0.0001, max_iteraciones = 100 } = req.body;
    
    const response = await axios.post(`${DJANGO_API_URL}/calculos/biseccion/`, {
      expresion,
      a_inicial: parseFloat(a_inicial),
      b_inicial: parseFloat(b_inicial),
      tolerancia: parseFloat(tolerancia),
      max_iteraciones: parseInt(max_iteraciones)
    });
    
    res.json({
      success: true,
      data: response.data
    });
  } catch (error) {
    console.error('Error en bisección:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Newton-Raphson
app.post('/api/calculos/newton', async (req, res) => {
  try {
    const { expresion, x_inicial, tolerancia = 0.0001, max_iteraciones = 100 } = req.body;
    
    const response = await axios.post(`${DJANGO_API_URL}/calculos/newton-raphson/`, {
      expresion,
      x_inicial: parseFloat(x_inicial),
      tolerancia: parseFloat(tolerancia),
      max_iteraciones: parseInt(max_iteraciones)
    });
    
    res.json({
      success: true,
      data: response.data
    });
  } catch (error) {
    console.error('Error en Newton:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Polinomios de Taylor
app.post('/api/calculos/polinomio-taylor', async (req, res) => {
  try {
    const { expresion, centro, grado, punto_evaluacion } = req.body;
    
    const response = await axios.post(`${DJANGO_API_URL}/calculos/polinomio-taylor/`, {
      expresion,
      centro: parseFloat(centro),
      grado: parseInt(grado),
      punto_evaluacion: parseFloat(punto_evaluacion)
    });
    
    res.json({
      success: true,
      data: response.data
    });
  } catch (error) {
    console.error('Error en Taylor:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Cambio de Base
app.post('/api/calculos/cambio-base', async (req, res) => {
  try {
    const { numero, base_origen, base_destino, max_iteraciones = 50 } = req.body;
    
    const response = await axios.post(`${DJANGO_API_URL}/calculos/cambios-base/`, {
      numero,
      base_origen: parseInt(base_origen),
      base_destino: parseInt(base_destino),
      max_iteraciones: parseInt(max_iteraciones)
    });
    
    res.json({
      success: true,
      data: response.data
    });
  } catch (error) {
    console.error('Error en cambio de base:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Lagrange
app.post('/api/calculos/lagrange', async (req, res) => {
  try {
    const { puntos, x_evaluacion = puntos[Math.floor(puntos.length / 2)]?.x } = req.body;
    
    const puntos_x = puntos.map(p => parseFloat(p.x));
    const puntos_y = puntos.map(p => parseFloat(p.y));
    
    const response = await axios.post(`${DJANGO_API_URL}/calculos/interpolacion-lagrange/`, {
      puntos_x,
      puntos_y,
      x_evaluacion: parseFloat(x_evaluacion)
    });
    
    res.json({
      success: true,
      data: response.data
    });
  } catch (error) {
    console.error('Error en Lagrange:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Diferencias Divididas
app.post('/api/calculos/diferencias-divididas', async (req, res) => {
  try {
    const { puntos, x_evaluacion = puntos[Math.floor(puntos.length / 2)]?.x } = req.body;
    
    const puntos_x = puntos.map(p => parseFloat(p.x));
    const puntos_y = puntos.map(p => parseFloat(p.y));
    
    const response = await axios.post(`${DJANGO_API_URL}/calculos/diferencias-divididas/`, {
      puntos_x,
      puntos_y,
      x_evaluacion: parseFloat(x_evaluacion)
    });
    
    res.json({
      success: true,
      data: response.data
    });
  } catch (error) {
    console.error('Error en Diferencias Divididas:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Mínimos Cuadrados
app.post('/api/calculos/minimos-cuadrados', async (req, res) => {
  try {
    const { puntos, grado = 1, tipo_ajuste = 'polinomio' } = req.body;
    
    const puntos_x = puntos.map(p => parseFloat(p.x));
    const puntos_y = puntos.map(p => parseFloat(p.y));
    
    const response = await axios.post(`${DJANGO_API_URL}/calculos/ajuste-curvas/`, {
      puntos_x,
      puntos_y,
      grado: parseInt(grado),
      tipo_ajuste
    });
    
    res.json({
      success: true,
      data: response.data
    });
  } catch (error) {
    console.error('Error en Mínimos Cuadrados:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Newton para Sistemas
app.post('/api/calculos/newton-sistemas', async (req, res) => {
  try {
    const { ecuaciones, valores_iniciales, tolerancia = 0.0001, max_iteraciones = 100 } = req.body;
    
    const response = await axios.post(`${DJANGO_API_URL}/calculos/newton-sistemas/`, {
      ecuaciones,
      valores_iniciales: valores_iniciales.map(v => parseFloat(v)),
      tolerancia: parseFloat(tolerancia),
      max_iteraciones: parseInt(max_iteraciones)
    });
    
    res.json({
      success: true,
      data: response.data
    });
  } catch (error) {
    console.error('Error en Newton Sistemas:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// ═══════════════════════════════════════════════════════════
// RUTA POR DEFECTO - SERVIR FRONTEND
// ═══════════════════════════════════════════════════════════
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

// Manejo de rutas no encontradas
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Ruta no encontrada'
  });
});

// ═══════════════════════════════════════════════════════════
// INICIAR SERVIDOR
// ═══════════════════════════════════════════════════════════
app.listen(PORT, () => {
  console.log(`✓ Servidor corriendo en http://localhost:${PORT}`);
  console.log(`✓ API Django: ${DJANGO_API_URL}`);
});
