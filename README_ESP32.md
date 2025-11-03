# 🚦 Sistema de Alertas LED ESP32 - Guía Completa

Sistema de alertas visuales en tiempo real mediante LEDs controlados por ESP32, integrado al sistema EPP.

---

## 📋 Contenido

1. [Introducción](#introducción)
2. [Requisitos](#requisitos)
3. [Instalación Hardware](#instalación-hardware)
4. [Instalación Software](#instalación-software)
5. [Configuración](#configuración)
6. [Uso](#uso)
7. [Troubleshooting](#troubleshooting)
8. [Desactivar el Sistema](#desactivar-el-sistema)

---

## 🎯 Introducción

Este módulo agrega alertas visuales y sonoras en tiempo real al sistema EPP:

- **🔴 LED ROJO + Beep Largo**: Sin personas/elementos detectados
- **⚪ LED BLANCO + Alerta Triple**: Solo personas, sin EPP (incumplimiento total)
- **🟠 LED NARANJA + Beep Triple**: Personas con algunos EPP (incumplimiento parcial)
- **🟢 LED VERDE + Beep Corto**: Todos con EPP completo (cumplimiento total)

**Características:**

- ⚡ Procesamiento en vivo (cada 1-2 frames)
- 🚀 Ultra rápido (~50-100ms latencia)
- 🔧 No interfiere con el sistema actual
- 🎨 Lógica de colores configurable
- 🔌 Fácil de activar/desactivar

---

## 📦 Requisitos

### Hardware

| Componente        | Cantidad | Notas                                        |
| ----------------- | -------- | -------------------------------------------- |
| **ESP32**         | 1        | Cualquier modelo (DevKit, NodeMCU-32S, etc.) |
| **LED RGB**       | 1        | Cátodo o ánodo común                         |
| **Resistencias**  | 3        | 220Ω - 330Ω (una para cada pin del LED)      |
| **Buzzer SFM-27** | 1        | Buzzer activo 5V                             |
| **Cables Dupont** | ~8       | Para conexiones                              |
| **Protoboard**    | 1        | Opcional (para pruebas)                      |
| **Cable USB**     | 1        | Para programar ESP32                         |

**Costo total estimado:** $8-15 USD

### Software

#### En la PC:

- ✅ Python (ya instalado)
- ✅ Librería `requests` (ya instalada)

#### Para ESP32:

- Arduino IDE 2.x o superior
- Soporte para ESP32 en Arduino
- Librería ArduinoJson

---

## 🔌 Instalación Hardware

### Configuración Actual (LED RGB + Buzzer)

```
ESP32                          Componentes
=====                          ===========

D35 (GPIO 35) ──[330Ω]──→ LED RGB Pin R (Rojo)
                              │
D25 (GPIO 25) ──[330Ω]──→ LED RGB Pin G (Verde)
                              │
D27 (GPIO 27) ──[330Ω]──→ LED RGB Pin B (Azul)
                              │
                         LED RGB Pin común → GND

5V ──────────────────────→ Buzzer SFM-27 (+)

D32 (GPIO 32) ────────────→ Buzzer SFM-27 (–)

GND ──────────────────────→ GND común
```

**Pasos:**

1. Conecta cada pin del LED RGB a través de resistencia a D35(R), D25(G), D27(B)
2. Conecta pin común del LED RGB a GND
3. Conecta Buzzer (+) a 5V
4. Conecta Buzzer (–) a D32
5. Verifica que todos compartan GND común

---

## 💻 Instalación Software

### 1. Instalar Arduino IDE

1. Descargar de: https://www.arduino.cc/en/software
2. Instalar (siguiente → siguiente → instalar)

### 2. Configurar Soporte ESP32

1. Abrir Arduino IDE
2. Ir a: **Archivo → Preferencias**
3. En "Gestor de URLs adicionales de tarjetas", agregar:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Ir a: **Herramientas → Placa → Gestor de tarjetas**
5. Buscar "esp32" e instalar "esp32 by Espressif Systems"

### 3. Instalar Librería ArduinoJson

1. Ir a: **Herramientas → Administrar bibliotecas**
2. Buscar "ArduinoJson"
3. Instalar la versión 6.x (NO la 7.x)

### 4. Programar el ESP32

1. Abrir `esp32/arduino/led_server.ino` en Arduino IDE

2. **CONFIGURAR WIFI** (líneas 45-46):

   ```cpp
   const char* WIFI_SSID = "TU_RED_WIFI";        // ← TU RED
   const char* WIFI_PASSWORD = "TU_CONTRASEÑA";  // ← TU CONTRASEÑA
   ```

3. Conectar ESP32 por USB a la PC

4. Configurar placa:

   - **Herramientas → Placa** → ESP32 Dev Module (o tu modelo)
   - **Herramientas → Puerto** → (Seleccionar el puerto COM del ESP32)

5. Subir el código:

   - Click en el botón **→** (Subir)
   - Esperar "Done uploading"

6. Abrir Monitor Serial:

   - **Herramientas → Monitor Serie**
   - Configurar: **115200 baudios**

7. **ANOTAR LA IP** que muestra (ejemplo: `192.168.1.100`)

---

## ⚙️ Configuración

### 1. Configurar IP del ESP32 en Python

Editar `esp32/esp32_config.py` línea 20:

```python
ESP32_IP = "192.168.1.100"  # ← Poner la IP que anotaste
```

### 2. Personalizar Lógica de Colores (Opcional)

En `esp32/esp32_config.py`, función `calcular_color_led()`:

```python
def calcular_color_led(detecciones):
    num_personas = detecciones.count("Person")

    if num_personas >= 3:
        return "verde"      # ✅ Todo bien
    elif num_personas >= 1:
        return "naranja"    # ⚠️ Alerta
    else:
        return "rojo"       # ❌ Sin personas
```

**Ejemplos de otras lógicas:**

#### Basado en EPP (Cascos):

```python
def calcular_color_led(detecciones):
    num_personas = detecciones.count("Person")
    num_cascos = detecciones.count("Hardhat")

    if num_personas == 0:
        return "rojo"
    elif num_cascos >= num_personas:
        return "verde"  # Todos con casco
    else:
        return "naranja"  # Algunos sin casco
```

#### Por horario:

```python
def calcular_color_led(detecciones):
    from datetime import datetime
    hora = datetime.now().hour
    num_personas = detecciones.count("Person")

    if hora >= 22 or hora <= 6:  # Noche
        return "naranja" if num_personas == 0 else "verde"
    else:  # Día
        return "verde" if num_personas >= 3 else "rojo"
```

### 3. Ajustar Frecuencia (Opcional)

En `esp32/esp32_config.py` línea 32:

```python
PROCESAR_CADA_N_FRAMES_ESP32 = 2  # Cada 2 frames (muy rápido)
```

- `1` = Cada frame (ultra rápido, puede saturar)
- `2` = Cada 2 frames (recomendado)
- `5` = Cada 5 frames (más lento pero seguro)

---

## 🚀 Uso

### Iniciar el Sistema

1. **Encender ESP32** (conectado a corriente)
2. **Ejecutar el sistema EPP normal:**

   ```powershell
   python main.py
   ```

3. Verás estos mensajes nuevos:

   ```
   ================================================================================
   🚦 SISTEMA ESP32 ACTIVADO
   ================================================================================
   🔧 Worker ESP32 activo en segundo plano
   📡 Enviando a ESP32 cada 2 frames
   ================================================================================
   ```

4. Cuando detecte personas, verás:
   ```
   🚦 [ESP32] Personas: 3 → Color: VERDE [Cola: 0]
       💡 ESP32: LED → VERDE
   ```

### Probar Conexión

```powershell
python esp32/esp32_client.py
```

Esto probará la conexión y hará parpadear los LEDs.

### Ver Estado del ESP32

Abrir en navegador: `http://IP_DEL_ESP32/`

Verás una página con:

- Estado actual del LED
- Número de comandos recibidos
- Tiempo encendido

---

## 🐛 Troubleshooting

### ❌ Error: "ESP32: No se pudo conectar"

**Causas posibles:**

1. **ESP32 no está encendido**

   - ✅ Verificar que esté conectado y el LED integrado parpadea

2. **IP incorrecta**

   - ✅ Revisar IP en Monitor Serial del Arduino
   - ✅ Actualizar `ESP32_IP` en `esp32_config.py`

3. **No están en la misma red WiFi**

   - ✅ PC y ESP32 deben estar en la misma red
   - ✅ Probar ping: `ping 192.168.1.100`

4. **Firewall bloqueando**
   - ✅ Desactivar firewall temporalmente
   - ✅ Agregar excepción para Python

### ⚠️ ESP32 no conecta a WiFi

**Soluciones:**

1. **Verificar SSID y contraseña** en `led_server.ino`

   - Mayúsculas y minúsculas importan
   - Sin espacios extra

2. **Red debe ser 2.4 GHz**

   - ESP32 NO soporta 5 GHz
   - Si tienes red dual, conectar a 2.4 GHz

3. **Verificar en Monitor Serial**
   - Ver mensajes de error específicos
   - Si dice "..." sin conectar, revisar contraseña

### 🔴 LEDs no encienden

**Soluciones:**

1. **Verificar conexiones físicas**

   - Resistencias bien conectadas
   - LEDs en polaridad correcta (pata larga = +)

2. **Probar con LED integrado**

   - Cambiar pines a `LED_BUILTIN` temporalmente
   - Si funciona, problema es hardware externo

3. **Medir voltaje**

   - Con multímetro, verificar ~3.3V en GPIO

4. **Usar endpoint de prueba**
   - Abrir: `http://IP_ESP32/test`
   - Debe hacer secuencia de colores

### 🐌 Sistema va lento

**Soluciones:**

1. **Aumentar frames procesados**

   ```python
   PROCESAR_CADA_N_FRAMES_ESP32 = 5  # Menos frecuente
   ```

2. **Reducir timeout**

   ```python
   HTTP_TIMEOUT = 0.5  # Más rápido, pero menos tolerante
   ```

3. **Verificar WiFi**
   - Acercar ESP32 al router
   - Verificar señal fuerte

---

## 🔌 Desactivar el Sistema

### Método 1: Desde Configuración (Recomendado)

Editar `esp32/esp32_config.py` línea 18:

```python
USAR_ESP32 = False  # ← Cambiar a False
```

### Método 2: Comentar en main.py

Editar `main.py`, comentar estas líneas:

```python
# from esp32.esp32_worker import iniciar_worker_esp32, agregar_detecciones_esp32
```

Y más abajo:

```python
# iniciar_worker_esp32()
# agregar_detecciones_esp32(clases)
# agregar_detecciones_esp32([])
```

### Método 3: Eliminar Módulo (Permanente)

```powershell
Remove-Item -Recurse -Force esp32
```

Luego revertir cambios en `main.py` usando Git:

```powershell
git checkout main.py
```

---

## 📊 Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────┐
│         ROBOFLOW (Stream en vivo)                    │
│         Detecciones cada frame                       │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │   my_sink()    │  ← Recibe CADA frame
            └────────┬───────┘
                     │
        ┌────────────┴─────────────┐
        │                          │
        ▼                          ▼
┌───────────────┐        ┌──────────────────┐
│ Sistema Actual│        │  ESP32 Worker    │
│ (cada 5 seg)  │        │  (cada 2 frames) │
│               │        │                  │
│ • BD          │        │ • Contar clases  │
│ • Imágenes    │        │ • Calcular color │
│ • Métricas    │        │ • HTTP a ESP32   │
└───────────────┘        └──────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   ESP32         │
                         │   • WiFi        │
                         │   • HTTP Server │
                         │   • Control LED │
                         └─────────────────┘
```

---

## 🎓 Estructura de Archivos

```
esp32/
├── __init__.py           # Módulo Python
├── esp32_config.py       # ⚙️ Configuración (IP, lógica)
├── esp32_client.py       # 📡 Cliente HTTP
├── esp32_worker.py       # 🔧 Worker con cola
└── arduino/
    └── led_server.ino    # 💾 Código para ESP32
```

---

## 🔒 Seguridad

- El sistema ESP32 es **totalmente independiente**
- Si falla, el sistema principal continúa sin problemas
- La cola tiene límite (no se satura memoria)
- Timeout de 1 segundo (no bloquea)

---

## 📈 Mejoras Futuras

Ideas para expandir el sistema:

1. **Buzzer/Alarma** cuando hay incumplimiento
2. **Display LCD** mostrando número de personas
3. **Telegram Bot** enviando alertas
4. **Dashboard web** desde el ESP32
5. **Múltiples ESP32** en diferentes áreas

---

## 🆘 Soporte

Si tienes problemas:

1. Revisar esta documentación
2. Verificar logs en consola
3. Probar endpoint `/test` del ESP32
4. Verificar Monitor Serial del Arduino
5. Probar con `python esp32/esp32_client.py`

---

## 📝 Changelog

**v1.0.0** (2 Nov 2025)

- ✨ Lanzamiento inicial
- 🚦 Sistema de 3 colores (Rojo/Naranja/Verde)
- 📡 Comunicación HTTP
- 🔧 Worker independiente
- 📖 Documentación completa

---

## ❤️ Créditos

Sistema desarrollado como módulo adicional para el proyecto EPP-UCP-2025.

---

**¡Disfruta tu sistema de alertas en tiempo real! 🚀**
