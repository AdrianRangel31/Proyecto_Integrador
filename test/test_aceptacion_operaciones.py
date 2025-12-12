import sys
import os
from datetime import date
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.ventasCRUD import ventas, detalleVenta

def test_dia_operaciones():
    print("=== INICIANDO PRUEBA DE ACEPTACIÓN: DÍA COMPLETO (UAT-01) ===")
    
    # Datos simulados de 3 ventas
    ventas_simuladas = [
        {"total": 150.00, "hora": "12:30", "items": [("Hamburguesa sencilla", 2)]},
        {"total": 200.00, "hora": "14:00", "items": [("Hamburguesa doble", 1), ("Refresco", 2)]},
        {"total": 50.00,  "hora": "18:45", "items": [("Hot dog", 2)]}
    ]
    
    fecha_hoy = date.today()
    exitos = 0
    
    print(f"\nSimulando {len(ventas_simuladas)} transacciones para la fecha {fecha_hoy}...")
    
    for i, venta in enumerate(ventas_simuladas, 1):
        print(f"\n--- Procesando Venta #{i} ({venta['hora']}) ---")
        
        # 1. Insertar Venta
        ok_venta, id_venta = ventas.insertar(venta['total'], fecha_hoy, venta['hora'])
        
        if ok_venta and id_venta:
            print(f"   ✅ Venta registrada con ID: {id_venta}")
            
            # 2. Insertar Detalles
            detalles_ok = True
            for producto, cantidad in venta['items']:
                ok_det = detalleVenta.insertar(id_venta, producto, cantidad)
                if ok_det:
                    print(f"      -> Agregado: {cantidad} x {producto}")
                else:
                    print(f"      ❌ Error al agregar {producto}")
                    detalles_ok = False
            
            if detalles_ok:
                exitos += 1
        else:
            print("   ❌ Error al registrar la venta.")

    print("\n[RESULTADOS]")
    if exitos == len(ventas_simuladas):
        print("✅ UAT-01 PASÓ: Se registró el flujo completo de operaciones sin errores.")
    else:
        print(f"⚠️ UAT-01 OBSERVACIÓN: Se registraron {exitos}/{len(ventas_simuladas)} ventas correctamente.")

    print("=== PRUEBA FINALIZADA ===")

if __name__ == "__main__":
    test_dia_operaciones()