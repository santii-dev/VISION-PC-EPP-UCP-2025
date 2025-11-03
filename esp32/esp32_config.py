"""
Configuración del Sistema ESP32
================================

Aquí se configura TODO lo relacionado con el ESP32:
- IP y puerto
- Lógica de colores según detecciones
- Timeouts y reintentos
- Activación/desactivación del módulo
"""

# ============================================================================
# CONFIGURACIÓN GENERAL
# ============================================================================

# 🔌 Activar/Desactivar el módulo ESP32 (cambiar a False para desactivar)
USAR_ESP32 = True

# 🌐 IP del ESP32 en tu red local (CAMBIAR según tu ESP32)
ESP32_IP = "192.168.1.34"  # ⚠️ IMPORTANTE: Configurar la IP correcta

# 🔌 Puerto HTTP del ESP32 (normalmente 80)
ESP32_PORT = 80

# 🔗 URL completa del ESP32
ESP32_URL = f"http://{ESP32_IP}:{ESP32_PORT}/led"

# ⏱️ Timeout para peticiones HTTP (segundos)
HTTP_TIMEOUT = 2.0  # 2 segundos (más generoso, no hay prisa)

# 🔄 Procesar cada N frames recibidos en la cola (1 = procesar todos)
# Como ahora solo recibimos 1 detección cada 5 segundos, procesamos TODOS
PROCESAR_CADA_N_FRAMES_ESP32 = 1

# 📊 Tamaño máximo de la cola (pequeña porque ya llega cada 5 seg)
MAX_COLA_ESP32 = 5


# ============================================================================
# LÓGICA DE COLORES
# ============================================================================

def calcular_color_led(detecciones):
    """
    Calcula qué color debe mostrar el LED según las detecciones.
    
    Parámetros:
        detecciones (list): Lista de clases detectadas 
                           (ej: ["person", "hardhat", "safety vest"])
    
    Retorna:
        str: "morado", "rojo" o "naranja"
    
    LÓGICA SIMPLIFICADA:
        - 🟣 MORADO: No detecta nada (área vacía - silencio)
        - 🔴 ROJO: Personas SIN ningún EPP (ALARMA CONTINUA)
        - 🟠 NARANJA: Personas CON EPP parcial
        - 🟢 VERDE: EPP COMPLETO (1 persona = 1 casco + 1 chaleco + 1 gafas)
    """
    
    # Convertir a minúsculas para búsqueda case-insensitive
    detecciones_lower = [d.lower() for d in detecciones]
    
    # Contar personas
    num_personas = detecciones_lower.count("person")
    
    # Contar cada tipo de EPP por separado
    num_cascos = sum(1 for d in detecciones_lower if any(x in d for x in ["hardhat", "helmet", "casco"]))
    num_chalecos = sum(1 for d in detecciones_lower if any(x in d for x in ["vest", "jacket", "chaleco"]))
    num_gafas = sum(1 for d in detecciones_lower if any(x in d for x in ["goggles", "gafas", "glasses"]))
    
    total_epp = num_cascos + num_chalecos + num_gafas
    
    # ========================================================================
    # CASO 1: NO DETECTA NADA → MORADO
    # ========================================================================
    if num_personas == 0 and total_epp == 0:
        return "morado"
    
    # ========================================================================
    # CASO 2: PERSONAS SIN NINGÚN EPP → ROJO (ALARMA)
    # ========================================================================
    if num_personas > 0 and total_epp == 0:
        return "rojo"
    
    # ========================================================================
    # CASO 3: EPP COMPLETO → VERDE
    # ========================================================================
    # Cada persona debe tener casco + chaleco + gafas
    if num_personas > 0:
        tiene_todo = (num_cascos >= num_personas and 
                     num_chalecos >= num_personas and 
                     num_gafas >= num_personas)
        if tiene_todo:
            return "verde"
    
    # ========================================================================
    # CASO 4: EPP PARCIAL → NARANJA
    # ========================================================================
    if num_personas > 0 and total_epp > 0:
        return "naranja"
    
    # ========================================================================
    # CASO 5: Solo EPP sin personas → MORADO
    # ========================================================================
    return "morado"
    
    # ========================================================================
    # EJEMPLOS DE OTRAS LÓGICAS (descomenta para usar):
    # ========================================================================
    
    # # Ejemplo 1: Basado en EPP (cascos)
    # num_personas = detecciones.count("Person")
    # num_cascos = detecciones.count("Hardhat")
    # 
    # if num_personas == 0:
    #     return "rojo"  # Sin personas
    # elif num_cascos >= num_personas:
    #     return "verde"  # Todos con casco
    # elif num_cascos > 0:
    #     return "naranja"  # Algunos sin casco
    # else:
    #     return "rojo"  # Nadie con casco
    
    # # Ejemplo 2: Horario (turno nocturno)
    # from datetime import datetime
    # hora = datetime.now().hour
    # 
    # if hora >= 22 or hora <= 6:  # Turno nocturno
    #     if num_personas > 0:
    #         return "verde"  # OK si hay personal
    #     else:
    #         return "naranja"  # Normal, área cerrada
    # else:  # Turno diurno
    #     if num_personas >= 3:
    #         return "verde"
    #     else:
    #         return "rojo"  # Problema, debería haber gente


# ============================================================================
# CONFIGURACIÓN AVANZADA (normalmente no necesitas cambiar esto)
# ============================================================================

# 🔁 Reintentar si falla el envío
REINTENTAR_SI_FALLA = False  # No recomendado, puede causar delay

# 📝 Mostrar logs detallados
DEBUG_ESP32 = True  # Cambiar a False para menos mensajes en consola

# 🎨 Mapeo de colores (por si usas nombres diferentes en ESP32)
COLOR_MAPPING = {
    "morado": "purple",
    "rojo": "red",
    "verde": "green",
    "naranja": "orange"
}

# ⚙️ Estado por defecto si no hay detecciones
COLOR_POR_DEFECTO = "morado"
