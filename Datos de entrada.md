# DATOS DE ENTRADA

| DATO | TIPO | DESCRIPCIÓN | UNIDAD |
|---|---|---|---|
| Presión_At | float | Presión atmosférica que mide el sensor | hPa |
| Aceleración | float | Aceleración instantánea | m/s² |
| temp | float | Temperatura | °C |
| Modo | int | Modo de Operación (Operador o simulación) | - |

## PROCESOS

1. Calcular la Altitud:

   h = 44330 * (1 - (Presión_At / 1013.25)^0.1903)

2. Determinar la fase de vuelo:
   - Si altitud_actual > altitud_previa => el cohete está ascendiendo.
   - Si altitud_actual < altitud_previa => el cohete está descendiendo.
   - Se determina con la aceleración si el cohete está en ascenso, apogeo y/o despliegue de paracaídas.

3. Evaluar temperatura:
   - Si temp > 80°C generar alerta.

4. Actualizar el apogeo:
   - Si altitud_actual > altitud_maxima → Reemplazar valor de altitud_maxima (solo queda el valor máximo guardado)
   - Si altitud_actual < altitud_previa → Apogeo_detectado = true

5. Acumular estadísticas:
   1. Suma de temperaturas
      - Suma_temperaturas = suma_temperaturas + temperatura
   2. Contar las lecturas
      - Contador = Contador + 1
   3. Calcular temperatura promedio
      - Temp_promedio = suma_temperaturas / contador
   4. Aceleración máxima
      - Si la aceleración > aceleracion_maxima → Se actualiza aceleracion_maxima = aceleración
   5. Avanzar el tiempo
      - Tiempo = tiempo + 1

6. Controlar bucles
   - Decidir cuándo terminar: altitud <= 0 o usuario detiene operación
   - Termina el ciclo

## DATOS DE SALIDA

| DATO | TIPO | DESCRIPCIÓN | UNIDAD |
|---|---|---|---|
| Altitud_actual | float | Altitud se muestra cada segundo | Metros (m) |
| Estado | int | Fases: 1. Ascenso 2. Apogeo 3. Paracaídas | - |
| Alerta_temp | str | Mensaje de alerta si la temperatura supera los 80°C | - |
| Altitud_maxima | float | Mayor altitud alcanzada durante el vuelo | m/s² |
| Temp_prom | float | Promedio de todas las temperaturas registradas | °C |
| Aceleracion_max | float | Mayor valor de aceleración registrado durante el vuelo | m/s² |
| Apogeo_detectado | bool | Indica si ya se inició el descenso (true = apogeo, False = Aún no) | - |

## DIAGRAMA DE FLUJO

<https://n9.cl/kzjp9>

# Pseudocódigo

## 1. Pseudocódigo (funciones)

**a) Función I: calcular_altitud(Presion_At)**

```
Funcion calcular_altitud(Presion_At)
    Altitud = 44330 * (1 - (Presion_At / 1013.25) ^ 0.1903)
    Retornar altitud
Fin Funcion
```

**b) Función 2: determinar_estado_vuelo(altitud_actual, altitud_previa, aceleracion)**

```
Funcion determinar_estado_vuelo(altitud_actual, altitud_previa, aceleracion)
    Si altitud_actual > altitud_previa Entonces
        Estado = 1
    SiNo
        Si altitud_actual < altitud_previa Entonces
            Si aceleracion <= 0 Entonces
                Estado = 2
            SiNo
                Estado = 3
            Fin Si
        Fin Si
    Fin Si
    Retornar estado
Fin Funcion
```

**c) Función 3: evaluar_alerta_temperatura(temp)**

```
Funcion evaluar_alerta_temperatura(temp)
    Si temp > 80 Entonces
        Alerta = "ALERTA: Temperatura critica"
    SiNo
        Alerta = "Sin Alerta"
    Fin Si
    Retornar alerta
Fin Funcion
```

**d) Función 4: generar_datos_simulados(t)**

```
Funcion generar_datos_simulados(t)
    Si t < 30 Entonces
        presion_base = 1013.25 - t * 15.0
        aceleracion_base = 20.0 - 0.5 * t
        temperatura_base = 25.0 + t * 1.5
    SiNo Si t < 60 Entonces
        presion_base = 1013.25 - 30*15.0 + (t - 30) * 10.0
        aceleracion_base = -9.8
        temperatura_base = 70.0 - (t - 30) * 0.5
    SiNo
        presion_base = 1013.25 - 30*15.0 + 30*10.0 + (t - 60) * 5.0
        aceleracion_base = 25.0
        temperatura_base = 55.0 - (t - 60) * 0.2
    Fin Si
    Devolver presion, aceleracion, temperatura
Fin Funcion
```

## 2. Pseudocódigo principal

```
Inicio
    Tiempo = 0
    Contador = 0
    Altitud_previa = 0
    Altitud_max = 0
    Aceleracion_max = 0
    Suma_temperaturas = 0
    Apogeo_detectado = False
    Continuar = True

    Escribir "Seleccionar modo: 1. Operación 2. Simulación"

    Si modo == Operador Entonces
        Leer presion, aceleracion y temperatura
    SiNo
        (Presion, aceleracion, Temperatura) = generar_datos_simulados(t)
    Fin Si

    Altitud_actual = calcular_altitud (Presion_At)
    Estado = determinar_estado_vuelo (Altitud_actual, Altitud_previa, Aceleracion)
    Alerta_temp = evaluar_alerta_temperatura (Temperatura)

    Si Altitud_actual > Altitud_max Entonces
        Altitud_max = Altitud_actual
    Fin Si

    Si Altitud_actual < Altitud_previa Entonces
        Apogeo_detectado = True
    Fin Si

    Suma_temperatura = suma_temperatura + Temperatura
    Contador = Contador + 1
    Temp_Prom = Suma_temperaturas / Contador

    Si Aceleracion > Aceleracion_max Entonces
        Aceleracion_max = Aceleracion
    Fin Si

    Escribir Tiempo, Altitud, Estado, Alerta, Altitud_max, Temp_Prom, Aceleracion_max

    Altitud_previa = Altitud_actual
    Tiempo = Tiempo + 1

    Si Altitud_actual <= 0 Entonces
        Continuar = False
    SiNo
        Escribir "¿Desea continuar?"
        Escribir "1. Si"
        Escribir "2. No"
        Leer opcion
        Si opcion = 2 Entonces
            Continuar = False
        Fin Si
    Fin Si
Fin Mientras

Escribir Tiempo, Altitud, Estado, Alerta, Altitud_max, Temp_Prom, Aceleracion_max, Apogeo_detectado
Fin
```
