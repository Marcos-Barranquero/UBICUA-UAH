import sqlite3
import time
from time import sleep
import datetime


class BaseDatos:
    def __init__(self):
        self.__conexion = sqlite3.connect("datosPECL")

    def insertarLectura(self, presion1, presion2, presion3, pulsaciones, sesion):
        """
            Inserta una nueva lectura en la base de datos con los datos 
            de presiones y pulsaciones que se le pasan como parametro
        """
        try:
            cursor = self.__conexion.cursor()
            cursor.execute("INSERT INTO LecturasSensores VALUES(?, ?, ?, ?, ?, ?)", [
                           int(time.time()), presion1, presion2, presion3, pulsaciones, sesion])
            self.__conexion.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error al insertar: ", error)

    def insertarInforme(self, texto, sesion):
        """
            Inserta un informe nuevo con el texto que se le pasa
            como parametro
        """
        try:
            cursor = self.__conexion.cursor()
            cursor.execute("INSERT INTO Informes VALUES(?, ?, ?)", [
                           int(time.time()), texto, sesion])
            self.__conexion.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error al insertar: ", error)

    def consultarLecturas(self, horas):
        """
            Recupera las lecturas de todos los sensores guardadas en las ultimas horas
            Las horas se le pasan como parametro
        """
        try:
            cursor = self.__conexion.cursor()
            # Se le suma 1 hora para que este en nuestra franja horaria
            cursor.execute("SELECT datetime(fecha + 3600, 'unixepoch'), presion1, presion2, presion3, pulsaciones, sesion FROM LecturasSensores WHERE fecha >= " +
                           str(int(time.time() - 3600 * horas)))
            self.__conexion.commit()
            datos = cursor.fetchall()
            cursor.close()

            return datos

        except sqlite3.Error as error:
            print("Error al consultar la base de datos: ", error)

    def consultarUltimoInforme(self):
        """
            Devuelve el ultimo informe generado
        """
        try:
            cursor = self.__conexion.cursor()
            # Se le suma 1 hora para que este en nuestra franja horaria
            cursor.execute(
                "SELECT datetime(fecha + 3600, 'unixepoch'), datos, sesion FROM Informes ORDER BY fecha DESC LIMIT 1")
            self.__conexion.commit()
            datos = cursor.fetchall()
            cursor.close()

            return datos

        except sqlite3.Error as error:
            print("Error al consultar la base de datos: ", error)

    def consultarInformes(self):
        """
            Devuelve todos los informes almacenados en la base de datos
            ordenados de mas reciente a mas antiguo
        """
        try:
            cursor = self.__conexion.cursor()
            # Se le suma 1 hora para que este en nuestra franja horaria
            cursor.execute(
                "SELECT datetime(fecha + 3600, 'unixepoch'), datos, sesion FROM Informes ORDER BY fecha DESC")
            self.__conexion.commit()
            datos = cursor.fetchall()
            cursor.close()

            return datos

        except sqlite3.Error as error:
            print("Error al consultar la base de datos: ", error)

    def getUltimaSesion(self):
        """ 
        Devuelve el id de la última sesión registrada.
        """
        try:
            cursor = self.__conexion.cursor()
            cursor.execute("SELECT MAX(sesion) FROM LecturasSensores")
            self.__conexion.commit()
            datos = cursor.fetchall()
            cursor.close()
            id_sesion = datos[0][0]
            if(id_sesion is None):
                id_sesion = 0
            return id_sesion
        except sqlite3.Error as error:
            print("Error al consultar la base de datos: ", error)

    def getPulsacionesSesion(self, idSesion):
        """
        Dada una id de sesión, devuelve una lista de tuplas (hora, bpm) de esa sesión
        """
        try:
            cursor = self.__conexion.cursor()
            cursor.execute(
                "SELECT datetime(fecha + 3600, 'unixepoch'), pulsaciones FROM LecturasSensores WHERE sesion = " + str(idSesion) + " ORDER BY fecha ASC")
            self.__conexion.commit()
            datos = cursor.fetchall()
            cursor.close()
            return datos
        except sqlite3.Error as error:
            print("Error al consultar la base de datos: ", error)

    def getDatosSesion(self, idSesion):
        """
        Dada una id de sesión, devuelve una lista de todos los datos recogidos de esa sesión
        """
        try:
            cursor = self.__conexion.cursor()
            cursor.execute(
                "SELECT datetime(fecha + 3600, 'unixepoch'), presion1, presion2, presion3, pulsaciones, sesion FROM LecturasSensores WHERE sesion = " + str(idSesion) + " ORDER BY fecha ASC")
            self.__conexion.commit()
            datos = cursor.fetchall()
            cursor.close()
            return datos
        except sqlite3.Error as error:
            print("Error al consultar la base de datos: ", error)

    def getHoraInicial(self, idSesion):
        """
        Dada una id de sesión, devuelve la hora de inicio de esa sesión
        """
        try:
            cursor = self.__conexion.cursor()
            cursor.execute(
                "SELECT min(datetime(fecha + 3600, 'unixepoch')) FROM LecturasSensores WHERE sesion = " + str(idSesion))
            self.__conexion.commit()
            datos = cursor.fetchall()
            cursor.close()
            fecha = datos[0][0]
            fecha_dt = dt = datetime.datetime.strptime(
                fecha, "%Y-%m-%d %H:%M:%S")
            return fecha_dt
        except sqlite3.Error as error:
            print("Error al consultar la base de datos: ", error)

    def getFechaSesion(self, idSesion):
        """
        Dada una id de sesión, devuelve la fecha de esa sesión
        """
        try:
            cursor = self.__conexion.cursor()
            cursor.execute(
                "SELECT max(datetime(fecha + 3600, 'unixepoch')) FROM LecturasSensores WHERE sesion = " + str(idSesion))
            self.__conexion.commit()
            datos = cursor.fetchall()
            cursor.close()
            fecha = datos[0][0]
            return fecha.split(" ")[0]
        except sqlite3.Error as error:
            print("Error al consultar la base de datos: ", error)

    def getHoraFinal(self, idSesion):
        """
        Dada una id de sesión, devuelve la hora de inicio de esa sesión
        """
        try:
            cursor = self.__conexion.cursor()
            cursor.execute(
                "SELECT max(datetime(fecha + 3600, 'unixepoch')) FROM LecturasSensores WHERE sesion = " + str(idSesion))
            self.__conexion.commit()
            datos = cursor.fetchall()
            cursor.close()
            fecha = datos[0][0]
            fecha_dt = dt = datetime.datetime.strptime(
                fecha, "%Y-%m-%d %H:%M:%S")
            return fecha_dt
        except sqlite3.Error as error:
            print("Error al consultar la base de datos: ", error)


# Tests
if __name__ == "__main__":
    b = BaseDatos()
    x = b.getDatosSesion(1)
    for e in x:
        print(e)
