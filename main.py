import eel
from Backend.VentaDAO import VentaDAO

dao = VentaDAO()

@eel.expose
def buscar_producto(codigo):
    return dao.buscarProducto(codigo)

@eel.expose
def guardar_venta(subtotal, iva, total, lista_productos):
    return dao.procesarVenta(subtotal, iva, total, lista_productos)

@eel.expose
def obtener_siguiente_folio():
    return dao.obtenerSiguienteFolio()

if __name__ == "__main__":
    eel.init('Fronted')
    eel.start('frm_principal.html', cmdline_args=['--start-maximized'])

