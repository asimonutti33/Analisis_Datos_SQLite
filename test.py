# Archivo validacion de código
# Se utiliza para validar que las funciones se ejecutan correctamente
import unittest
from coches import *

nombre_fichero = 'test.csv'

class test_numero_coches_tabla(unittest.TestCase):
    def test(self):
        borrar_datos()
        datos = leer_datos(nombre_fichero)
        conexion = crear_conexion_bd()
        crear_tabla_coches(conexion)
        grabar_coche(conexion, datos)
        dato = numero_coches_tabla(conexion)
        self.assertEqual(2780,dato)


if __name__ == '__main__':
    unittest.main()
