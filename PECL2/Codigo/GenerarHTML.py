import textwrap
import os
from Funcionalidad import *
from Consultas import *

def getFechaHoy():
    fecha = datetime.datetime.now()
    ano = fecha.year
    mes = fecha.month
    dia = fecha.day

class PaginaHTML:
    def __init__(self, sesion, fecha):
        self.__nombre = "Sesion_" + str(sesion) + "_" + fecha
        self.__titulo = "Sesion " + str(sesion) + " - " + fecha
        self.__ruta = "./templates/" + self.__nombre + ".html"

    def crearFichero(self, texto, mediaBPM, cambiosPostura, tiempoSuenno):
        inicioHTML = textwrap.dedent("""\
            <!doctype html>
            <html lang=\"es\">
            <head>
                <meta charset=\"UTF-8\">
                <title>Informe - """ + self.__titulo + """</title>
                <link rel="icon" href="data:;base64,iVBORw0KGgo=">
            </head>
            <body>
                <div style=\"width:800px; margin: 0 auto;\">
                    <h1>Informe - """ + self.__titulo + """</h1>
            """)
        finalHTML = textwrap.dedent("""\
                </div>
            </body>
            </html>
            """)

        # Abrimos el archivo y escribimos el html inicial
        f = open(self.__ruta, "w+", encoding="utf8")
        f.write(inicioHTML)

        # Construimos la parte dinámica de la página HTML
        contenidoHTML = textwrap.dedent("""\
                <div>
                    <hr>
                    <h2>Resumen de tu sueño para esta sesión</h2>
                    <p>""" + texto + """</p>
                    <ul>
                        <li>Media de BPM: <strong>"""+str(mediaBPM)+"""</strong></li>
                        <li>Número de cambios de postura: <strong>"""+str(cambiosPostura)+"""</strong></li>
                        <li>Tiempo de sueño: <strong>"""+str(tiempoSuenno)+"""</strong></li>

                    </ul>
                    <hr>
                    <h2>Gráfico de BPM a lo largo de la noche</h2>
                    <img src=\"/static/images/"""+self.__nombre+"""_bpm.png\" height=\"600\" width=\"800\">
                    <hr>
                    <h2>Gráfico de movimientos a lo largo de la noche</h2>
                    <img src=\"/static/images/"""+self.__nombre+"""_movimientos.png\" height=\"600\" width=\"800\">
                    <hr>
                    <h2>Gráfico de presión sobre los sensores a lo largo de la noche</h2>
                    <img src=\"/static/images/"""+self.__nombre+"""_presiones.png\" height=\"600\" width=\"800\">
                </div>
            """)
        f.write(contenidoHTML)

        # Cerramos el archivo html y cerramos el fichero
        f.write(finalHTML)
        f.close()


if __name__ == "__main__":
    # Pruebas, no ejecutar
  bbdd = BaseDatos()
  # bbdd.getFechaSesion(1)
  bbdd.insertarInforme("Indice de informe de sesion"+str(1), 1)
  estado, media_bpm, cambios, tpo_sueno = generaInforme(1)
  p = PaginaHTML(1, "2020-01-08")
  p.crearFichero(estado, media_bpm, cambios, tpo_sueno)
