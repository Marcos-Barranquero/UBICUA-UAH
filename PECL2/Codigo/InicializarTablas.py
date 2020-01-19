import sqlite3

############### Configuracion ####################
# Nombre de la base de datos
DB_NAME = "datosPECL"

# Archivo SQL con la definicion de las tablas
SQL_File_Name = "CrearTablas.sql"
##############################################

# Se carga el archivo SQL a una variable y se eliminan los saltos de linea
TableSchema=""
with open(SQL_File_Name, 'r') as SchemaFile:
    TableSchema=SchemaFile.read().replace('\n', '')

# Se crea la nueva base de datos
conn = sqlite3.connect(DB_NAME)
curs = conn.cursor()

# Se lanza la consulta de creacion de tablas
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

# Se cierra la conexion con la base de datos
curs.close()
conn.close()