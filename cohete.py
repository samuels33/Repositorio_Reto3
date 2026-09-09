def calcular_altitud(presion_At):
    altitud = 44330 * (1-(presion_At / 1013.25) ** 0.1903)
    return altitud

def determinar_estado_vuelo(altitud_actual, altitud_previa, aceleracion):
    if altitud_actual > altitud_previa:
        return 1
    elif altitud_actual < altitud_previa:
        return 3
    else:
        return 2
def evaluar_alerta_temperatura(temp):
        if temp > 80:
            return "ALERTA"
        else:
            return "no hay alerta"
#def generar_datos_simulados(t):      # me ayude con IA
            if t < 5:
                presion = 1013.25 - (t * 30)
                aceleracion = 20 - (t * 2)
                temperatura = 40 + (t * 5)
            elif t < 10:
                presion = 863.25
                aceleracion = 0
                temperatura = 65
            else:
                presion = 863.25 + ((t - 7) * 40)
                aceleracion = -5
                temperatura = 60 -((t - 7) * 2)
            return presion, aceleracion, temperatura


tiempo = 0
contador = 0
altitud_previa = 0
altitud_max = 0
aceleracion_max = 0
suma_temperatura = 0
apogeo_detectado = False
continuar = True


print("seleccionar modo : 'operador' o 'simulacion' ")
modo = input()

while continuar:
    if modo == "operador":
        presion = float(input("Ingrese presion: "))
        aceleracion = float(input("Ingrese aceleracion: "))
        temperatura = float(input("Ingrese temperatura: "))
    else:
        presion, aceleracion, temperatura = generar_datos_simulados(tiempo)
        print("presion:", presion)
        print("Aceleracion:", aceleracion)
        print("Temperatura:", temperatura)

    altitud_actual = calcular_altitud(presion)
    estado = determinar_estado_vuelo(altitud_actual, altitud_previa, aceleracion)
    alerta = evaluar_alerta_temperatura(temperatura)
    if altitud_actual > altitud_max:
        altitud_max = altitud_actual

    if altitud_actual < altitud_previa:
        apogeo_detectado = True

    suma_temperatura = suma_temperatura + temperatura
    contador = contador + 1
    temp_promedio = suma_temperatura / contador

    if aceleracion > aceleracion_max:
        aceleracion_max = aceleracion

    print(f"tiempo: {tiempo}s")
    print(f"Altitud: {altitud_actual:.2f}m")
    print(f"presion: {presion}hPa")
    print(f"Estado: {estado}")
    print(f"Alerta: {alerta}")
    print(f"Altitud maxima: {altitud_max:.2f}")
    print(f"Temperatura promedio: {temp_promedio:.2f}°c")
    print(f"Aceleracion maxima: {aceleracion_max}m/s²")
    print(f"Apogeo dectado: {apogeo_detectado}")

    if estado == 1:
        print("Fase: Ascenso")
    elif estado == 2:
        print("Fase: Apogeo")
    elif estado == 3:
        print("Fase: Despliegue de paracaidas")

    altitud_previa = altitud_actual
    tiempo = tiempo + 1

    if altitud_actual <= 0:
        print("Ha aterrizado")
        continuar = False
    else: 
        opcion = input("¿Desea continuar? (Si/No)")
        if opcion == "No":
            continuar = False

    print(f"Altitud maxima: {altitud_max:.2f}m")
    print(f"Temperatura promedio: {temp_promedio:.2f}°c")
    print(f"Aceleracion maxima: {aceleracion_max}m/s²")
    print(f"Apogeo dectado: {apogeo_detectado}")
