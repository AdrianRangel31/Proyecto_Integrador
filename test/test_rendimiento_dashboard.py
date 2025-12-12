import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.ventasCRUD import reportes

def test_rendimiento():
    print("=== INICIANDO PRUEBA DE RENDIMIENTO: DASHBOARD (PD-01) ===")
    
    print("\n[PASO 1] Midiendo tiempo de consulta para Gráfico de Ingresos (Semanal)...")
    
    inicio = time.time()
    datos_ingresos = reportes.obtener_ingresos_grafico("Semanal")
    fin = time.time()
    
    tiempo_ingresos = fin - inicio
    print(f"   -> Tiempo de respuesta BD (Ingresos): {tiempo_ingresos:.4f} segundos")
    
    print("\n[PASO 2] Midiendo tiempo de consulta para Gráfico de Ventas por Producto...")
    
    inicio = time.time()
    datos_ventas = reportes.obtener_datos_grafico("Semanal")
    fin = time.time()
    
    tiempo_ventas = fin - inicio
    print(f"   -> Tiempo de respuesta BD (Productos): {tiempo_ventas:.4f} segundos")
    
    tiempo_total = tiempo_ingresos + tiempo_ventas
    print(f"\n[RESULTADO] Tiempo total de carga de datos: {tiempo_total:.4f} segundos")
    
    if tiempo_total <= 2.0:
        print("✅ PD-01 PASÓ: El tiempo de carga es menor a 2 segundos.")
    else:
        print(f"❌ PD-01 FALLÓ: El sistema es lento ({tiempo_total}s > 2.0s).")

    print("=== PRUEBA FINALIZADA ===")

if __name__ == "__main__":
    test_rendimiento()