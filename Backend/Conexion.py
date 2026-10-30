import mysql.connector
from mysql.connector import Error

class Conexion():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'aplicacion_pdv'
        self.database = 'punto_venta'
        self.password = 'edu123'
        self.conexion = None

    def conectar(self):

        try:
            if self.conexion is None:
                self.conexion = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    database=self.database,
                    password=self.password
                )
            return self.conexion
        except Error as e:
            print(e)
            return None

    def desconectar(self):
        if self.conexion.is_connected():
            self.conexion.close()
