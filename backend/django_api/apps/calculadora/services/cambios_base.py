from .metodo_numerico import MetodoNumerico


class CambiosDeBase(MetodoNumerico):

    def ejecutar(self, base_actual, numero, base_nueva):
        base_actual = int(base_actual)
        base_nueva = int(base_nueva)
        num_str = str(numero)

        for i in num_str:
            if i == '.':
                continue
            if not i.isdigit():
                return {"error": f"El carácter '{i}' no es un dígito válido"}
            if int(i) >= base_actual:
                return {"error": f"El dígito '{i}' no es válido para la base {base_actual}"}
            
        if "." in num_str:
            parte_entera_str, parte_fraccionaria_str = num_str.split(".")
        else:
            parte_entera_str, parte_fraccionaria_str = num_str, ""

        def from_ten_to_base_n(n, val_decimal):
            parte_decimal = val_decimal % 1
            parte_entera = int(val_decimal)
            acc_entero = ""
            
            if parte_entera == 0:
                acc_entero = "0"
            else:
                while parte_entera > 0:
                    residuo = parte_entera % n
                    cociente = parte_entera // n
                    
                    self.historial.append({
                        "Fase": "Entera (División)",
                        "Operación": f"{parte_entera} / {n}",
                        "Resultado": cociente,
                        "Dígito Extraído": residuo,
                        "Acumulado": None
                    })
                    
                    acc_entero = str(residuo) + acc_entero
                    parte_entera = cociente

            acc_fraccionaria = ""
            iteracion = 0
            while parte_decimal > 0 and iteracion < self.max_iter:
                parte_decimal = round(parte_decimal, 10)
                if parte_decimal == 0:
                    break
                    
                producto = parte_decimal * n
                digito = int(producto)
                
                self.historial.append({
                    "Fase": "Fraccionaria (Multiplicación)",
                    "Operación": f"{parte_decimal} * {n}",
                    "Resultado": producto,
                    "Dígito Extraído": digito,
                    "Acumulado": None
                })
                
                acc_fraccionaria += str(digito)
                parte_decimal = producto % 1
                iteracion += 1
                
            if acc_fraccionaria:
                return acc_entero + "." + acc_fraccionaria
            return acc_entero
            

        def from_base_n_to_ten(n, parte_entera, parte_fraccionaria):
            acc = 0
            exponente = len(parte_entera) - 1
            cadena_completa = parte_entera + parte_fraccionaria
            
            for i in cadena_completa:
                valor_paso = int(i) * pow(n, exponente)
                acc += valor_paso
                
                self.historial.append({
                    "Fase": "Polinómica (Base N a 10)",
                    "Operación": f"{i} * ({n}^{exponente})",
                    "Resultado": valor_paso,
                    "Dígito Extraído": None,
                    "Acumulado": acc
                })
                
                exponente -= 1
                
            return acc
        
        self.limpiar_historial()
        if base_actual == base_nueva:
            return num_str
        elif base_actual == 10:
            val_decimal = float(num_str)
            return from_ten_to_base_n(base_nueva, val_decimal)
        elif base_nueva == 10:
            return str(from_base_n_to_ten(base_actual, parte_entera_str, parte_fraccionaria_str))
        else:
            decimal_intermedio = from_base_n_to_ten(base_actual, parte_entera_str, parte_fraccionaria_str)
            return from_ten_to_base_n(base_nueva, decimal_intermedio)
