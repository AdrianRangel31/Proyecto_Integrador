import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controller.reportes import GeneradorPDF
from model.productosCRUD import Productos

def test_generacion_reporte():
    print("=== INICIANDO PRUEBA DE INTEGRACIÓN: REPORTES (PI-01) ===")
    
    nombre_archivo = "Reporte_Prueba_Integracion.pdf"
    titulo_reporte = "REPORTE DE PRUEBA AUTOMATIZADA"
    
    print(f"\n[PASO 1] Obteniendo datos reales de la base de datos...")
    datos = Productos.buscar() # Obtiene todos los productos
    
    if len(datos) > 0:
        print(f"✅ Conexión BD exitosa. Se obtuvieron {len(datos)} registros.")
    else:
        print("⚠️ Advertencia: La BD está vacía, el reporte saldrá en blanco pero se probará la generación.")

    print(f"\n[PASO 2] Generando archivo PDF: {nombre_archivo}")
    
    try:
        pdf = GeneradorPDF(nombre_archivo, titulo_reporte)
        pdf.generar_encabezado()
        pdf.generar_tabla(datos)
        pdf.guardar()
        
        # Verificar que el archivo existe en el disco
        if os.path.exists(nombre_archivo):
            peso = os.path.getsize(nombre_archivo)
            print(f"✅ PI-01 PASÓ: El archivo se creó exitosamente ({peso} bytes).")
            print(f"   Ubicación: {os.path.abspath(nombre_archivo)}")
        else:
            print("❌ PI-01 FALLÓ: El archivo no aparece en el sistema de archivos.")
            
    except Exception as e:
        print(f"❌ PI-01 FALLÓ con excepción: {e}")

    print("=== PRUEBA FINALIZADA ===")

if __name__ == "__main__":
    test_generacion_reporte()