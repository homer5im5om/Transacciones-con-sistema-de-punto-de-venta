from Backend.Conexion import Conexion

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
            cursor = None
            try:
                cursor = Connect.cursor(dictionary=True)
                sql = """select codigodebarras, descripcion, precio, stock from productos where codigodebarras = %s"""
                cursor.execute(sql, (codigodebarras,))
                producto = cursor.fetchone()

                if producto:
                    producto['precio'] = float(producto['precio'])

            except Exception as e:
                print(e)
            finally:
                if cursor is not None:
                    cursor.close()
                self.db.desconectar()
        return producto

    def procesarVenta(self, subtotal, iva, total, lista_productos):

        Connect = self.db.conectar()
        if not Connect:
            return False

        try:
            cursor = Connect.cursor()
            Connect.start_transaction()

            sql_venta = "insert into venta (subtotal, iva, total) values (%s, %s, %s)"
            cursor.execute(sql_venta, (subtotal, iva, total))
            id_venta = cursor.lastrowid

            sql_detalle = """insert into detalle_venta
                                 (id_venta, codigodebarras, cantidad, unit_price, importe)
                             values (%s, %s, %s, %s, %s)"""
            sql_stock = "update productos set stock = stock - %s where codigodebarras = %s"

            for item in lista_productos:
                cursor.execute(sql_detalle, (id_venta, item['codigodebarras'], item['cantidad'], item['unit_price'],
                                             item['importe']))

                cursor.execute(sql_stock, (item['cantidad'], item['codigodebarras']))

            Connect.commit()
            return True

        except Exception as e:
            Connect.rollback()
            print(e)
            return False

        finally:
            cursor.close()
            self.db.desconectar()

    def obtenerSiguienteFolio(self):
        Connect = self.db.conectar()
        siguiente_folio = 1
        if Connect:
            try:
                cursor = Connect.cursor()
                cursor.execute("SELECT MAX(id_venta) FROM venta")
                resultado = cursor.fetchone()

                if resultado[0] is not None:
                    siguiente_folio = resultado[0] + 1

            except Exception as e:
                print(e)
            finally:
                cursor.close()
                self.db.desconectar()
        return siguiente_folio