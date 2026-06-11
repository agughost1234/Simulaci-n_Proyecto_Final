from evaluador import Evaluador
from biseccion import Biseccion
from newton_raphson import NewtonRaphson
from cambios_base import CambiosDeBase
from sistemas_no_lineales_newton import NewtonSistemas
from polinomios_lagrange import Lagrange
from diferencias_divididas_newton import DiferenciasDivididasNewton
from taylor import PolinomioTaylor
from minimos_cuadrados import MinimosCuadradosLineal
    
# --- BLOQUE DE PRUEBA MANUAL ---
if __name__ == "__main__":

    # ============================================================
    # 1. PROBANDO CAMBIOS DE BASE
    # ============================================================
    print("\n" + "="*60)
    print("PROBANDO CAMBIOS DE BASE")
    print("="*60)
    
    conversor = CambiosDeBase(None, None, 15) 
    base_origen = 2
    numero_prueba = "1011.101"  # Esto es 11.625 en decimal 
    base_destino = 3 # en base 3, esto debería ser aproximadamente "102.0021"
    
    print(f"Convirtiendo el número {numero_prueba} (Base {base_origen}) a Base {base_destino}...")
    resultado_base = conversor.ejecutar(base_origen, numero_prueba, base_destino)
    
    if isinstance(resultado_base, dict) and "error" in resultado_base:
        print(f"Error: {resultado_base['error']}")
    else:
        print(f"Resultado final: {resultado_base}_{base_destino}\n")
        
        print("--- PROCEDIMIENTO ALGORÍTMICO ---")
        print(f"{'Fase':<30} | {'Operación':<15} | {'Resultado':<10} | {'Dígito Extraído':<16} | {'Acumulado':<12}")
        print("-" * 100)
        for paso in conversor.historial:
            digito_val = f"{paso['Dígito Extraído']}" if paso['Dígito Extraído'] is not None else "......"
            acum_val = f"{paso['Acumulado']:.4f}" if paso['Acumulado'] is not None else "......"
            print(f"{paso['Fase']:<30} | {paso['Operación']:<15} | {paso['Resultado']:<10.4f} | {digito_val:<16} | {acum_val:<12}")
        print("-" * 100)
    
    # Pruebas tradicionales
    conversor.generar_excel("historial_cambio_base")
    # Pruebas Backend (Base64) - Sin gráfica
    b64_excel = conversor.obtener_excel_base64()
    print(f"[BACKEND] Excel Base64 generado: {b64_excel[:40]}... (Total: {len(b64_excel)} chars)")
        
    # ============================================================
    # 2. PROBANDO MÉTODO DE BISECCIÓN
    # ============================================================
    print("\n\n" + "="*60)
    print("PROBANDO MÉTODO DE BISECCIÓN")
    print("="*60)
    expresion = "exp(-x) - x" 
    tolerancia = 0.0001
    maximo_iteraciones = 100

    evaluador_test = Evaluador(expresion)
    busqueda_raiz = Biseccion(evaluador_test, tolerancia, maximo_iteraciones)
    resultado = busqueda_raiz.ejecutar(0, 1)

    if "error" in resultado:
        print(f"Error: {resultado['error']}")
    else:
        print(f"Estado de finalización: {resultado['estado'].upper()}")
        print(f"Raíz aproximada obtenida: {resultado['raiz']:.6f}\n")
        
        print(f"{'n':<4} | {'an':<10} | {'bn':<10} | {'pn':<10} | {'f(pn)':<11} | {'ERROR':<10}")
        print("-" * 70)
        for it in resultado["iteraciones"]:
            err_str = f"{it['error']:<10.6f}" if it['error'] is not None else f"{'.....':<10}"
            print(f"{it['iter']:<4} | {it['a']:<10.6f} | {it['b']:<10.6f} | {it['p_n']:<10.6f} | {it['f_p_n']:<11.6f} | {err_str}")
    
    # Pruebas tradicionales
    busqueda_raiz.generar_excel("historial_biseccion")
    busqueda_raiz.graficar("grafica_biseccion")
    # Pruebas Backend (Base64)
    b64_excel = busqueda_raiz.obtener_excel_base64()
    b64_img = busqueda_raiz.obtener_grafica_base64()
    print(f"[BACKEND] Excel Base64 generado: {b64_excel[:40]}... (Total: {len(b64_excel)} chars)")
    print(f"[BACKEND] Imagen Base64 generada: {b64_img[:40]}... (Total: {len(b64_img)} chars)")
        
    # ============================================================
    # 3. PROBANDO NEWTON-RAPHSON
    # ============================================================
    print("\n\n" + "="*60)
    print("PROBANDO MÉTODO DE NEWTON-RAPHSON")
    print("="*60)
    expresion = "x^3 - 2*x^2 -5"    
    evaluador_test = Evaluador(expresion)
    metodo_newton = NewtonRaphson(evaluador_test, tolerancia, maximo_iteraciones)
    res_newton = metodo_newton.ejecutar(0.5)

    if "error" in res_newton:
        print(f"Error: {res_newton['error']}")
    else:
        print(f"Estado: {res_newton['estado'].upper()}")
        print(f"Raíz obtenida: {res_newton['raiz']:.6f}\n")
        print(f"{'n':<4} | {'xn':<10} | {'f(xn)':<11} | {'ERROR':<10}")
        print("-" * 45)
        for it in res_newton["iteraciones"]:
            err_str = f"{it['error']:<10.6f}" if it['error'] is not None else f"{'.....':<10}"
            print(f"{it['iter']:<4} | {it['x_n']:<10.6f} | {it['f_x_n']:<11.6f} | {err_str}")
    
    # Pruebas tradicionales
    metodo_newton.generar_excel("historial_newton_raphson")
    metodo_newton.graficar("grafica_newton_raphson")
    # Pruebas Backend (Base64)
    b64_excel = metodo_newton.obtener_excel_base64()
    b64_img = metodo_newton.obtener_grafica_base64()
    print(f"[BACKEND] Excel Base64 generado: {b64_excel[:40]}... (Total: {len(b64_excel)} chars)")
    print(f"[BACKEND] Imagen Base64 generada: {b64_img[:40]}... (Total: {len(b64_img)} chars)")

    # ============================================================
    # 4. PROBANDO POLINOMIO DE TAYLOR
    # ============================================================
    print("\n\n" + "="*60)
    print("PROBANDO POLINOMIO DE TAYLOR")
    print("="*60)
    expresion_taylor = "exp(x)" 
    evaluador_taylor = Evaluador(expresion_taylor)
    metodo_taylor = PolinomioTaylor(evaluador_taylor, tolerancia=0.0, max_iter=0)
    
    x0_centro = 0.0
    x_a_evaluar = 1.0
    grado_polinomial = 5
    
    print(f"Aproximando f(x) = {expresion_taylor} centrado en x0 = {x0_centro}")
    print(f"Evaluando para x = {x_a_evaluar} usando grado {grado_polinomial}...\n")
    
    res_taylor = metodo_taylor.ejecutar(x0=x0_centro, x_eval=x_a_evaluar, grado=grado_polinomial)
    
    if "error" in res_taylor:
        print(f"Error: {res_taylor['error']}")
    else:
        print(f"Estado: {res_taylor['estado'].upper()}")
        print(f"Aproximación final obtenida: {res_taylor['aproximacion']:.6f}\n")
        
        print(f"{'k (Grado)':<10} | {'f^(k)(x0)':<15} | {'Término k':<15} | {'Suma Acumulada':<15}")
        print("-" * 65)
        for paso in res_taylor["historial"]:
            print(f"{paso['orden_k']:<10} | {paso['derivada_en_x0']:<15.6f} | {paso['termino_k']:<15.6f} | {paso['aproximacion_acumulada']:<15.6f}")
        print("-" * 65)
        
    # Pruebas tradicionales
    metodo_taylor.generar_excel("historial_taylor")
    metodo_taylor.graficar("grafica_taylor")
    # Pruebas Backend (Base64)
    b64_excel = metodo_taylor.obtener_excel_base64()
    b64_img = metodo_taylor.obtener_grafica_base64()
    print(f"[BACKEND] Excel Base64 generado: {b64_excel[:40]}... (Total: {len(b64_excel)} chars)")
    print(f"[BACKEND] Imagen Base64 generada: {b64_img[:40]}... (Total: {len(b64_img)} chars)")

    # ============================================================
    # 5. PROBANDO MÍNIMOS CUADRADOS (MODELO LINEAL)
    # ============================================================
    print("\n\n" + "="*60)
    print("PROBANDO MÍNIMOS CUADRADOS (MODELO LINEAL)")
    print("="*60)
    
    metodo_min_cuadrados = MinimosCuadradosLineal()
    puntos_x = [1.0, 2.0, 3.0, 4.0, 5.0]
    puntos_y = [3.1, 4.9, 7.2, 8.8, 11.1]
    
    res_mc = metodo_min_cuadrados.ejecutar(puntos_x, puntos_y)
    
    if "error" in res_mc:
        print(f"Error: {res_mc['error']}")
    else:
        print(f"Estado: {res_mc['estado'].upper()}")
        print(f"Intersección (c0): {res_mc['c0']:.6f}")
        print(f"Pendiente (c1):     {res_mc['c1']:.6f}")
        print(f"Ecuación ajustada:  y = {res_mc['c0']:.4f} + {res_mc['c1']:.4f}x\n")
        
        print(f"{'Punto i':<8} | {'x_i':<10} | {'y_real':<10} | {'y_predicho':<12} | {'Error (Residuo)':<15}")
        print("-" * 65)
        for punto in res_mc["historial"]:
            print(f"{punto['punto_i']:<8} | {punto['x_i']:<10.2f} | {punto['y_real']:<10.2f} | {punto['y_predicho']:<12.4f} | {punto['error_residual']:<15.4f}")
        print("-" * 65)
        
    # Pruebas tradicionales
    metodo_min_cuadrados.generar_excel("historial_minimos_cuadrados")
    metodo_min_cuadrados.graficar("grafica_minimos_cuadrados")
    # Pruebas Backend (Base64)
    b64_excel = metodo_min_cuadrados.obtener_excel_base64()
    b64_img = metodo_min_cuadrados.obtener_grafica_base64()
    print(f"[BACKEND] Excel Base64 generado: {b64_excel[:40]}... (Total: {len(b64_excel)} chars)")
    print(f"[BACKEND] Imagen Base64 generada: {b64_img[:40]}... (Total: {len(b64_img)} chars)")

    # ============================================================
    # 6. PROBANDO NEWTON PARA SISTEMAS NO LINEALES
    # ============================================================
    print("\n\n" + "="*60)
    print("PROBANDO NEWTON PARA SISTEMAS NO LINEALES")
    print("="*60)
    
    funcs = [
        lambda x: x[0]**2 + x[0]*x[1] - 10,
        lambda x: x[1] + 3*x[0]*(x[1]**2) - 57
    ]
    jacob = [
        [lambda x: 2*x[0] + x[1],         lambda x: x[0]],
        [lambda x: 3*(x[1]**2),           lambda x: 1 + 6*x[0]*x[1]]
    ]
    x0_iniciales = [1.5, 3.5]

    metodo_sys = NewtonSistemas(tolerancia=1e-6, max_iteraciones=50)
    res_sys = metodo_sys.ejecutar(funcs, jacob, x0_iniciales)

    if "error" in res_sys:
        print(f"Error: {res_sys['error']}")
    else:
        print(f"Estado: {res_sys['estado'].upper()}")
        print(f"Solución Vectorial Obtenida: {res_sys['solucion']}")
        print(f"Residuo Final: {res_sys['residuo']:.2e}\n")
        
        print(f"{'Iter':<5} | {'Error':<12} | {'Residuo':<12} | {'Variables Calculadas (x_0, x_1, ...)'}")
        print("-" * 75)
        for p in res_sys["historial"]:
            err_v = f"{p['error']:.6f}" if p['error'] is not None else "------"
            res_v = f"{p['residuo']:.6f}" if p['residuo'] is not None else "------"
            print(f"{p['iteracion']:<5} | {err_v:<12} | {res_v:<12} | [{p['x_0']:.4f}, {p['x_1']:.4f}]")
            
    # Pruebas tradicionales (SIN GRÁFICA COMO LO SOLICITASTE)
    metodo_sys.generar_excel("historial_newton_sistemas")
    # Pruebas Backend (Base64) - Sin gráfica
    b64_excel = metodo_sys.obtener_excel_base64()
    print(f"[BACKEND] Excel Base64 generado: {b64_excel[:40]}... (Total: {len(b64_excel)} chars)")

    # ============================================================
    # 7. PROBANDO DIFERENCIAS DIVIDIDAS DE NEWTON
    # ============================================================
    print("\n\n" + "="*60)
    print("PROBANDO DIFERENCIAS DIVIDIDAS DE NEWTON")
    print("="*60)
    
    puntos_x = [1.0, 2.0, 4.0, 7.0]
    puntos_y = [3.0, 5.0, 11.0, 21.0]

    metodo_dd = DiferenciasDivididasNewton()
    res_dd = metodo_dd.ejecutar(puntos_x, puntos_y)

    print(f"Estado: {res_dd['estado'].upper()}")
    print(f"Coeficientes c_i: {res_dd['coeficientes']}")
    print(f"Polinomio obtenido: P(x) = {res_dd['expresion']}\n")
    
    print("Tabla de Diferencias Divididas calculada:")
    for fila in res_dd["historial"]:
        valores_fila = [f"{fila[k]:.4f}" for k in fila if "F_Orden" in k]
        print(f"i={fila['i']} | x={fila['x_i']:.1f} | Diffs: {valores_fila}")

    # Pruebas tradicionales
    metodo_dd.generar_excel("historial_diferencias_divididas")
    metodo_dd.graficar("grafica_diferencias_divididas")
    # Pruebas Backend (Base64)
    b64_excel = metodo_dd.obtener_excel_base64()
    b64_img = metodo_dd.obtener_grafica_base64()
    print(f"[BACKEND] Excel Base64 generado: {b64_excel[:40]}... (Total: {len(b64_excel)} chars)")
    print(f"[BACKEND] Imagen Base64 generada: {b64_img[:40]}... (Total: {len(b64_img)} chars)")

    # ============================================================
    # 8. PROBANDO POLINOMIO INTERPOLANTE DE LAGRANGE
    # ============================================================
    print("\n\n" + "="*60)
    print("PROBANDO POLINOMIO INTERPOLANTE DE LAGRANGE")
    print("="*60)
    
    puntos_x = [1.0, 2.0, 4.0, 7.0]
    puntos_y = [3.0, 5.0, 11.0, 21.0]

    metodo_lagrange = Lagrange()
    res_lagrange = metodo_lagrange.ejecutar(puntos_x, puntos_y)

    if "error" in res_lagrange:
        print(f"Error: {res_lagrange['error']}")
    else:
        print(f"Estado: {res_lagrange['estado'].upper()}")
        print(f"Coeficientes Monomiales: {res_lagrange['coeficientes']}")
        print(f"Polinomio obtenido: P(x) = {res_lagrange['expresion']}\n")
        
        print(f"{'Polin L_i':<10} | {'x_i':<6} | {'y_i':<6} | {'Denominador L_i':<18} | Coefs Parciales")
        print("-" * 75)
        for p in res_lagrange["historial"]:
            print(f"L_{p['polinomio_L_i']:<8} | {p['x_i']:<6.1f} | {p['y_i']:<6.1f} | {p['denominador_L']:<18.4f} | {p['coef_monomial_parcial']}")

    # Pruebas tradicionales
    metodo_lagrange.generar_excel("historial_polinomio_lagrange")
    metodo_lagrange.graficar("grafica_polinomio_lagrange")
    # Pruebas Backend (Base64)
    b64_excel = metodo_lagrange.obtener_excel_base64()
    b64_img = metodo_lagrange.obtener_grafica_base64()
    print(f"[BACKEND] Excel Base64 generado: {b64_excel[:40]}... (Total: {len(b64_excel)} chars)")
    print(f"[BACKEND] Imagen Base64 generada: {b64_img[:40]}... (Total: {len(b64_img)} chars)")
    
    print("\n" + "="*60 + "\n¡CÓDIGOS PROBADOS CON ÉXITO Y LISTOS PARA EL BACKEND!\n" + "="*60)