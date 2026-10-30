from Conexion import Conexion

class VentaDAO():
    def __init__(self):
        self.db = Conexion()

    def insertarDatos(self,codigodebarras,descripcion,precio,stock):
        Connect = self.db.conectar()

        if Connect:
            try:
                cursor = Connect.cursor()

                sql = """insert into productos (codigodebarras, descripcion , precio, stock) values (%s,%s,%s,%s)"""

                cursor.execute(sql, (codigodebarras,descripcion,precio,stock))
                Connect.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                self.db.desconectar()


    def buscarProducto(self,codigodebarras):
        Connect = self.db.conectar()
        producto = None
        if Connect:
            try:
                cursor = Connect.cursor(dictionary=True)

                sql = """select codigodebarras, descripcion, precio, stock from productos where codigodebarras = %s"""

                cursor.execute(sql, (codigodebarras,))

                producto = cursor.fetchone()

            except Exception as e:
                print(e)
            finally:
                cursor.close()
                self.db.desconectar()
        return producto