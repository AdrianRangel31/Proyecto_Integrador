import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.productosCRUD import Productos
from model.proveedoresCRUD import Proveedores
import time

def test_inventario():
    print("=== INICIANDO PRUEBA FUNCIONAL: GESTIÓN DE INVENTARIO (PF-01, PF-02) ===")
    
    # 1. Preparar datos de prueba
    nombre_prod = "Producto Test Prueba"
    desc = "Prueba automatizada"
    cantidad_inicial = 50.0
    cantidad_final = 40.0 # Simula salida de 10 unidades
    unidad = "piezas"
    precio = 100.0
    caducidad = "2025-12-31"
    
    # Necesitamos un proveedor existente o usamos el ID 1
    id_proveedor = 1 
    
    print(f"\n[PASO 1] Intentando registrar producto: {nombre_prod}")
    
    # PF-01: Registrar nuevo producto
    resultado_insert = Productos.insertar(nombre_prod, desc, cantidad_inicial, unidad, precio, caducidad, id_proveedor)
    
    if resultado_insert:
        print("✅ PF-01 PASÓ: El sistema guardó el producto correctamente.")
    else:
        print("❌ PF-01 FALLÓ: No se pudo insertar.")
        return

    # Verificamos obteniendo el ID del producto recién creado (buscando por nombre)
    datos = Productos.buscar("Nombre", nombre_prod)
    if not datos:
        print("❌ Error: No se encuentra el producto insertado para continuar la prueba.")
        return
    
    producto_registrado = datos[0] # Tomamos el primero que coincida
    id_prod = producto_registrado[0]
    print(f"   -> Producto registrado con ID: {id_prod} | Stock actual: {producto_registrado[3]}")

    # PF-02: Registrar salida de insumo (Actualizar stock)
    print(f"\n[PASO 2] Registrando salida de insumo (De {cantidad_inicial} a {cantidad_final})")
    
    resultado_update = Productos.actualizar(id_prod, nombre_prod, desc, cantidad_final, unidad, precio, caducidad, id_proveedor)
    
    if resultado_update:
        # Verificar cambio
        datos_nuevos = Productos.buscar("ID", id_prod)
        stock_actual = float(datos_nuevos[0][3])
        if stock_actual == cantidad_final:
             print(f"✅ PF-02 PASÓ: El sistema descontó la cantidad correctamente. Stock actual: {stock_actual}")
        else:
             print(f"⚠️ PF-02 ALERTA: Se actualizó pero el stock no coincide. Leído: {stock_actual}")
    else:
        print("❌ PF-02 FALLÓ: No se pudo actualizar el stock.")

    # Limpieza (Opcional: Eliminar el producto de prueba para no ensuciar la BD)
    print("\n[LIMPIEZA] Eliminando datos de prueba...")
    Productos.eliminar(id_prod)
    print("=== PRUEBA FINALIZADA ===")

if __name__ == "__main__":
    test_inventario()