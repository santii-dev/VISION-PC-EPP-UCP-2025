"""
Worker ESP32 - Procesamiento en Segundo Plano
==============================================

Este worker corre en un thread separado y:
1. Recibe detecciones desde la cola
2. Calcula el color según la lógica configurada
3. Envía el color al ESP32

NO bloquea el video ni el sistema principal.
"""

import threading
from queue import Queue, Empty
import time
import os
import sys

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from esp32.esp32_config import (
    USAR_ESP32,
    MAX_COLA_ESP32,
    PROCESAR_CADA_N_FRAMES_ESP32,
    calcular_color_led,
    DEBUG_ESP32
)
from esp32.esp32_client import enviar_color_a_esp32


# ============================================================================
# VARIABLES GLOBALES
# ============================================================================

# Cola para comunicación thread-safe
cola_esp32 = Queue(maxsize=MAX_COLA_ESP32)

# Contador de frames (para procesar cada N frames)
contador_frames_esp32 = 0

# Thread del worker
thread_esp32 = None

# Flag para detener el worker
_detener_worker = False


# ============================================================================
# WORKER (corre en segundo plano)
# ============================================================================

def _worker_esp32():
    """
    Worker que procesa la cola de detecciones y envía colores al ESP32.
    Corre en un thread separado, NO bloquea el video.
    """
    
    print("🔧 [ESP32] Worker iniciado y esperando detecciones...")
    
    ultimo_color = None  # Para evitar enviar el mismo color repetidamente
    
    while not _detener_worker:
        try:
            # Esperar detecciones de la cola (timeout 0.5 segundos)
            detecciones = cola_esp32.get(timeout=0.5)
            
            # 🚀 OPTIMIZACIÓN: Vaciar mensajes viejos de la cola (usar solo el más reciente)
            while not cola_esp32.empty():
                try:
                    detecciones = cola_esp32.get_nowait()  # Tomar el más reciente
                except Empty:
                    break
            
            # Calcular color según lógica configurada
            color = calcular_color_led(detecciones)
            
            # Enviar siempre (cada registro, no solo al cambiar color)
            if DEBUG_ESP32:
                num_personas = sum(1 for d in detecciones if d.lower() == "person")
                tamano_cola = cola_esp32.qsize()
                print(f"\n🚦 [ESP32] Personas: {num_personas} → Color: {color.upper()} [Cola: {tamano_cola}]")
            
            # Enviar al ESP32
            enviar_color_a_esp32(color)
            ultimo_color = color
            
            # Marcar tarea completada
            cola_esp32.task_done()
        
        except Empty:
            # Cola vacía (normal), seguir esperando
            continue
        
        except Exception as e:
            if DEBUG_ESP32:
                print(f"⚠️ [ESP32] Error en worker: {e}")
            time.sleep(1)
    
    print("🔧 [ESP32] Worker detenido.")


# ============================================================================
# FUNCIONES PÚBLICAS
# ============================================================================

def iniciar_worker_esp32():
    """
    Inicia el worker ESP32 en un thread separado.
    Llamar UNA SOLA VEZ al inicio del programa.
    
    Retorna:
        bool: True si se inició correctamente, False si está desactivado
    """
    
    global thread_esp32, _detener_worker
    
    # Verificar si el módulo está activado
    if not USAR_ESP32:
        print("⚪ [ESP32] Módulo desactivado (USAR_ESP32 = False)")
        return False
    
    # Verificar que no esté ya corriendo
    if thread_esp32 is not None and thread_esp32.is_alive():
        print("⚠️ [ESP32] Worker ya está corriendo")
        return True
    
    # Crear e iniciar thread
    _detener_worker = False
    thread_esp32 = threading.Thread(target=_worker_esp32, daemon=True)
    thread_esp32.start()
    
    print("="*80)
    print("🚦 SISTEMA ESP32 ACTIVADO")
    print("="*80)
    print(f"🔧 Worker ESP32 activo en segundo plano")
    print(f"📡 Enviando a ESP32 cada {PROCESAR_CADA_N_FRAMES_ESP32} frames")
    print(f"📊 Tamaño máximo de cola: {MAX_COLA_ESP32}")
    print("="*80 + "\n")
    
    return True


def agregar_detecciones_esp32(detecciones):
    """
    Agrega detecciones a la cola del ESP32.
    Llamar desde my_sink() en main.py.
    
    Parámetros:
        detecciones (list): Lista de clases detectadas
                           Ejemplo: ["Person", "Person", "Hardhat"]
    
    Retorna:
        bool: True si se agregó a la cola, False si no
    
    Ejemplo de uso:
        >>> agregar_detecciones_esp32(["Person", "Person", "Hardhat"])
        True
    """
    
    global contador_frames_esp32
    
    # Verificar si el módulo está activado
    if not USAR_ESP32:
        return False
    
    # Procesar solo cada N frames (no saturar ESP32)
    contador_frames_esp32 += 1
    if contador_frames_esp32 % PROCESAR_CADA_N_FRAMES_ESP32 != 0:
        return False
    
    # Intentar agregar a la cola (no bloqueante)
    try:
        cola_esp32.put_nowait(detecciones)
        return True
    
    except:
        # Cola llena, ignorar (ESP32 muy lento o caído)
        if DEBUG_ESP32:
            print(f"⚠️ [ESP32] Cola llena ({MAX_COLA_ESP32}), frame ignorado")
        return False


def detener_worker_esp32():
    """
    Detiene el worker ESP32.
    Útil para limpiar recursos al cerrar el programa.
    """
    
    global _detener_worker
    
    if thread_esp32 is not None and thread_esp32.is_alive():
        _detener_worker = True
        thread_esp32.join(timeout=2)
        print("🔧 [ESP32] Worker detenido correctamente")


def obtener_estado_esp32():
    """
    Obtiene el estado actual del sistema ESP32.
    
    Retorna:
        dict: Información del estado
    """
    
    return {
        "activado": USAR_ESP32,
        "worker_corriendo": thread_esp32 is not None and thread_esp32.is_alive(),
        "tamano_cola": cola_esp32.qsize(),
        "frames_procesados": contador_frames_esp32,
        "max_cola": MAX_COLA_ESP32
    }


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # Prueba básica del worker
    print("Iniciando prueba del worker ESP32...")
    
    # Iniciar worker
    if iniciar_worker_esp32():
        
        # Simular detecciones
        print("\n📤 Enviando detecciones de prueba...")
        
        # Caso 1: Sin personas (rojo)
        print("Caso 1: Sin personas")
        agregar_detecciones_esp32([])
        time.sleep(1)
        
        # Caso 2: 1 persona (naranja)
        print("Caso 2: 1 persona")
        agregar_detecciones_esp32(["Person"])
        time.sleep(1)
        
        # Caso 3: 3+ personas (verde)
        print("Caso 3: 3+ personas")
        agregar_detecciones_esp32(["Person", "Person", "Person", "Hardhat"])
        time.sleep(1)
        
        print("\n✅ Prueba completada")
        print(f"Estado: {obtener_estado_esp32()}")
        
        # Detener worker
        detener_worker_esp32()
    else:
        print("❌ No se pudo iniciar el worker")
