import matplotlib.pyplot as plt
import pandas as pd
from Consultas import *
import datetime as dt
import numpy as np
import matplotlib.dates as mdates
import datetime
import string

from Consultas import BaseDatos
from GenerarHTML import PaginaHTML
import Consultas
from Fecha import Fecha


def strToDt(fecha_str):
    dt = datetime.datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    return dt


def generarInforme(datos_hora):
    '''Recibe: una lista con los datos recabados en 1h y el numero de hora
    Devuelve: una lista de 6 elementos con formato [hora, bmps, veces_movidas] correspondiente a espacios  de 10 min en la hora'''
    movimientos = []
    bpms = []
    movido = False
    fecha_inicial = Fecha(datos_hora[0][0])
    presiones = []

    # Recogida de datos
    for tupla in datos_hora:
        fecha = datetime.datetime.strptime(tupla[0], '%Y-%m-%d %H:%M:%S')
        presion_anterior = [datos_hora[0][1],
                            datos_hora[0][2], datos_hora[0][3]]
        movs = 0
        for tupla in datos_hora:
            presion_actual = [tupla[1], tupla[2], tupla[3]]
            presiones.append([fecha, tupla[1], tupla[2], tupla[3]])
            for e in range(3):
                # Para evitar una division por 0 al calcular "razon"
                if presion_anterior[e] == 0:
                    presion_anterior[e] += 1

                razon = presion_actual[e] / presion_anterior[e]

                # Los movimientos se detectan con un cambio de presión del 20% minimo en cualquier sensor
                if razon > 1.2 or razon < 0.8 and razon != 0:
                    movido = True

                presion_anterior[e] = presion_actual[e]

            bpms.append([datetime.datetime.strptime(tupla[0], '%Y-%m-%d %H:%M:%S'),
                         tupla[4]])  # Nuevo dato para la lista bpms

        if (movido):
            movimientos.append(datetime.datetime.strptime(
                tupla[0], '%Y-%m-%d %H:%M:%S'))
            movido = False  # Por defecto el usuario no se mueve a menos que lo detecte

    resultado = [[0, 0, 0, 0, 0] for i in range(6)]

    for movimiento in movimientos:
        minuto = int(movimiento.minute / 10)
        resultado[minuto][1] += 1

    veces = [0 for i in range(6)]
    for bpm in bpms:
        minuto = int(bpm[0].minute / 10)
        veces[minuto] += 1
        resultado[minuto][0] += bpm[1]

    veces2 = [0 for i in range(6)]
    for actual in presiones:
        minuto = int(actual[0].minute / 10)
        veces2[minuto] += 1
        resultado[minuto][2] += actual[1]
        resultado[minuto][3] += actual[2]
        resultado[minuto][4] += actual[3]

    for i in range(6):
        if (veces[i] != 0):
            resultado[i][0] /= veces[i]

        if (veces2[i] != 0):
            resultado[i][2] /= veces2[i]
            resultado[i][3] /= veces2[i]
            resultado[i][4] /= veces2[i]

    resultado_bis = []
    fecha_inicial.minutos = 0
    for elem in resultado:
        dtfecha = fecha_inicial.toDt()
        listafecha = [dtfecha]
        resultado_bis.append(listafecha + elem)
        fecha_inicial.minutos += 10
        # [hora, bpms, movimientos]
    return resultado_bis


def separar_datos_por_horas(datos, horaInicial, horaFinal):
    """
    Separa los datos de una sesión por horas, y lo devuelve en una lista. 
    """
    datos_segun_hora = []
    inicio = horaInicial.timetuple().tm_hour
    final = horaFinal.timetuple().tm_hour+1
    for hora in range(inicio, final):
        datos_segun_hora.append(getDatosHora(datos, hora))
    return datos_segun_hora


def getDatosHora(datos, hora):
    """ 
    Devuelve todos los datos de una hora concreta en el conjunto de datos de una sesión
    """
    datos_hora = []
    for dato in datos:
        fecha_dt = strToDt(dato[0])
        dt_tupla = fecha_dt.timetuple()
        dt_hora = dt_tupla.tm_hour
        if(dt_hora == hora):
            datos_hora.append(dato)
    return datos_hora


def informes_por_hora(datos_por_hora):
    """
    Dados los datos separados según la hora, genera los informes de cada hora. 
    """
    informes = []
    contador = 0
    for datos_hora in datos_por_hora:
        contador += 1
        informes.append(generarInforme(datos_hora))
    return informes


def generar_informe_sesion(bbdd, idSesion):
    """
    Dada una sesión con su id, genera los informes de la sesión, divididos por horas. 
    """
    datos = bbdd.getDatosSesion(1)
    inicio = bbdd.getHoraInicial(1)
    final = bbdd.getHoraFinal(1)
    datos_horas = separar_datos_por_horas(datos, inicio, final)
    return informes_por_hora(datos_horas)


# Esta funcion devuelve [media_bpm, tiempo_sueño_min, cambios_postura]
def medidas_relevantes(informe):
    bpm, frecuencia_bpm = 0, 0
    cambios_postura = 0
    tiempo_suenno = 0

    for diezminutos in informe:
        bpm_actual = diezminutos[1]
        cambios_postura_actual = diezminutos[2]
        if(bpm_actual != 0):
            cambios_postura += cambios_postura_actual
            bpm += bpm_actual
            frecuencia_bpm += 1
            if(bpm_actual < 45):
                tiempo_suenno += 10

    return [float(bpm)/frecuencia_bpm, tiempo_suenno, cambios_postura]


def rellenar_huecos(valores, rango):
    valores_rellenados = []
    valores_rellenados.append(0)
    for i in range(len(valores)):
        valores_rellenados.append(valores[i])
        if(i < (len(valores)-1)):
            valores_rellenados.append((valores[i]+valores[i+1])/2)
            valores_rellenados.append((valores[i]+valores[i+1])/2)
    if(len(valores_rellenados) != len(rango)):
        if(len(valores_rellenados)>len(rango)):
            while(len(valores_rellenados)!=len(rango)):
                valores_rellenados.pop()
        else:
            while(len(valores_rellenados) != len(rango)):
                valores_rellenados.append(0)
    return valores_rellenados


def generarGraficoBpm(idSesion):
    bbdd = BaseDatos()
    datos = bbdd.getPulsacionesSesion(idSesion)
    fechas = []
    valores = []

    for dato in datos:
        fecha = dato[0]
        fecha_dt = dt.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        fechas.append(fecha_dt)
        valores.append(dato[1])

    now = fechas[-1]
    then = fechas[0]
    rango = mdates.drange(then, now, dt.timedelta(seconds=1))
    y = rellenar_huecos(valores, rango)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H-%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
    plt.gca().set_ylim([0, max(y)+20])
    plt.plot(rango, y)
    #plt.show()
    plt.gcf().autofmt_xdate()

    fecha_sesion = fechas[int(len(valores)/2)]
    fecha_sesion = fecha_sesion.timetuple()
    ano = str(fecha_sesion.tm_year)
    mes = fecha_sesion.tm_mon
    if(mes < 10):
        mes=str(0)+str(mes)
    else:
        mes=str(mes)
    dia = fecha_sesion.tm_mday
    if(dia < 10):
        dia=str(0)+str(dia)
    else:
        dia=str(dia)
    
    fecha = (ano+"-"+mes+"-"+dia+"")

    plt.savefig("static/images/Sesion_"+str(idSesion)+"_"+fecha+"_"+"bpm")
    plt.cla()
    return fecha


def generarGraficoMovimientos(idSesion, informes, fecha_sesion):
    informes_por_hora = informes
    todos_los_informes_juntos = []
    for informe in informes_por_hora:
        for diezminutos in informe:
            todos_los_informes_juntos.append(diezminutos)

    fechas = []
    bpms = []
    movimientos = []

    for subinforme in todos_los_informes_juntos:
        fechas.append(subinforme[0])
        bpms.append(subinforme[1])
        movimientos.append(subinforme[2])

    df = pd.DataFrame({'x': fechas, 'Media BPM': bpms,
                       'Movimientos': movimientos})

    # multiple line plot
    plt.plot('x', 'Media BPM', data=df, marker='o',
             markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    plt.plot('x', 'Movimientos', data=df,
             marker='', color='olive', linewidth=2)
    plt.xticks(rotation=90)
    plt.legend()
    plt.savefig("static/images/Sesion_"+str(idSesion) +
                "_"+fecha_sesion+"_"+"movimientos")
    plt.cla()


def generarGraficoPresiones(idSesion, informes, fecha_sesion):
    informes_por_hora = informes
    todos_los_informes_juntos = []
    for informe in informes_por_hora:
        for diezminutos in informe:
            todos_los_informes_juntos.append(diezminutos)

    fechas = []
    presion1 = []
    presion2 = []
    presion3 = []

    for subinforme in todos_los_informes_juntos:
        fechas.append(subinforme[0])
        presion1.append(subinforme[3])
        presion2.append(subinforme[4])
        presion3.append(subinforme[5])

    df = pd.DataFrame({'x': fechas, 'Sensor1': presion2,
                       'Sensor2': presion1, 'Sensor3': presion3})

    # multiple line plot
    plt.plot('x', 'Sensor1', data=df, marker='',
             color='green',  linestyle='dashed', linewidth=2)
    plt.plot('x', 'Sensor2', data=df, marker='',
             color='orange', linestyle='dashed', linewidth=2)
    plt.plot('x', 'Sensor3', data=df, marker='',
             color='olive', linestyle='dashed', linewidth=2)
    plt.xticks(rotation=90)
    plt.legend()

    plt.savefig("static/images/Sesion_"+str(idSesion) +
                "_"+fecha_sesion+"_"+"presiones")
    plt.cla()


def texto(medidas_relevantes):  # Este texto deberia salir por el HTML
    res = ""
    bpm, tiempo_suenno, cambios_postura = medidas_relevantes[
        0], medidas_relevantes[1], medidas_relevantes[2]
    if(tiempo_suenno < 600):
        res += "Has dormido demasiado poco.\n"
    else:
        res += "Has dormido un tiempo correcto.\n"

    if(cambios_postura > 500):
        res += "Tu sueño ha sido agitado, te has movido mucho.\n"
    else:
        res += "No te has movido mucho al dormir.\n"

    if(bpm > 85):
        res += "No has entrado en sueño profundo, deberías hacer más ejercicio por cierto.\n"
    else:
        res += "No has entrado en sueño profundo"

    return res

def generarGraficos(idSesion, informes_por_hora):
    fecha_sesion = generarGraficoBpm(idSesion)
    generarGraficoMovimientos(idSesion, informes_por_hora, fecha_sesion)
    generarGraficoPresiones(idSesion, informes_por_hora, fecha_sesion)


def generaInforme(idSesion):
    bbdd = BaseDatos()
    print("Conectada base de datos. ")
    print("Estudiando informes...")
    informes_por_hora = generar_informe_sesion(bbdd, idSesion)
    print("Generando gráficos...")
    generarGraficos(idSesion, informes_por_hora)
    todos_los_informes_juntos = []
    for informe in informes_por_hora:
        for diezminutos in informe:
            todos_los_informes_juntos.append(diezminutos)
    print("Generando medidas relevantes...")
    media_bpm, tiempo_sueno, cambios_postura = medidas_relevantes(todos_los_informes_juntos)
    estado = texto([media_bpm, tiempo_sueno, cambios_postura])
    print("Completado: está bien. ")
    return estado, media_bpm, tiempo_sueno, cambios_postura
