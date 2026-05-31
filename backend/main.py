from evaluador import Evaluador
from biseccion import Biseccion
from newton_raphson import NewtonRaphson
from cambios_base import CambiosDeBase
    
# --- BLOQUE DE PRUEBA MANUAL ---
if __name__ == "__main__":


    print("\n\n" + "="*60)
    print("PROBANDO CAMBIOS DE BASE")
    print("="*60)
    
    # Instanciamos enviando None al evaluador/tol porque no se usan aquí, 
    # pero pasamos 15 como max_iter para la parte fraccionaria.
    conversor = CambiosDeBase(None, None, 15) 
    
    base_origen = 10
    numero_prueba = "22.625"
    base_destino = 2
    
    print(f"Convirtiendo el número {numero_prueba} (Base {base_origen}) a Base {base_destino}...")
    resultado_base = conversor.ejecutar(base_origen, numero_prueba, base_destino)
    
    if isinstance(resultado_base, dict) and "error" in resultado_base:
        print(f"Error: {resultado_base['error']}")
    else:
        print(f"Resultado final: {resultado_base}_{base_destino}\n")
        
        # Tabla del procedimiento (Historial de divisiones/multiplicaciones)
        print("--- PROCEDIMIENTO ALGORÍTMICO ---")
        print(f"{'Fase':<30} | {'Operación':<15} | {'Resultado':<10} | {'Dígito/Acumulado'}")
        print("-" * 80)
        for paso in conversor.historial:
            # Buscamos 'Dígito Extraído', y si no está (porque es polinómica), buscamos 'Acumulado'
            valor_extra = paso.get('Dígito Extraído', paso.get('Acumulado', ''))
            print(f"{paso['Fase']:<30} | {paso['Operación']:<15} | {paso['Resultado']:<10.4f} | {valor_extra}")
        print("-" * 80)
        
    print("\n\n" + "="*60)
    print("PROBANDO MÉTODO DE BISECCIÓN")
    print("="*60)
    # Probemos con el ejercicio de la imagen para validar que dé igual
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
        
        # Formato de tabla elegante e idéntico al solicitado
        print(f"{'n':<4} | {'an':<10} | {'bn':<10} | {'pn':<10} | {'f(pn)':<11} | {'ERROR':<10}")
        print("-" * 70)
        for it in resultado["iteraciones"]:
            err_str = f"{it['error']:<10.6f}" if it['error'] is not None else f"{'.....':<10}"
            print(f"{it['iter']:<4} | {it['a']:<10.6f} | {it['b']:<10.6f} | {it['p_n']:<10.6f} | {it['f_p_n']:<11.6f} | {err_str}")
        
        # Al final de tu código de prueba, puedes agregar esto:
    print("\n" + "="*50 + "\nProbando Newton-Raphson:\n" + "="*50)
    metodo_newton = NewtonRaphson(evaluador_test, tolerancia, maximo_iteraciones)
    res_newton = metodo_newton.ejecutar(0.5)

    print(f"Estado: {res_newton['estado'].upper()}")
    print(f"Raíz obtenida: {res_newton['raiz']:.6f}\n")
    print(f"{'n':<4} | {'xn':<10} | {'f(xn)':<11} | {'ERROR':<10}")
    print("-" * 45)
    for it in res_newton["iteraciones"]:
        print(f"{it['iter']:<4} | {it['x_n']:<10.6f} | {it['f_x_n']:<11.6f} | {it['error']:<10.6f}")