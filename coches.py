import sqlite3
import sys
from os import remove
from zipfile import ZipFile
import pandas as pd
from sqlite3 import Error

# Nombre de la base de datos SQLite
basededatos = 'coches.bd'

# Función para calcular el precio medio de los coches por marca
def precio_medio_por_marca(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT marca, AVG(precio) FROM coches GROUP BY marca")
    datos = cursor.fetchall()
    return datos

# Función para obtener la marca, modelo y precio del coche más barato
def marca_coche_mas_barato(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT marca, modelo, MIN(precio) FROM coches")
    datos = cursor.fetchall()
    return datos

# Función para calcular el precio total de todos los coches
def precio_total_coches(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT SUM(precio) FROM coches")
    dato = cursor.fetchall()
    numero = dato[0][0]
    return numero

# Función para contar el número de coches en la tabla
def numero_coches_tabla(conexion):
    cursor = conexion.cursor()
    cursor.execute('SELECT COUNT(*) FROM coches')
    dato = cursor.fetchall()
    numero = dato[0][0]
    return numero

# Función para mostrar los primeros 20 coches de la tabla
def consultar_coches(conexion):
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM coches LIMIT 20')
    filas = cursor.fetchall()
    for fila in filas:
        print(fila)

# Función para borrar el archivo de base de datos si existe
def borrar_datos():
    try:
        remove(basededatos)
    except FileNotFoundError:
        pass

# Función para insertar un coche en la tabla de coches
def insertar_tabla_coche(conexion, coche):
    cursor = conexion.cursor()
    cursor.execute(
        'INSERT INTO coches(marca, modelo, combustible, transmision, estado, matriculacion, kilometraje, potencia, precio) VALUES(?,?,?,?,?,?,?,?,?)',
        coche)
    conexion.commit()

# Función para grabar los datos de los coches en la tabla
def grabar_coche(conexion, datos):
    for fila in datos.itertuples():
        marca = fila[1]
        modelo = fila[2]
        combustible = fila[3]
        transmision = fila[4]
        estado = fila[5]
        matriculacion = fila[6]
        kilometraje = fila[7]
        potencia = fila[8]
        precio = fila[9]

        coche = (marca, modelo, combustible, transmision, estado, matriculacion, kilometraje, potencia, precio)

        insertar_tabla_coche(conexion, coche)

# Función para crear la tabla de coches en la base de datos
def crear_tabla_coches(conexion):
    cursor = conexion.cursor()
    cursor.execute(
        'CREATE TABLE coches(marca text, modelo text, combustible text, transmision text, estado text, matriculacion text, kilometraje int, potencia real, precio real)')
    conexion.commit()

# Función para crear una conexión a la base de datos
def crear_conexion_bd():
    try:
        conexion = sqlite3.connect(basededatos)
        return conexion
    except Error:
        print(Error)

# Función para leer datos desde un archivo CSV
def leer_datos(nombre):
    datos = pd.read_csv(nombre, sep=';')
    return datos

# Función para descomprimir un archivo ZIP
def descomprimir_fichero(nombre):
    with ZipFile(nombre, 'r') as zip:
        zip.extractall()

# Punto de entrada principal
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error. Número incorrecto de parámetros.")
    else:
        nombre_fichero = sys.argv[1]

        borrar_datos()

        descomprimir_fichero(nombre_fichero)

        datos = leer_datos(nombre_fichero)
        print(datos)

        conexion = crear_conexion_bd()

        crear_tabla_coches(conexion)

        grabar_coche(conexion, datos)

        print("\nConsultamos los datos de la tabla")
        consultar_coches(conexion)

        dato = numero_coches_tabla(conexion)
        print("\nEl número de coches es: {}".format(dato))

        numero = precio_total_coches(conexion)
        dinero = '{:,}'.format(numero).replace(',', '.')
        print("\nEl precio total de los coches es: {}".format(numero))

        datos = marca_coche_mas_barato(conexion)
        marca = datos[0][0]
        modelo = datos[0][1]
        precio = datos[0][2]
        print("\nCoches más baratos. Marca = {}, modelo = {}, precio = {}".format(marca, modelo, precio))

        print("\nPrecio medio por marca\n")
        datos = precio_medio_por_marca(conexion)
        for dato in datos:
            marca = dato[0]
            precio = dato[1]
            print(marca, precio)
