"""
Cliente HTTP para comunicación con ESP32
=========================================

Maneja el envío de comandos al ESP32 mediante HTTP POST.
Incluye manejo de errores y timeouts.
"""

import requests
import os
import sys

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from esp32.esp32_config import (
    ESP32_URL, 
    HTTP_TIMEOUT, 
    DEBUG_ESP32,
    REINTENTAR_SI_FALLA
)


def enviar_color_a_esp32(color):
    """
    Envía comando de color al ESP32 mediante HTTP POST.
    
    Parámetros:
        color (str): Color a enviar ("rojo", "naranja", "verde")
    
    Retorna:
        bool: True si se envió correctamente, False si falló
    
    Ejemplo de uso:
        >>> enviar_color_a_esp32("verde")
        True
    """
    
    try:
        # Preparar datos JSON
        payload = {"color": color}
        
        # Enviar POST al ESP32
        response = requests.post(
            ESP32_URL,
            json=payload,
            timeout=HTTP_TIMEOUT
        )
        
        # Verificar respuesta
        if response.status_code == 200:
            if DEBUG_ESP32:
                print(f"    💡 ESP32: LED → {color.upper()}")
            return True
        else:
            if DEBUG_ESP32:
                print(f"    ⚠️ ESP32 respondió con código {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        if DEBUG_ESP32:
            print(f"    ⏱️ ESP32: Timeout ({HTTP_TIMEOUT}s)")
        return False
        
    except requests.exceptions.ConnectionError:
        if DEBUG_ESP32:
            print(f"    ❌ ESP32: No se pudo conectar a {ESP32_URL}")
            print(f"       💡 Verifica que el ESP32 esté encendido y en la red")
        return False
        
    except Exception as e:
        if DEBUG_ESP32:
            print(f"    ⚠️ ESP32: Error inesperado: {e}")
        return False


def probar_conexion_esp32():
    """
    Prueba la conexión con el ESP32.
    Útil para verificar que todo está funcionando.
    
    Retorna:
        bool: True si la conexión funciona, False si no
    """
    
    print("\n" + "="*60)
    print("🔧 PROBANDO CONEXIÓN CON ESP32")
    print("="*60)
    print(f"📡 URL: {ESP32_URL}")
    print(f"⏱️ Timeout: {HTTP_TIMEOUT}s")
    print()
    
    # Probar secuencia de colores
    colores_prueba = ["rojo", "naranja", "verde", "rojo"]
    
    for i, color in enumerate(colores_prueba, 1):
        print(f"Prueba {i}/{len(colores_prueba)}: Enviando '{color}'...", end=" ")
        
        exito = enviar_color_a_esp32(color)
        
        if exito:
            print("✅ OK")
        else:
            print("❌ FALLÓ")
            print("\n⚠️ Verifica:")
            print("   1. ESP32 está encendido")
            print("   2. IP correcta en esp32_config.py")
            print("   3. ESP32 y PC en misma red WiFi")
            print("="*60 + "\n")
            return False
        
        # Pausa entre colores
        import time
        time.sleep(0.5)
    
    print("\n✅ CONEXIÓN CON ESP32: OK")
    print("="*60 + "\n")
    return True


if __name__ == "__main__":
    # Ejecutar prueba si se corre directamente este archivo
    # Uso: python esp32/esp32_client.py
    probar_conexion_esp32()
