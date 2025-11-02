"""
Script para crear la base de datos EPP
Ejecutar: python 1_crear_bd.py
"""
import sqlite3
import os

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "epp_registros.db")

def crear_base_datos():
    """Crea la base de datos y las tablas necesarias"""
    
    print("="*80)
    print("🗄️  CREANDO BASE DE DATOS EPP")
    print("="*80)
    
    # Conectar a la BD (la crea si no existe)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"\n📍 Ubicación: {DB_PATH}\n")
    
    # TABLA PRINCIPAL: registros
    print("📋 Creando tabla 'registros'...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_hora TEXT NOT NULL,
            frame_number INTEGER,
            
            -- Conteo de detecciones
            total_personas INTEGER DEFAULT 0,
            total_cascos INTEGER DEFAULT 0,
            total_chalecos INTEGER DEFAULT 0,
            total_gafas INTEGER DEFAULT 0,
            
            -- Cumplimiento (calculado y guardado)
            cumplimiento_general REAL DEFAULT 0.0,
            cumplimiento_casco REAL DEFAULT 0.0,
            cumplimiento_chaleco REAL DEFAULT 0.0,
            cumplimiento_gafas REAL DEFAULT 0.0,
            
            -- Distribución personas
            personas_con_casco INTEGER DEFAULT 0,
            personas_sin_casco INTEGER DEFAULT 0,
            personas_con_chaleco INTEGER DEFAULT 0,
            personas_sin_chaleco INTEGER DEFAULT 0,
            personas_con_gafas INTEGER DEFAULT 0,
            personas_sin_gafas INTEGER DEFAULT 0,
            
            -- Incumplimientos
            incumplimientos_totales INTEGER DEFAULT 0,
            
            -- Ruta de la imagen guardada
            ruta_imagen TEXT,
            
            -- Timestamp de creación
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✅ Tabla 'registros' creada")
    
    # TABLA SECUNDARIA: detecciones_persona (detalle por persona)
    print("📋 Creando tabla 'detecciones_persona'...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detecciones_persona (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registro_id INTEGER NOT NULL,
            numero_persona INTEGER NOT NULL,
            tiene_casco INTEGER DEFAULT 0,
            tiene_chaleco INTEGER DEFAULT 0,
            tiene_gafas INTEGER DEFAULT 0,
            cumplimiento_persona REAL DEFAULT 0.0,
            FOREIGN KEY (registro_id) REFERENCES registros(id) ON DELETE CASCADE
        )
    """)
    print("   ✅ Tabla 'detecciones_persona' creada")
    
    # Crear índices para búsquedas rápidas
    print("🔍 Creando índices...")
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_fecha 
        ON registros(fecha_hora)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_registro 
        ON detecciones_persona(registro_id)
    """)
    print("   ✅ Índices creados")
    
    # Guardar cambios
    conn.commit()
    conn.close()
    
    print("\n" + "="*80)
    print("✅ BASE DE DATOS CREADA EXITOSAMENTE")
    print("="*80)
    print(f"\n📂 Archivo: {os.path.basename(DB_PATH)}")
    print(f"📍 Ruta completa: {DB_PATH}")
    print(f"📊 Tablas creadas:")
    print(f"   - registros (datos principales cada 15 seg)")
    print(f"   - detecciones_persona (detalle por persona)")
    print("\n✅ Lista para usar!\n")


if __name__ == "__main__":
    crear_base_datos()
