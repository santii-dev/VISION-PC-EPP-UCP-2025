


# 1. Import the InferencePipeline library
from inference import InferencePipeline
import cv2
import onnxruntime as ort
import requests
import json
import copy
import numpy as np
from datetime import datetime
import threading
from queue import Queue
import time

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# URL de tu backend para enviar los datos procesados
BACKEND_URL = "http://localhost:8000/api/registros"  # Endpoint del backend

# ⚙️ CONFIGURACIÓN DE FRECUENCIA
# Si la cámara va a ~15 FPS real, entonces:
# 5 segundos = 75 frames, 8 segundos = 120 frames
PROCESAR_CADA_N_FRAMES = 75  # Procesar cada 5 segundos aprox (ajustado para cámara ~15 FPS)
MOSTRAR_JSON_COMPLETO = False  # Cambiar a True si quieres ver el JSON completo en consola

# Variables internas
frame_counter = 0
ultimo_timestamp = None
cola_backend = Queue(maxsize=30)  # Máximo 30 peticiones en cola

def worker_backend():
    """
    Worker que corre en segundo plano enviando datos al backend.
    Esto evita que el video se bloquee esperando respuesta del backend.
    """
    print("🔧 Worker backend iniciado y esperando datos...")
    from queue import Empty
    
    while True:
        try:
            output_crudo = cola_backend.get(timeout=3)  # Espera 3 segundos por nueva tarea
            
            tamano_cola = cola_backend.qsize()
            print(f"\n📦 [COLA: {tamano_cola}] Enviando datos al backend...")
            
            # Enviar al backend
            inicio = time.time()
            response = requests.post(BACKEND_URL, json=output_crudo, timeout=10)
            tiempo_respuesta = time.time() - inicio
            
            if response.status_code == 200:
                resultado = response.json()
                print(f"✅ Guardado en BD - ID: {resultado.get('registro_id', 'N/A')} ({tiempo_respuesta:.2f}s)")
            else:
                print(f"⚠️ Backend error {response.status_code}: {response.text[:100]}")
            
            cola_backend.task_done()
        
        except Empty:
            # Cola vacía (normal) - no hacer nada, seguir esperando
            pass
                
        except requests.exceptions.ConnectionError as e:
            print(f"\n❌ Backend NO responde en {BACKEND_URL}")
            print(f"   💡 Ejecuta: python backend/start_backend.py")
            time.sleep(5)
        except requests.exceptions.Timeout:
            print(f"⏱️ Backend tardó más de 10 segundos (timeout)")
        except Exception as e:
            print(f"⚠️ Error en worker: {e}")
            import traceback
            traceback.print_exc()

# Iniciar worker en thread separado
thread_worker = threading.Thread(target=worker_backend, daemon=True)
thread_worker.start()
print("="*80)
print("🚀 SISTEMA DE CAPTURA EPP INICIADO")
print("="*80)
print("🔧 Worker de backend activo en segundo plano")
print(f"📡 Enviando a: {BACKEND_URL}")
print(f"⏱️ Frecuencia: cada {PROCESAR_CADA_N_FRAMES} frames (~5 segundos)")
print(f"💡 Si tarda más/menos, ajusta PROCESAR_CADA_N_FRAMES en línea 26")
print("="*80 + "\n")

def convertir_a_serializable(obj):
    """Convierte objetos de Roboflow (incluyendo numpy arrays) a formato JSON serializable"""
    # Manejar arrays de NumPy
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convertir numpy array a lista de Python
    
    # Manejar datetime
    elif isinstance(obj, datetime):
        return obj.isoformat()
    
    # Manejar objetos con atributos
    elif hasattr(obj, '__dict__'):
        return {k: convertir_a_serializable(v) for k, v in obj.__dict__.items()}
    
    # Manejar diccionarios
    elif isinstance(obj, dict):
        return {k: convertir_a_serializable(v) for k, v in obj.items()}
    
    # Manejar listas
    elif isinstance(obj, list):
        return [convertir_a_serializable(item) for item in obj]
    
    # Manejar tuplas
    elif isinstance(obj, tuple):
        return [convertir_a_serializable(item) for item in obj]
    
    # Tipos básicos (int, float, str, bool, None)
    else:
        return obj

def my_sink(result, video_frame):
    global frame_counter, ultimo_timestamp
    
    # Siempre mostrar la imagen con mejor calidad
    if result.get("output_image"):
        img = result["output_image"].numpy_image
        
        # Configurar la ventana para que sea redimensionable y mantenga la calidad
        cv2.namedWindow("Workflow Image", cv2.WINDOW_NORMAL)
        
        # Mostrar la imagen original (sin escalar, para mantener calidad)
        cv2.imshow("Workflow Image", img)
        cv2.waitKey(1)
    
    # Solo procesar cada N frames para no bloquear el video
    frame_counter += 1
    if frame_counter % PROCESAR_CADA_N_FRAMES != 0:
        return  # Saltar este frame
    
    # Calcular tiempo real transcurrido
    ahora = time.time()
    if ultimo_timestamp:
        tiempo_real = ahora - ultimo_timestamp
        fps_real = PROCESAR_CADA_N_FRAMES / tiempo_real
    else:
        tiempo_real = 0
        fps_real = 0
    ultimo_timestamp = ahora
    
    # ===== CAPTURAR OUTPUT CRUDO Y CONVERTIR A SERIALIZABLE =====
    output_crudo = convertir_a_serializable(result)
    
    # ===== MOSTRAR EN CONSOLA SIN ARRAYS GRANDES (SIMPLIFICADO) =====
    print("\n" + "="*80)
    if tiempo_real > 0:
        print(f"📦 Frame #{frame_counter} - Detecciones (cada {tiempo_real:.1f}s | FPS real: {fps_real:.1f}):")
    else:
        print(f"📦 Frame #{frame_counter} - Detecciones:")
    print("="*80)
    
    # Mostrar solo las detecciones, no todo el JSON
    if "model_1" in output_crudo:
        predictions = output_crudo["model_1"]
        if "data" in predictions and "class_name" in predictions["data"]:
            clases = predictions["data"]["class_name"]
            confidences = predictions.get("confidence", [])
            
            print(f"🎯 Detectado: {len(clases)} objeto(s)")
            for i, (clase, conf) in enumerate(zip(clases, confidences)):
                print(f"  {i+1}. {clase} - Confianza: {conf:.2%}")
        else:
            print("⚪ Sin detecciones en este frame")
    
    # OPCIONAL: Mostrar JSON completo (solo para debugging)
    if MOSTRAR_JSON_COMPLETO:
        output_para_log = copy.deepcopy(output_crudo)
        if "output_image" in output_para_log and isinstance(output_para_log["output_image"], dict):
            if "_base64_image" in output_para_log["output_image"]:
                output_para_log["output_image"]["_base64_image"] = "[BASE64_REMOVIDO]"
            if "_numpy_image" in output_para_log["output_image"]:
                try:
                    shape_info = np.array(output_para_log["output_image"]["_numpy_image"]).shape
                    output_para_log["output_image"]["_numpy_image"] = f"[NUMPY_ARRAY_REMOVIDO - Shape: {shape_info}]"
                except:
                    output_para_log["output_image"]["_numpy_image"] = "[NUMPY_ARRAY_REMOVIDO]"
        print("\n📄 JSON Completo:")
        print(json.dumps(output_para_log, indent=2, ensure_ascii=False)[:2000])  # Primeros 2000 caracteres
    
    print("="*80 + "\n")
    
    # ===== AGREGAR A COLA DE BACKEND (NO BLOQUEANTE) =====
    try:
        cola_backend.put_nowait(output_crudo)
        tamano = cola_backend.qsize()
        print(f"📤 [COLA: {tamano}] Datos agregados → esperando envío al backend")
    except:
        print(f"⚠️ Cola llena ({cola_backend.maxsize} items), saltando envío (backend muy lento)")
        # Si la cola está llena, simplemente no agregamos y continuamos


# 2. Initialize a pipeline object
pipeline = InferencePipeline.init_with_workflow(
    api_key="cQNHowIMmynwup9oMg8a",
    workspace_name="epp-taba",
    workflow_id="epp-produccion",
    video_reference="rtsp://CAMARAEPP:123camara@192.168.1.33/stream1",  # stream1 = campo visual más estrecho
    max_fps=30,
    on_prediction=my_sink
)

# Verificamos proveedores directamente desde la instalación activa de ONNX Runtime
print("✅ Available providers (global):", ort.get_available_providers())

# 3. Start the pipeline and wait for it to finish
pipeline.start()
pipeline.join()