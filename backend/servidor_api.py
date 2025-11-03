"""
Servidor FastAPI para recibir y procesar detecciones EPP
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import Dict
from datetime import datetime
import sys
import os
import subprocess
import psutil

# Agregar rutas al path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from backend.BD.operaciones_bd import (
    insertar_registro_completo,
    obtener_todos_registros,
    obtener_registro_con_detalle,
    obtener_estadisticas_generales,
    eliminar_registro,
    eliminar_todos_registros
)
from backend.cumplimiento import calcular_cumplimiento
from backend.image_utils import extraer_imagen_del_output

# Crear aplicación FastAPI
app = FastAPI(
    title="API EPP",
    description="Sistema de monitoreo de EPP",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def inicio():
    """Endpoint de prueba"""
    return {
        "mensaje": "API EPP funcionando",
        "status": "OK",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/registros")
async def recibir_deteccion(data: Dict):
    """
    Recibe detección de Roboflow, calcula cumplimiento,
    guarda imagen y almacena en BD
    """
    try:
        print("\n" + "="*80)
        print("📥 NUEVO REGISTRO RECIBIDO")
        print("="*80)
        
        # 1. Extraer metadata
        video_metadata = data.get("output_image", {}).get("_video_metadata", {})
        fecha_hora = video_metadata.get("frame_timestamp", datetime.now().isoformat())
        frame_number = video_metadata.get("frame_number", 0)
        
        print(f"⏰ Fecha: {fecha_hora}")
        print(f"🎬 Frame: {frame_number}")
        
        # 2. Guardar imagen
        print("\n📸 Guardando imagen...")
        ruta_imagen = extraer_imagen_del_output(data)
        if ruta_imagen:
            print(f"   ✅ Guardada: {ruta_imagen}")
        else:
            print("   ⚠️ No se pudo guardar")
            ruta_imagen = ""
        
        # 3. Calcular cumplimiento
        print("\n📊 Calculando cumplimiento...")
        metricas = calcular_cumplimiento(data)
        
        print(f"   👥 Personas: {metricas['total_personas']}")
        print(f"   🪖 Cascos: {metricas['total_cascos']}")
        print(f"   🦺 Chalecos: {metricas['total_chalecos']}")
        print(f"   🥽 Gafas: {metricas['total_gafas']}")
        print(f"\n   📈 Cumplimiento General: {metricas['cumplimiento_general']}%")
        print(f"      - Casco: {metricas['cumplimiento_casco']}%")
        print(f"      - Chaleco: {metricas['cumplimiento_chaleco']}%")
        print(f"      - Gafas: {metricas['cumplimiento_gafas']}%")
        print(f"   ❌ Incumplimientos: {metricas['incumplimientos_totales']}")
        
        # 4. Preparar datos para BD
        datos_bd = {
            "fecha_hora": fecha_hora,
            "frame_number": frame_number,
            "total_personas": metricas["total_personas"],
            "total_cascos": metricas["total_cascos"],
            "total_chalecos": metricas["total_chalecos"],
            "total_gafas": metricas["total_gafas"],
            "cumplimiento_general": metricas["cumplimiento_general"],
            "cumplimiento_casco": metricas["cumplimiento_casco"],
            "cumplimiento_chaleco": metricas["cumplimiento_chaleco"],
            "cumplimiento_gafas": metricas["cumplimiento_gafas"],
            "personas_con_casco": metricas["personas_con_casco"],
            "personas_sin_casco": metricas["personas_sin_casco"],
            "personas_con_chaleco": metricas["personas_con_chaleco"],
            "personas_sin_chaleco": metricas["personas_sin_chaleco"],
            "personas_con_gafas": metricas["personas_con_gafas"],
            "personas_sin_gafas": metricas["personas_sin_gafas"],
            "incumplimientos_totales": metricas["incumplimientos_totales"],
            "ruta_imagen": ruta_imagen,
            "detecciones_persona": metricas["detecciones_persona"]
        }
        
        # 5. Guardar en BD
        print("\n💾 Guardando en base de datos...")
        registro_id = insertar_registro_completo(datos_bd)
        
        print(f"   ✅ Registro ID {registro_id} guardado")
        print("="*80 + "\n")
        
        # 6. Retornar respuesta
        return JSONResponse(content={
            "status": "success",
            "registro_id": registro_id,
            "mensaje": "Registro procesado correctamente",
            "metricas": metricas
        })
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/registros")
async def listar_registros(limite: int = 100):
    """Obtiene lista de registros"""
    try:
        registros = obtener_todos_registros(limite)
        
        # Mapear fecha_hora a timestamp para el frontend
        for registro in registros:
            if 'fecha_hora' in registro:
                registro['timestamp'] = registro['fecha_hora']
            if 'cumplimiento_casco' in registro:
                registro['cumplimiento_cascos'] = registro['cumplimiento_casco']
            if 'cumplimiento_chaleco' in registro:
                registro['cumplimiento_chalecos'] = registro['cumplimiento_chaleco']
            if 'cumplimiento_gafas' in registro:
                registro['cumplimiento_gafas'] = registro['cumplimiento_gafas']
        
        return JSONResponse(
            content={
                "status": "success",
                "total": len(registros),
                "registros": registros
            },
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/registros/{registro_id}")
async def obtener_registro_detalle(registro_id: int):
    """Obtiene un registro con detalle por persona"""
    try:
        data = obtener_registro_con_detalle(registro_id)
        if not data:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        # Separar detecciones del registro principal
        detecciones_persona = data.pop('detecciones_persona', [])
        
        # Mapear fecha_hora a timestamp en el registro
        if 'fecha_hora' in data:
            data['timestamp'] = data['fecha_hora']
        if 'cumplimiento_casco' in data:
            data['cumplimiento_cascos'] = data['cumplimiento_casco']
        if 'cumplimiento_chaleco' in data:
            data['cumplimiento_chalecos'] = data['cumplimiento_chaleco']
        if 'cumplimiento_gafas' in data:
            data['cumplimiento_gafas'] = data['cumplimiento_gafas']
        
        return JSONResponse(content={
            "status": "success",
            "registro": data,
            "detecciones": detecciones_persona
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/estadisticas")
async def estadisticas():
    """Obtiene estadísticas generales"""
    try:
        stats = obtener_estadisticas_generales()
        return JSONResponse(content={
            "status": "success",
            "estadisticas": stats
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/registros/{registro_id}")
async def eliminar_registro_endpoint(registro_id: int):
    """Elimina un registro específico y su imagen"""
    try:
        # Primero obtener la ruta de la imagen antes de eliminar
        registro = obtener_registro_con_detalle(registro_id)
        
        if registro and registro.get('ruta_imagen'):
            # Eliminar la imagen si existe
            ruta_imagen = os.path.join(BASE_DIR, registro['ruta_imagen'])
            if os.path.exists(ruta_imagen):
                try:
                    os.remove(ruta_imagen)
                    print(f"✓ Imagen eliminada: {ruta_imagen}")
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar imagen: {e}")
        
        # Eliminar el registro de la BD
        resultado = eliminar_registro(registro_id)
        
        if resultado:
            return JSONResponse(content={
                "status": "success",
                "mensaje": f"Registro #{registro_id} eliminado correctamente"
            })
        else:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error eliminando registro: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/registros")
async def eliminar_todos_registros_endpoint():
    """Elimina todos los registros y sus imágenes"""
    try:
        # Obtener todos los registros para eliminar sus imágenes
        registros = obtener_todos_registros(10000)  # Obtener todos
        
        # Eliminar todas las imágenes
        for registro in registros:
            if registro.get('ruta_imagen'):
                ruta_imagen = os.path.join(BASE_DIR, registro['ruta_imagen'])
                if os.path.exists(ruta_imagen):
                    try:
                        os.remove(ruta_imagen)
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar {ruta_imagen}: {e}")
        
        # Eliminar todos los registros de la BD
        cantidad = eliminar_todos_registros()
        
        print(f"✓ Eliminados {cantidad} registros y sus imágenes")
        
        return JSONResponse(content={
            "status": "success",
            "mensaje": f"Se eliminaron {cantidad} registros correctamente"
        })
    except Exception as e:
        print(f"Error eliminando todos los registros: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/registros/{filename}")
async def obtener_imagen(filename: str):
    """Sirve las imágenes de los registros"""
    try:
        ruta_imagen = os.path.join(BASE_DIR, "registros", filename)
        
        if not os.path.exists(ruta_imagen):
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        
        return FileResponse(
            ruta_imagen,
            media_type="image/jpeg",
            headers={"Cache-Control": "public, max-age=3600"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Variable global para almacenar el proceso de la cámara
camera_process = None


@app.post("/api/camera/start")
async def iniciar_camara():
    """Inicia el proceso de captura de cámara (main.py)"""
    global camera_process
    
    try:
        # Verificar si ya está corriendo
        if camera_process and camera_process.poll() is None:
            return JSONResponse(content={
                "status": "already_running",
                "mensaje": "La cámara ya está activa",
                "pid": camera_process.pid
            })
        
        # 🚦 ENVIAR SEÑAL VERDE AL ESP32 (sistema activándose)
        try:
            import requests
            requests.post(
                "http://192.168.1.34:80/led",
                json={"color": "verde"},
                timeout=1
            )
            print("✅ ESP32: Sistema activado → VERDE")
        except:
            print("⚠️ ESP32: No se pudo enviar señal de activación")
        
        # Iniciar main.py
        main_path = os.path.join(BASE_DIR, "main.py")
        camera_process = subprocess.Popen(
            [sys.executable, main_path],
            cwd=BASE_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        return JSONResponse(content={
            "status": "success",
            "mensaje": "Cámara iniciada correctamente",
            "pid": camera_process.pid
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar cámara: {str(e)}")


@app.post("/api/camera/stop")
async def detener_camara():
    """Detiene el proceso de captura de cámara"""
    global camera_process
    
    try:
        if not camera_process or camera_process.poll() is not None:
            return JSONResponse(content={
                "status": "not_running",
                "mensaje": "La cámara no está activa"
            })
        
        # Intentar detener el proceso de forma ordenada
        try:
            parent = psutil.Process(camera_process.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            parent.terminate()
            
            # Esperar un poco para que termine
            parent.wait(timeout=5)
        except psutil.NoSuchProcess:
            pass
        except psutil.TimeoutExpired:
            # Si no termina, forzar
            parent.kill()
        
        camera_process = None
        
        # 🚦 APAGAR LED DEL ESP32 (sistema desactivado)
        try:
            import requests
            requests.post(
                "http://192.168.1.34:80/led",
                json={"color": "apagado"},
                timeout=1
            )
            print("✅ ESP32: Sistema desactivado → LED APAGADO")
        except:
            print("⚠️ ESP32: No se pudo enviar señal de desactivación")
        
        return JSONResponse(content={
            "status": "success",
            "mensaje": "Cámara detenida correctamente"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al detener cámara: {str(e)}")


@app.get("/api/camera/status")
async def estado_camara():
    """Verifica el estado de la cámara"""
    global camera_process
    
    try:
        if camera_process and camera_process.poll() is None:
            return JSONResponse(content={
                "status": "running",
                "mensaje": "Cámara activa",
                "pid": camera_process.pid
            })
        else:
            return JSONResponse(content={
                "status": "stopped",
                "mensaje": "Cámara inactiva"
            })
    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "mensaje": str(e)
        })


if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor API EPP...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
