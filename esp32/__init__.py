"""
Módulo ESP32 - Sistema de Alertas LED en Tiempo Real
=====================================================

Este módulo maneja la comunicación con el ESP32 para mostrar
alertas visuales mediante LEDs según las detecciones en vivo.

Componentes:
- esp32_config.py: Configuración (IP, lógica de colores)
- esp32_client.py: Cliente HTTP para enviar comandos
- esp32_worker.py: Worker independiente con cola
- arduino/led_server.ino: Código para ESP32

Para desactivar: Comentar líneas en main.py o cambiar USAR_ESP32 = False
"""

__version__ = "1.0.0"
__author__ = "Sistema EPP"
