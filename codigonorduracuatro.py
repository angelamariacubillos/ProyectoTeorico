import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from scipy import stats
import math

archivo_dat = "datosliterales.txt"
archivo_dat2 = "datosusme.txt"
archivo_dat3 = "datosengativa.txt"
archivo_dat4 = "datosvalentina.txt"

mes = archivo_dat[5:]
mes = mes[:-4]
df = pd.read_csv(archivo_dat, sep=';', skiprows=42, header=None)
horaUTC = df[0]
T = df[2]
V = df[3]
brillo = df[4]

mes2 = archivo_dat2[5:]
mes2 = mes2[:-4]
df2 = pd.read_csv(archivo_dat2, sep=';', skiprows=42, header=None)
horaUTC2 = df2[0]
T2 = df2[2]
V2 = df2[3]
brillo2 = df2[4]

mes3 = archivo_dat3[5:]
mes3 = mes3[:-4]
df3 = pd.read_csv(archivo_dat3, sep=';', skiprows=42, header=None)
horaUTC3 = df3[0]
T3 = df3[2]
V3 = df3[3]
brillo3 = df3[4]

mes4 = archivo_dat4[5:]
mes4 = mes4[:-4]
df4 = pd.read_csv(archivo_dat4, sep=';', skiprows=42, header=None)
horaUTC4 = df4[0]
T4 = df4[2]
V4 = df4[3]
brillo4 = df4[4]


horas_utc = [datetime.strptime(hora, '%Y-%m-%dT%H:%M:%S.%f') for hora in horaUTC]
horas_bogota = [hora - timedelta(hours=5) for hora in horas_utc]
horas_nocturnas = [hora for hora in horas_bogota if hora.hour >= 17 or hora.hour <= 7]
horas_nocturnas.sort()

noches_separadas = []
noche_actual = []

ventanas_todas = []
brillo_todas = []
duracion_todas = []
brillo_promedio_todas = []

ventanas_por_mes = {}

horas_utc2 = [datetime.strptime(hora, '%Y-%m-%dT%H:%M:%S.%f') for hora in horaUTC2]
horas_bogota2 = [hora - timedelta(hours=5) for hora in horas_utc2]
horas_nocturnas2 = [hora for hora in horas_bogota2 if hora.hour >= 17 or hora.hour <= 7]
horas_nocturnas2.sort()

noches_separadas2 = []
noche_actual2 = []

ventanas_todas2 = []
brillo_todas2 = []
duracion_todas2 = []
brillo_promedio_todas2 = []

ventanas_por_mes2 = {}

horas_utc3 = [datetime.strptime(hora, '%Y-%m-%dT%H:%M:%S.%f') for hora in horaUTC3]
horas_bogota3 = [hora - timedelta(hours=5) for hora in horas_utc3]
horas_nocturnas3 = [hora for hora in horas_bogota3 if hora.hour >= 17 or hora.hour <= 7]
horas_nocturnas3.sort()

noches_separadas3 = []
noche_actual3 = []

ventanas_todas3 = []
brillo_todas3 = []
duracion_todas3 = []
brillo_promedio_todas3 = []

ventanas_por_mes3 = {}

horas_utc4 = [datetime.strptime(hora, '%Y-%m-%dT%H:%M:%S.%f') for hora in horaUTC4]
horas_bogota4 = [hora - timedelta(hours=5) for hora in horas_utc4]
horas_nocturnas4 = [hora for hora in horas_bogota4 if hora.hour >= 17 or hora.hour <= 7]
horas_nocturnas4.sort()

noches_separadas4 = []
noche_actual4 = []

ventanas_todas4 = []
brillo_todas4 = []
duracion_todas4 = []
brillo_promedio_todas4 = []

ventanas_por_mes4 = {}


umbral_variabilidad = 0.05

intervalosvent = {}
intervalosvent2 = {}
intervalosvent3 = {}
intervalosvent4 = {}

#set 1

for hora in horas_nocturnas:
    
    if not noche_actual:
        
        noche_actual.append(hora)
        
    elif (hora - noche_actual[-1]).seconds > 6 * 3600:
        
        noches_separadas.append(noche_actual)
        noche_actual = [hora]
        
    else:
        noche_actual.append(hora)

noches_separadas.append(noche_actual)

duracion_todas = []
noches_en_mes = {}

for idx, noche in enumerate(noches_separadas):
    
    mes_actual = noche[0].strftime('%m')
    
    if mes_actual not in noches_en_mes:
        noches_en_mes[mes_actual] = set()
    noches_en_mes[mes_actual].add(noche[0].strftime('%m-%d'))
    
    noches_en_mes[mes_actual].add(noche[0].strftime('%m-%d'))
    
    plt.figure(figsize=(10, 6))
    
    brillo_noche = [brillo[horas_bogota.index(hora)] for hora in noche]
    
    brillo_noche_filtrado = [b for b in brillo_noche if b > 18]
    horas_noche_filtrado = [hora for i, hora in enumerate(noche) if brillo_noche[i] > 18]
    
    desviacion_estandar = np.std(brillo_noche_filtrado)
    
    ventanas_noche_actual = []
    brillo_noche_actual = []
    duracion_noche_actual = []
    
    MAD = stats.median_abs_deviation(brillo_noche_filtrado)
    mediana = np.median(brillo_noche_filtrado)
    promedio = np.mean(brillo_noche_filtrado)
        
    brillo_noche_filtrado = [b for b in brillo_noche if b > 6]
    horas_noche_filtrado = [hora for i, hora in enumerate(noche) if brillo_noche[i] > 6]
    
    
    if not math.isnan(mediana):
        
        if float(mediana) >= 19.0:
                       
            valoroscu_datos = [dato for dato in brillo_noche_filtrado if dato >= 19.0]
            valoroscu_horas = [hora for hora, dato in zip(horas_noche_filtrado, brillo_noche_filtrado) if dato >= 19.0]
            
            plt.scatter(valoroscu_horas, valoroscu_datos, color='r')
            
            intervalos_consecutivos = []
            temp_intervalo = [valoroscu_datos[0]]
            temp_horas_intervalo = [valoroscu_horas[0]]
            
            for i in range(0, len(valoroscu_datos)):
                
                diferencia = valoroscu_horas[i] - valoroscu_horas[i - 1]
                
                if abs(diferencia) <= timedelta(minutes=5):
                    
                    temp_intervalo.append(valoroscu_datos[i])
                    temp_horas_intervalo.append(valoroscu_horas[i])
                    
                else:
                    
                    intervalos_consecutivos.append((temp_intervalo, temp_horas_intervalo))
                    temp_intervalo = [valoroscu_datos[i]]
                    temp_horas_intervalo = [valoroscu_horas[i]]
                    intervalos_consecutivos.append((temp_intervalo, temp_horas_intervalo))
            
            for intervalo, horas_intervalo in intervalos_consecutivos:

                if len(intervalo)>=5:

                    plt.scatter(horas_intervalo, intervalo, color='green')
                
                    brillo_promedio_conjunto = np.mean(intervalo)
                    brillo_promedio_todas.append(brillo_promedio_conjunto)
        
                    ventanas_todas.append(intervalo) 
                    brillo_todas.append(intervalo)                     
                
                    
                    
                    duracion_intervalo = (horas_intervalo[-1] - horas_intervalo[0]).total_seconds() / 3600.0
                    duracion_todas.append(duracion_intervalo)
                
                    
                    mes_actual = horas_intervalo[0].strftime('%m')
                    
                    if mes_actual not in ventanas_por_mes:
                        ventanas_por_mes[mes_actual] = set()
                    ventanas_por_mes[mes_actual].add(tuple(horas_intervalo))

                    if mes_actual not in intervalosvent:
                        intervalosvent[mes_actual] = []
                    
                    intervalosvent[mes_actual].append(duracion_intervalo)
         
                    
        else:
            
            valoroscu = mediana + MAD
            valoroscu_datos = [dato for dato in brillo_noche_filtrado if dato >= valoroscu]
            valoroscu_horas = [hora for hora, dato in zip(horas_noche_filtrado, brillo_noche_filtrado) if dato >= valoroscu]
    
            plt.scatter(valoroscu_horas, valoroscu_datos, color='r')

            intervalos_consecutivos = []
            temp_intervalo = [valoroscu_datos[0]]
            temp_horas_intervalo = [valoroscu_horas[0]]
            
            for i in range(0, len(valoroscu_datos)):
                
                if abs(valoroscu_horas[i] - valoroscu_horas[i - 1]) <= timedelta(minutes=5):
                    
                    temp_intervalo.append(valoroscu_datos[i])
                    temp_horas_intervalo.append(valoroscu_horas[i])
                    
                else:
                    intervalos_consecutivos.append((temp_intervalo, temp_horas_intervalo))
                    temp_intervalo = [valoroscu_datos[i]]
                    temp_horas_intervalo = [valoroscu_horas[i]]
                    intervalos_consecutivos.append((temp_intervalo, temp_horas_intervalo))
            
    
            for intervalo, horas_intervalo in intervalos_consecutivos:
                
                if len(intervalo)>=5:
                    
                    diferencias_brillo = np.diff(intervalo)
                    
                    if any(abs(diff) <= umbral_variabilidad for diff in diferencias_brillo):

                        
                        plt.scatter(horas_intervalo, intervalo, color='green')
                        
                        brillo_promedio_conjunto = np.mean(intervalo)
                        brillo_promedio_todas.append(brillo_promedio_conjunto)
            
                        ventanas_todas.append(intervalo) 
                        brillo_todas.append(intervalo)                     
                
                        
                        duracion_intervalo = (horas_intervalo[-1] - horas_intervalo[0]).total_seconds() / 3600.0
                        duracion_todas.append(duracion_intervalo)
                    
                        
                        mes_actual = horas_intervalo[0].strftime('%m')
                        
                        if mes_actual not in ventanas_por_mes:
                            ventanas_por_mes[mes_actual] = set()
                        ventanas_por_mes[mes_actual].add(tuple(horas_intervalo))

                        if mes_actual not in intervalosvent:
                            intervalosvent[mes_actual] = []
                        
                        intervalosvent[mes_actual].append(duracion_intervalo)

    plt.plot(horas_noche_filtrado, brillo_noche_filtrado, color='teal')
    formatoho = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(formatoho)
    plt.xlabel('Hora Local (Bogotá)', weight='bold') 
    plt.ylabel(r'$\mathbf{Brillo\ (mag/arcsec^2)}$', weight='bold')  
    
    plt.title('Brillo Nocturno', weight='bold', fontsize=20, y=1.06)
    fecha_noche = noche[0].strftime('%d-%m-%Y')
    dia=fecha_noche[:2]
    plt.suptitle(f'{fecha_noche}', weight='bold', fontsize=14, y=0.87)

    plt.grid(True)
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()

    
#set 2

for hora in horas_nocturnas2:
    
    if not noche_actual2:
        
        noche_actual2.append(hora)
        
    elif (hora - noche_actual2[-1]).seconds > 6 * 3600:
        
        noches_separadas2.append(noche_actual2)
        noche_actual2 = [hora]
        
    else:
        noche_actual2.append(hora)

noches_separadas2.append(noche_actual2)

duracion_todas2 = []

noches_en_mes2 = {}

for idx, noche in enumerate(noches_separadas2):
    
    mes_actual2 = noche[0].strftime('%m')
    
    if mes_actual2 not in noches_en_mes2:
        noches_en_mes2[mes_actual2] = set()
    noches_en_mes2[mes_actual2].add(noche[0].strftime('%m-%d'))
    
    noches_en_mes2[mes_actual2].add(noche[0].strftime('%m-%d'))
    
    plt.figure(figsize=(10, 6))
    
    brillo_noche2 = [brillo2[horas_bogota2.index(hora)] for hora in noche]
    
    brillo_noche_filtrado2 = [b for b in brillo_noche2 if b > 18]
    horas_noche_filtrado2 = [hora for i, hora in enumerate(noche) if brillo_noche2[i] > 18]
    
    desviacion_estandar2 = np.std(brillo_noche_filtrado2)
    
    ventanas_noche_actual2 = []
    brillo_noche_actual2 = []
    duracion_noche_actual2 = []
    
    MAD2 = stats.median_abs_deviation(brillo_noche_filtrado2)
    mediana2 = np.median(brillo_noche_filtrado2)
    promedio2 = np.mean(brillo_noche_filtrado2)
        
    brillo_noche_filtrado2 = [b for b in brillo_noche2 if b > 6]
    horas_noche_filtrado2 = [hora for i, hora in enumerate(noche) if brillo_noche2[i] > 6]
    
    
    if not math.isnan(mediana2):
        
        if float(mediana2) >= 19.0:
                       
            valoroscu_datos2 = [dato for dato in brillo_noche_filtrado2 if dato >= 19.0]
            valoroscu_horas2 = [hora for hora, dato in zip(horas_noche_filtrado2, brillo_noche_filtrado2) if dato >= 19.0]
            
            plt.scatter(valoroscu_horas2, valoroscu_datos2, color='r')
            
            intervalos_consecutivos2 = []
            temp_intervalo2 = [valoroscu_datos2[0]]
            temp_horas_intervalo2 = [valoroscu_horas2[0]]
            
            for i in range(0, len(valoroscu_datos2)):
                
                diferencia2 = valoroscu_horas2[i] - valoroscu_horas2[i - 1]
                
                if abs(diferencia2) <= timedelta(minutes=5):
                    
                    temp_intervalo2.append(valoroscu_datos2[i])
                    temp_horas_intervalo2.append(valoroscu_horas2[i])
                    
                else:
                    
                    intervalos_consecutivos2.append((temp_intervalo2, temp_horas_intervalo2))
                    temp_intervalo2 = [valoroscu_datos2[i]]
                    temp_horas_intervalo2 = [valoroscu_horas2[i]]
                    intervalos_consecutivos2.append((temp_intervalo2, temp_horas_intervalo2))
            
            for intervalo, horas_intervalo in intervalos_consecutivos2:

                if len(intervalo)>=5:

                    plt.scatter(horas_intervalo, intervalo, color='green')
                
                    brillo_promedio_conjunto2 = np.mean(intervalo)
                    brillo_promedio_todas2.append(brillo_promedio_conjunto2)
        
                    ventanas_todas2.append(intervalo) 
                    brillo_todas2.append(intervalo)                     
                
                    
                    
                    duracion_intervalo2 = (horas_intervalo[-1] - horas_intervalo[0]).total_seconds() / 3600.0
                    duracion_todas2.append(duracion_intervalo2)

                    
                    mes_actual2 = horas_intervalo[0].strftime('%m')
                    
                    if mes_actual2 not in ventanas_por_mes2:
                        ventanas_por_mes2[mes_actual2] = set()  
                    ventanas_por_mes2[mes_actual2].add(tuple(horas_intervalo))
                    
                    if mes_actual2 not in intervalosvent2:
                        intervalosvent2[mes_actual2] = []
                    
                    intervalosvent2[mes_actual2].append(duracion_intervalo2)
    
                    
        else:
            
            valoroscu2 = mediana2 + MAD2
            valoroscu_datos2 = [dato for dato in brillo_noche_filtrado2 if dato >= valoroscu2]
            valoroscu_horas2 = [hora for hora, dato in zip(horas_noche_filtrado2, brillo_noche_filtrado2) if dato >= valoroscu2]
    
            plt.scatter(valoroscu_horas2, valoroscu_datos2, color='r')

            intervalos_consecutivos2 = []
            temp_intervalo2 = [valoroscu_datos2[0]]
            temp_horas_intervalo2 = [valoroscu_horas2[0]]
            
            for i in range(0, len(valoroscu_datos2)):
                
                if abs(valoroscu_horas2[i] - valoroscu_horas2[i - 1]) <= timedelta(minutes=5):
                    
                    temp_intervalo2.append(valoroscu_datos2[i])
                    temp_horas_intervalo2.append(valoroscu_horas2[i])
                    
                else:
                    intervalos_consecutivos2.append((temp_intervalo2, temp_horas_intervalo2))
                    temp_intervalo2 = [valoroscu_datos2[i]]
                    temp_horas_intervalo2 = [valoroscu_horas2[i]]
                    intervalos_consecutivos2.append((temp_intervalo2, temp_horas_intervalo2))
            
    
            for intervalo, horas_intervalo in intervalos_consecutivos2:
                
                if len(intervalo)>=5:
                    
                    diferencias_brillo2 = np.diff(intervalo)
                    
                    if any(abs(diff) <= umbral_variabilidad for diff in diferencias_brillo2):

                        
                        plt.scatter(horas_intervalo, intervalo, color='green')
                        
                        brillo_promedio_conjunto2 = np.mean(intervalo)
                        brillo_promedio_todas2.append(brillo_promedio_conjunto2)
            
                        ventanas_todas2.append(intervalo) 
                        brillo_todas2.append(intervalo)                     
                
                        
                        duracion_intervalo2 = (horas_intervalo[-1] - horas_intervalo[0]).total_seconds() / 3600.0
                        duracion_todas2.append(duracion_intervalo2)
                    
                        mes_actual2 = horas_intervalo[0].strftime('%m')
                        
                        if mes_actual2 not in ventanas_por_mes2:
                            ventanas_por_mes2[mes_actual2] = set()  
                        ventanas_por_mes2[mes_actual2].add(tuple(horas_intervalo))
                        
                        if mes_actual2 not in intervalosvent2:
                            intervalosvent2[mes_actual2] = []
                        
                        intervalosvent2[mes_actual2].append(duracion_intervalo2)
                        

    plt.plot(horas_noche_filtrado2, brillo_noche_filtrado2, color='cornflowerblue')
    formatoho = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(formatoho)
    plt.xlabel('Hora Local (Bogotá)', weight='bold') 
    plt.ylabel(r'$\mathbf{Brillo\ (mag/arcsec^2)}$', weight='bold')  
    
    plt.title('Brillo Nocturno', weight='bold', fontsize=20, y=1.06)
    fecha_noche2 = noche[0].strftime('%d-%m-%Y')
    dia=fecha_noche2[:2]
    plt.suptitle(f'{fecha_noche2}', weight='bold', fontsize=14, y=0.87)

    plt.grid(True)
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()
    
#set 3

for hora in horas_nocturnas3:
    
    if not noche_actual3:
        
        noche_actual3.append(hora)
        
    elif (hora - noche_actual3[-1]).seconds > 6 * 3600:
        
        noches_separadas3.append(noche_actual3)
        noche_actual3 = [hora]
        
    else:
        noche_actual3.append(hora)

noches_separadas3.append(noche_actual3)

duracion_todas3 = []

noches_en_mes3 = {}

for idx, noche in enumerate(noches_separadas3):
    
    mes_actual3 = noche[0].strftime('%m')
    
    if mes_actual3 not in noches_en_mes3:
        noches_en_mes3[mes_actual3] = set()
    noches_en_mes3[mes_actual3].add(noche[0].strftime('%m-%d'))
    
    noches_en_mes3[mes_actual3].add(noche[0].strftime('%m-%d'))
    
    plt.figure(figsize=(10, 6))
    
    brillo_noche3 = [brillo3[horas_bogota3.index(hora)] for hora in noche]
    
    brillo_noche_filtrado3 = [b for b in brillo_noche3 if b > 18]
    horas_noche_filtrado3 = [hora for i, hora in enumerate(noche) if brillo_noche3[i] > 18]
    
    desviacion_estandar3 = np.std(brillo_noche_filtrado3)
    
    ventanas_noche_actual3 = []
    brillo_noche_actual3 = []
    duracion_noche_actual3 = []
    
    MAD3 = stats.median_abs_deviation(brillo_noche_filtrado3)
    mediana3 = np.median(brillo_noche_filtrado3)
    promedio3 = np.mean(brillo_noche_filtrado3)
        
    brillo_noche_filtrado3 = [b for b in brillo_noche3 if b > 6]
    horas_noche_filtrado3 = [hora for i, hora in enumerate(noche) if brillo_noche3[i] > 6]
    
    
    if not math.isnan(mediana3):
        
        if float(mediana3) >= 19.0:
                       
            valoroscu_datos3 = [dato for dato in brillo_noche_filtrado3 if dato >= 19.0]
            valoroscu_horas3 = [hora for hora, dato in zip(horas_noche_filtrado3, brillo_noche_filtrado3) if dato >= 19.0]
            
            plt.scatter(valoroscu_horas3, valoroscu_datos3, color='r')
            
            intervalos_consecutivos3 = []
            temp_intervalo3 = [valoroscu_datos3[0]]
            temp_horas_intervalo3 = [valoroscu_horas3[0]]
            
            for i in range(0, len(valoroscu_datos3)):
                
                diferencia3 = valoroscu_horas3[i] - valoroscu_horas3[i - 1]
                
                if abs(diferencia3) <= timedelta(minutes=5):
                    
                    temp_intervalo3.append(valoroscu_datos3[i])
                    temp_horas_intervalo3.append(valoroscu_horas3[i])
                    
                else:
                    
                    intervalos_consecutivos3.append((temp_intervalo3, temp_horas_intervalo3))
                    temp_intervalo3 = [valoroscu_datos3[i]]
                    temp_horas_intervalo3 = [valoroscu_horas3[i]]
                    intervalos_consecutivos3.append((temp_intervalo3, temp_horas_intervalo3))
            
            for intervalo, horas_intervalo in intervalos_consecutivos3:

                if len(intervalo)>=5:

                    plt.scatter(horas_intervalo, intervalo, color='green')
                
                    brillo_promedio_conjunto3 = np.mean(intervalo)
                    brillo_promedio_todas3.append(brillo_promedio_conjunto3)
        
                    ventanas_todas3.append(intervalo) 
                    brillo_todas3.append(intervalo)                     
                
                    
                    
                    duracion_intervalo3 = (horas_intervalo[-1] - horas_intervalo[0]).total_seconds() / 3600.0
                    duracion_todas3.append(duracion_intervalo3)

                    
                    mes_actual3 = horas_intervalo[0].strftime('%m')
                    
                    if mes_actual3 not in ventanas_por_mes3:
                        ventanas_por_mes3[mes_actual3] = set()  
                    ventanas_por_mes3[mes_actual3].add(tuple(horas_intervalo))
                    
                    if mes_actual3 not in intervalosvent3:
                        intervalosvent3[mes_actual3] = []
                    
                    intervalosvent3[mes_actual3].append(duracion_intervalo3)
    
                    
        else:
            
            valoroscu3 = mediana3 + MAD3
            valoroscu_datos3 = [dato for dato in brillo_noche_filtrado3 if dato >= valoroscu3]
            valoroscu_horas3 = [hora for hora, dato in zip(horas_noche_filtrado3, brillo_noche_filtrado3) if dato >= valoroscu3]
    
            plt.scatter(valoroscu_horas3, valoroscu_datos3, color='r')

            intervalos_consecutivos3 = []
            temp_intervalo3 = [valoroscu_datos3[0]]
            temp_horas_intervalo3 = [valoroscu_horas3[0]]
            
            for i in range(0, len(valoroscu_datos3)):
                
                if abs(valoroscu_horas3[i] - valoroscu_horas3[i - 1]) <= timedelta(minutes=5):
                    
                    temp_intervalo3.append(valoroscu_datos3[i])
                    temp_horas_intervalo3.append(valoroscu_horas3[i])
                    
                else:
                    intervalos_consecutivos3.append((temp_intervalo3, temp_horas_intervalo3))
                    temp_intervalo3 = [valoroscu_datos3[i]]
                    temp_horas_intervalo3 = [valoroscu_horas3[i]]
                    intervalos_consecutivos3.append((temp_intervalo3, temp_horas_intervalo3))
            
    
            for intervalo, horas_intervalo in intervalos_consecutivos3:
                
                if len(intervalo)>=5:
                    
                    diferencias_brillo3 = np.diff(intervalo)
                    
                    if any(abs(diff) <= umbral_variabilidad for diff in diferencias_brillo3):

                        
                        plt.scatter(horas_intervalo, intervalo, color='green')
                        
                        brillo_promedio_conjunto3 = np.mean(intervalo)
                        brillo_promedio_todas3.append(brillo_promedio_conjunto3)
            
                        ventanas_todas3.append(intervalo) 
                        brillo_todas3.append(intervalo)                     
                
                        
                        duracion_intervalo3 = (horas_intervalo[-1] - horas_intervalo[0]).total_seconds() / 3600.0
                        duracion_todas3.append(duracion_intervalo3)
                    
                        mes_actual3 = horas_intervalo[0].strftime('%m')
                        
                        if mes_actual3 not in ventanas_por_mes3:
                            ventanas_por_mes3[mes_actual3] = set()  
                        ventanas_por_mes3[mes_actual3].add(tuple(horas_intervalo))
                        
                        if mes_actual3 not in intervalosvent3:
                            intervalosvent3[mes_actual3] = []
                        
                        intervalosvent3[mes_actual3].append(duracion_intervalo3)
                        

    plt.plot(horas_noche_filtrado3, brillo_noche_filtrado3, color='cornflowerblue')
    formatoho = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(formatoho)
    plt.xlabel('Hora Local (Bogotá)', weight='bold') 
    plt.ylabel(r'$\mathbf{Brillo\ (mag/arcsec^3)}$', weight='bold')  
    
    plt.title('Brillo Nocturno', weight='bold', fontsize=20, y=1.06)
    fecha_noche3 = noche[0].strftime('%d-%m-%Y')
    dia=fecha_noche3[:2]
    plt.suptitle(f'{fecha_noche3}', weight='bold', fontsize=14, y=0.87)

    plt.grid(True)
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()

#set 4

for hora in horas_nocturnas4:
    
    if not noche_actual4:
        
        noche_actual4.append(hora)
        
    elif (hora - noche_actual4[-1]).seconds > 6 * 3600:
        
        noches_separadas4.append(noche_actual4)
        noche_actual4 = [hora]
        
    else:
        noche_actual4.append(hora)

noches_separadas4.append(noche_actual4)

duracion_todas4 = []

noches_en_mes4 = {}

for idx, noche in enumerate(noches_separadas4):
    
    mes_actual4 = noche[0].strftime('%m')
    
    if mes_actual4 not in noches_en_mes4:
        noches_en_mes4[mes_actual4] = set()
    noches_en_mes4[mes_actual4].add(noche[0].strftime('%m-%d'))
    
    noches_en_mes4[mes_actual4].add(noche[0].strftime('%m-%d'))
    
    plt.figure(figsize=(10, 6))
    
    brillo_noche4 = [brillo4[horas_bogota4.index(hora)] for hora in noche]
    
    brillo_noche_filtrado4 = [b for b in brillo_noche4 if b > 18]
    horas_noche_filtrado4 = [hora for i, hora in enumerate(noche) if brillo_noche4[i] > 18]
    
    desviacion_estandar4 = np.std(brillo_noche_filtrado4)
    
    ventanas_noche_actual4 = []
    brillo_noche_actual4 = []
    duracion_noche_actual4 = []
    
    MAD4 = stats.median_abs_deviation(brillo_noche_filtrado4)
    mediana4 = np.median(brillo_noche_filtrado4)
    promedio4 = np.mean(brillo_noche_filtrado4)
        
    brillo_noche_filtrado4 = [b for b in brillo_noche4 if b > 6]
    horas_noche_filtrado4 = [hora for i, hora in enumerate(noche) if brillo_noche4[i] > 6]
    
    
    if not math.isnan(mediana4):
        
        if float(mediana4) >= 19.0:
                       
            valoroscu_datos4 = [dato for dato in brillo_noche_filtrado4 if dato >= 19.0]
            valoroscu_horas4 = [hora for hora, dato in zip(horas_noche_filtrado4, brillo_noche_filtrado4) if dato >= 19.0]
            
            plt.scatter(valoroscu_horas4, valoroscu_datos4, color='r')
            
            intervalos_consecutivos4 = []
            temp_intervalo4 = [valoroscu_datos4[0]]
            temp_horas_intervalo4 = [valoroscu_horas4[0]]
            
            for i in range(0, len(valoroscu_datos4)):
                
                diferencia4 = valoroscu_horas4[i] - valoroscu_horas4[i - 1]
                
                if abs(diferencia4) <= timedelta(minutes=5):
                    
                    temp_intervalo4.append(valoroscu_datos4[i])
                    temp_horas_intervalo4.append(valoroscu_horas4[i])
                    
                else:
                    
                    intervalos_consecutivos4.append((temp_intervalo4, temp_horas_intervalo4))
                    temp_intervalo4 = [valoroscu_datos4[i]]
                    temp_horas_intervalo4 = [valoroscu_horas4[i]]
                    intervalos_consecutivos4.append((temp_intervalo4, temp_horas_intervalo4))
            
            for intervalo, horas_intervalo in intervalos_consecutivos4:

                if len(intervalo)>=5:

                    plt.scatter(horas_intervalo, intervalo, color='green')
                
                    brillo_promedio_conjunto4 = np.mean(intervalo)
                    brillo_promedio_todas4.append(brillo_promedio_conjunto4)
        
                    ventanas_todas4.append(intervalo) 
                    brillo_todas4.append(intervalo)                     
                
                   
                    duracion_intervalo4 = (horas_intervalo[-1] - horas_intervalo[0]).total_seconds() / 3600.0
                    duracion_todas4.append(duracion_intervalo4)

                    
                    mes_actual4 = horas_intervalo[0].strftime('%m')
                    
                    if mes_actual4 not in ventanas_por_mes4:
                        ventanas_por_mes4[mes_actual4] = set()  
                    ventanas_por_mes4[mes_actual4].add(tuple(horas_intervalo))
                    
                    if mes_actual4 not in intervalosvent4:
                        intervalosvent4[mes_actual4] = []
                    
                    intervalosvent4[mes_actual4].append(duracion_intervalo4)
    
                    
        else:
            
            valoroscu4 = mediana4 + MAD4
            valoroscu_datos4 = [dato for dato in brillo_noche_filtrado4 if dato >= valoroscu4]
            valoroscu_horas4 = [hora for hora, dato in zip(horas_noche_filtrado4, brillo_noche_filtrado4) if dato >= valoroscu4]
    
            plt.scatter(valoroscu_horas4, valoroscu_datos4, color='r')

            intervalos_consecutivos4 = []
            temp_intervalo4 = [valoroscu_datos4[0]]
            temp_horas_intervalo4 = [valoroscu_horas4[0]]
            
            for i in range(0, len(valoroscu_datos4)):
                
                if abs(valoroscu_horas4[i] - valoroscu_horas4[i - 1]) <= timedelta(minutes=5):
                    
                    temp_intervalo4.append(valoroscu_datos4[i])
                    temp_horas_intervalo4.append(valoroscu_horas4[i])
                    
                else:
                    intervalos_consecutivos4.append((temp_intervalo4, temp_horas_intervalo4))
                    temp_intervalo4 = [valoroscu_datos4[i]]
                    temp_horas_intervalo4 = [valoroscu_horas4[i]]
                    intervalos_consecutivos4.append((temp_intervalo4, temp_horas_intervalo4))
            
    
            for intervalo, horas_intervalo in intervalos_consecutivos4:
                
                if len(intervalo)>=5:
                    
                    diferencias_brillo4 = np.diff(intervalo)
                    
                    if any(abs(diff) <= umbral_variabilidad for diff in diferencias_brillo4):

                        
                        plt.scatter(horas_intervalo, intervalo, color='green')
                        
                        brillo_promedio_conjunto4 = np.mean(intervalo)
                        brillo_promedio_todas4.append(brillo_promedio_conjunto4)
            
                        ventanas_todas4.append(intervalo) 
                        brillo_todas4.append(intervalo)                     
                
                        
                        duracion_intervalo4 = (horas_intervalo[-1] - horas_intervalo[0]).total_seconds() / 3600.0
                        duracion_todas4.append(duracion_intervalo4)
                    
                        mes_actual4 = horas_intervalo[0].strftime('%m')
                        
                        if mes_actual4 not in ventanas_por_mes4:
                            ventanas_por_mes4[mes_actual4] = set()  
                        ventanas_por_mes4[mes_actual4].add(tuple(horas_intervalo))
                        
                        if mes_actual4 not in intervalosvent4:
                            intervalosvent4[mes_actual4] = []
                        
                        intervalosvent4[mes_actual4].append(duracion_intervalo4)
                        

    plt.plot(horas_noche_filtrado4, brillo_noche_filtrado4, color='cornflowerblue')
    formatoho = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(formatoho)
    plt.xlabel('Hora Local (Bogotá)', weight='bold') 
    plt.ylabel(r'$\mathbf{Brillo\ (mag/arcsec^2)}$', weight='bold')  
    
    plt.title('Brillo Nocturno', weight='bold', fontsize=20, y=1.06)
    fecha_noche4 = noche[0].strftime('%d-%m-%Y')
    dia=fecha_noche4[:2]
    plt.suptitle(f'{fecha_noche4}', weight='bold', fontsize=14, y=0.87)

    plt.grid(True)
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()    
    
meses = list(ventanas_por_mes.keys())
ventanas = [len(ventanas_por_mes[mes]) for mes in meses]
duracion_horas = np.array(duracion_todas)
brillo_promedio = np.array(brillo_promedio_todas)

meses2 = list(ventanas_por_mes2.keys())
ventanas2 = [len(ventanas_por_mes2[mes]) for mes in meses2]
duracion_horas2 = np.array(duracion_todas2)
brillo_promedio2 = np.array(brillo_promedio_todas2)

meses3 = list(ventanas_por_mes3.keys())
ventanas3 = [len(ventanas_por_mes3[mes]) for mes in meses3]
duracion_horas3 = np.array(duracion_todas3)
brillo_promedio3 = np.array(brillo_promedio_todas3)

meses4 = list(ventanas_por_mes4.keys())
ventanas4 = [len(ventanas_por_mes4[mes]) for mes in meses4]
duracion_horas4 = np.array(duracion_todas4)
brillo_promedio4 = np.array(brillo_promedio_todas4)

duracion_total_por_mes = {}

for mes, ventana in intervalosvent.items():
    duracion_total_mes_minutos = sum(ventana) * 60  
    duracion_total_por_mes[mes] = duracion_total_mes_minutos

duracion_por_mes = {}

for mes, noches in noches_en_mes.items():
    duracion_total_mes = 0
    
    for noche_fecha in noches:
        
        noche = [hora for hora in noches_separadas if hora[0].strftime('%m-%d') == noche_fecha][0]
        
        duracion_noche = (max(noche) - min(noche)).total_seconds() / 60
        
        duracion_total_mes += duracion_noche
    
    duracion_por_mes[mes] = duracion_total_mes
    
    
duracion_total_por_mes2 = {}

for mes, ventana in intervalosvent2.items():
    duracion_total_mes_minutos2 = sum(ventana) * 60  
    duracion_total_por_mes2[mes] = duracion_total_mes_minutos2

duracion_por_mes2 = {}

for mes, noches in noches_en_mes2.items():
    duracion_total_mes2 = 0
    
    for noche_fecha in noches:
        
        noche = [hora for hora in noches_separadas2 if hora[0].strftime('%m-%d') == noche_fecha][0]
        
        duracion_noche2 = (max(noche) - min(noche)).total_seconds() / 60
        
        duracion_total_mes2 += duracion_noche2
    
    duracion_por_mes2[mes] = duracion_total_mes2
    
duracion_total_por_mes3 = {}

for mes, ventana in intervalosvent3.items():
    duracion_total_mes_minutos3 = sum(ventana) * 60  
    duracion_total_por_mes3[mes] = duracion_total_mes_minutos3

duracion_por_mes3 = {}

for mes, noches in noches_en_mes3.items():
    duracion_total_mes3 = 0
    
    for noche_fecha in noches:
        
        noche = [hora for hora in noches_separadas3 if hora[0].strftime('%m-%d') == noche_fecha][0]
        
        duracion_noche3 = (max(noche) - min(noche)).total_seconds() / 60
        
        duracion_total_mes3 += duracion_noche3
    
    duracion_por_mes3[mes] = duracion_total_mes3
    
duracion_total_por_mes4 = {}

for mes, ventana in intervalosvent4.items():
    duracion_total_mes_minutos4 = sum(ventana) * 60  
    duracion_total_por_mes4[mes] = duracion_total_mes_minutos4

duracion_por_mes4 = {}

for mes, noches in noches_en_mes4.items():
    duracion_total_mes4 = 0
    
    for noche_fecha in noches:
        
        noche = [hora for hora in noches_separadas4 if hora[0].strftime('%m-%d') == noche_fecha][0]
        
        duracion_noche4 = (max(noche) - min(noche)).total_seconds() / 60
        
        duracion_total_mes4 += duracion_noche4
        
    duracion_por_mes4[mes] = duracion_total_mes4



ventanas_normalizadas = [duracion_total_por_mes[mes] / duracion_por_mes[mes] for mes in meses]
ventanas_normalizadas2 = [duracion_total_por_mes2[mes] / duracion_por_mes2[mes] for mes in meses2]
ventanas_normalizadas3 = [duracion_total_por_mes3[mes] / duracion_por_mes3[mes] for mes in meses3]
ventanas_normalizadas4 = [duracion_total_por_mes4[mes] / duracion_por_mes4[mes] for mes in meses4]



fig,ax = plt.subplots(figsize=(10,6))

ax.bar(meses, ventanas_normalizadas, edgecolor='lightseagreen', label ="Los Mártires", fill=False, linewidth = 2)
ax.bar(meses2, ventanas_normalizadas2, edgecolor='mediumpurple', label="Usme", fill=False, linewidth = 2)
ax.bar(meses3, ventanas_normalizadas3, edgecolor='indianred', label="Engativa", fill=False, linewidth = 2)
ax.bar(meses4, ventanas_normalizadas4, edgecolor='springgreen', label="Suba", fill=False, linewidth = 2)

ax.set_xlabel('Mes', weight='bold')
ax.set_ylabel('Número de Ventanas Normalizadas', weight='bold')
ax.set_title('Número de Ventanas Normalizadas', weight='bold', fontsize=16)
ax.grid(True)

ax.legend()
plt.show()

fig,ax = plt.subplots(figsize=(10,6))

ax.scatter(duracion_horas, brillo_promedio, color='lightseagreen', label="Los Mártires", marker='o')
ax.scatter(duracion_horas2, brillo_promedio2, color='mediumpurple', label="Usme", marker='s')
ax.scatter(duracion_horas3, brillo_promedio3, color='indianred', label="Engativa", marker='x')
ax.scatter(duracion_horas4, brillo_promedio4, color='springgreen', label="Suba", marker='p')

ax.set_xlabel('Duración de Ventanas (horas)', weight='bold')
ax.set_ylabel('Brillo Promedio Ventanas', weight='bold')
ax.set_title('Brillo Promedio vs Duración Ventanas', weight='bold', fontsize=16)
ax.grid(True)

ax.legend()
plt.show()