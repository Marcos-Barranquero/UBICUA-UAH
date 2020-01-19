import datetime


class Fecha:
    def __init__(self, fecha_str):
        dt = datetime.datetime.strptime(
            fecha_str, "%Y-%m-%d %H:%M:%S")
        dt = dt.timetuple()
        self.ano = dt.tm_year
        self.mes = dt.tm_mon
        self.dia = dt.tm_mday
        self.hora = dt.tm_hour
        self.minutos = dt.tm_min
        self.segundos = dt.tm_sec

    def toDt(self):
        return datetime.datetime(self.ano, self.mes, self.dia, self.hora, self.minutos, self.segundos)
        

if __name__ == "__main__":
    fecha = "2020-01-07 18:15:27"
    x = Fecha(fecha)
    print(x.ano)
