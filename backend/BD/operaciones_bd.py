"""
Operaciones de base de datos para registros EPP
Funciones para insertar, consultar y gestionar registros
"""
import sqlite3
import os
from typing import Dict, List, Optional

# Ruta de la BD
DB_PATH = os.path.join(os.path.dirname(__file__), "epp_registros.db")


def insertar_registro_completo(datos: Dict) -> int:
    """
    Inserta un registro completo en la BD.
    
    Args:
        datos: Diccionario con todos los datos del registro
        
    Returns:
        ID del registro insertado
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insertar registro principal
    cursor.execute("""
        INSERT INTO registros (
            fecha_hora, frame_number,
            total_personas, total_cascos, total_chalecos, total_gafas,
            cumplimiento_general, cumplimiento_casco, cumplimiento_chaleco, cumplimiento_gafas,
            personas_con_casco, personas_sin_casco,
            personas_con_chaleco, personas_sin_chaleco,
            personas_con_gafas, personas_sin_gafas,
            incumplimientos_totales, ruta_imagen
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datos["fecha_hora"],
        datos["frame_number"],
        datos["total_personas"],
        datos["total_cascos"],
        datos["total_chalecos"],
        datos["total_gafas"],
        datos["cumplimiento_general"],
        datos["cumplimiento_casco"],
        datos["cumplimiento_chaleco"],
        datos["cumplimiento_gafas"],
        datos["personas_con_casco"],
        datos["personas_sin_casco"],
        datos["personas_con_chaleco"],
        datos["personas_sin_chaleco"],
        datos["personas_con_gafas"],
        datos["personas_sin_gafas"],
        datos["incumplimientos_totales"],
        datos["ruta_imagen"]
    ))
    
    registro_id = cursor.lastrowid
    
    # Insertar detecciones por persona
    if "detecciones_persona" in datos and datos["detecciones_persona"]:
        for persona in datos["detecciones_persona"]:
            cursor.execute("""
                INSERT INTO detecciones_persona (
                    registro_id, numero_persona,
                    tiene_casco, tiene_chaleco, tiene_gafas,
                    cumplimiento_persona
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                registro_id,
                persona["numero_persona"],
                persona["tiene_casco"],
                persona["tiene_chaleco"],
                persona["tiene_gafas"],
                persona["cumplimiento_persona"]
            ))
    
    conn.commit()
    conn.close()
    
    return registro_id


def obtener_todos_registros(limite: int = 100) -> List[Dict]:
    """
    Obtiene los últimos registros de la BD.
    
    Args:
        limite: Número máximo de registros a retornar
        
    Returns:
        Lista de registros como diccionarios
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM registros 
        ORDER BY id DESC 
        LIMIT ?
    """, (limite,))
    
    registros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return registros


def obtener_registro_con_detalle(registro_id: int) -> Optional[Dict]:
    """
    Obtiene un registro específico con sus detecciones por persona.
    
    Args:
        registro_id: ID del registro
        
    Returns:
        Diccionario con el registro y sus detecciones, o None si no existe
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Obtener registro principal
    cursor.execute("SELECT * FROM registros WHERE id = ?", (registro_id,))
    registro = cursor.fetchone()
    
    if not registro:
        conn.close()
        return None
    
    registro_dict = dict(registro)
    
    # Obtener detecciones por persona
    cursor.execute("""
        SELECT * FROM detecciones_persona 
        WHERE registro_id = ?
        ORDER BY numero_persona
    """, (registro_id,))
    
    detecciones = [dict(row) for row in cursor.fetchall()]
    registro_dict["detecciones_persona"] = detecciones
    
    conn.close()
    
    return registro_dict


def obtener_estadisticas_generales() -> Dict:
    """
    Calcula estadísticas generales de todos los registros.
    
    Returns:
        Diccionario con estadísticas
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Contar total de registros
    cursor.execute("SELECT COUNT(*) FROM registros")
    total_registros = cursor.fetchone()[0]
    
    if total_registros == 0:
        conn.close()
        return {
            "total_registros": 0,
            "mensaje": "No hay registros aún"
        }
    
    # Obtener promedios
    cursor.execute("""
        SELECT 
            AVG(cumplimiento_general) as cumpl_gral,
            AVG(cumplimiento_casco) as cumpl_casco,
            AVG(cumplimiento_chaleco) as cumpl_chaleco,
            AVG(cumplimiento_gafas) as cumpl_gafas,
            SUM(total_personas) as total_personas,
            SUM(incumplimientos_totales) as total_incumpl
        FROM registros
    """)
    
    resultado = cursor.fetchone()
    conn.close()
    
    cumpl_gral = resultado[0] or 0
    
    return {
        "total_registros": total_registros,
        "cumplimiento_general_promedio": round(cumpl_gral, 2),
        "cumplimiento_casco_promedio": round(resultado[1] or 0, 2),
        "cumplimiento_chaleco_promedio": round(resultado[2] or 0, 2),
        "cumplimiento_gafas_promedio": round(resultado[3] or 0, 2),
        "total_personas_detectadas": resultado[4] or 0,
        "total_incumplimientos": resultado[5] or 0,
        "calificacion": calificar_cumplimiento(cumpl_gral)
    }


def calificar_cumplimiento(porcentaje: float) -> str:
    """Retorna calificación cualitativa del cumplimiento"""
    if porcentaje >= 90:
        return "Excelente"
    elif porcentaje >= 75:
        return "Bueno"
    elif porcentaje >= 60:
        return "Regular"
    elif porcentaje >= 40:
        return "Malo"
    else:
        return "Muy Malo"


def eliminar_registro(registro_id: int) -> bool:
    """
    Elimina un registro (y sus detecciones por CASCADE).
    
    Args:
        registro_id: ID del registro a eliminar
        
    Returns:
        True si se eliminó, False si no existía
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar primero si existe
    cursor.execute("SELECT id FROM registros WHERE id = ?", (registro_id,))
    existe = cursor.fetchone()
    
    if existe:
        print(f"🗑️  Eliminando registro ID: {registro_id}")
        cursor.execute("DELETE FROM registros WHERE id = ?", (registro_id,))
        cursor.execute("DELETE FROM detecciones_persona WHERE registro_id = ?", (registro_id,))
        conn.commit()
        print(f"✅ Registro {registro_id} eliminado correctamente")
    else:
        print(f"❌ Registro ID {registro_id} NO existe en la BD")
    
    conn.close()
    
    return existe is not None


def eliminar_todos_registros() -> int:
    """
    Elimina todos los registros de la base de datos y reinicia el contador de IDs.
    
    Returns:
        Cantidad de registros eliminados
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Contar registros antes de eliminar
    cursor.execute("SELECT COUNT(*) FROM registros")
    cantidad = cursor.fetchone()[0]
    
    print(f"🗑️  Eliminando {cantidad} registros...")
    
    # Eliminar todos los registros (CASCADE eliminará las detecciones)
    cursor.execute("DELETE FROM registros")
    cursor.execute("DELETE FROM detecciones_persona")
    
    # Reiniciar el contador de AUTOINCREMENT en SQLite
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='registros'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='detecciones_persona'")
    
    # Commit antes de VACUUM (VACUUM no se puede hacer en transacción)
    conn.commit()
    
    # Verificar que se eliminaron
    cursor.execute("SELECT COUNT(*) FROM registros")
    quedan = cursor.fetchone()[0]
    print(f"📊 Registros después de DELETE: {quedan}")
    
    # Verificar sqlite_sequence
    cursor.execute("SELECT * FROM sqlite_sequence WHERE name='registros'")
    seq = cursor.fetchone()
    print(f"📈 sqlite_sequence para 'registros': {seq}")
    
    # Vacuumar para optimizar y limpiar la BD (fuera de transacción)
    try:
        cursor.execute("VACUUM")
    except Exception as e:
        print(f"⚠️ No se pudo ejecutar VACUUM: {e}")
    
    conn.close()
    
    print(f"✅ {cantidad} registros eliminados. IDs reiniciados.")
    
    return cantidad

