from lector_miband import *
from lector_presion import *
from threading import Thread
from Consultas import *
import sys
from Funcionalidad import *
# Inicializo lector de presión
mcp = inicializar()

canales = get_canales(mcp)
# Inicializo mi band en un hilo aparte porque la lectura es bloqueante
band = inicializar_mi_band()
lectura = Thread(target=iniciar_lectura_bpm, args=[band])
lectura.start()

# Cargo bbdd
bbdd = BaseDatos()

# La mi band tarda un poco en arrancar, así que hasta que no lo haga no empezamos a leer...
while(band.ultimo_bpm < 0):
    sleep(5)

# Una vez cargada, obtengo nueva id de sesion
id_sesion = bbdd.getUltimaSesion() + 1

while(band.ultimo_bpm != 0):
    presion1 = get_valor(0, canales)    
    presion2 = get_valor(1, canales)
    presion3 = get_valor(2, canales)

    print('Valor C1: ', presion1)
    print('Valor C2: ', presion2)   
    print('Valor C3: ', presion3)
    print('BPM: ', band.ultimo_bpm)
    bbdd.insertarLectura(presion1, presion2, presion3, band.ultimo_bpm, id_sesion)
    sleep(3)

print("El usuario se ha quitado la pulsera. Fin de la recogida de datos. ")
bbdd = BaseDatos()
fecha = bbdd.getFechaSesion(id_sesion)
bbdd.insertarInforme("Indice de informe de sesion"+str(id_sesion), id_sesion)
estado, media_bpm, cambios, tpo_sueno = generaInforme(id_sesion)
p = PaginaHTML(id_sesion, fecha)
p.crearFichero(estado, media_bpm, cambios, tpo_sueno)