# 🚦 Sistema EPP - Detección y Alertas en Tiempo Real

Sistema completo de detección de Equipos de Protección Personal (EPP) con visión artificial y alertas LED mediante ESP32.

---

## 📋 **Contenido**

1. [Características](#características)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación Rápida](#instalación-rápida)
4. [Configuración de Red WiFi](#configuración-de-red-wifi)
5. [Hardware ESP32](#hardware-esp32)
6. [Uso del Sistema](#uso-del-sistema)
7. [Lógica de Colores LED](#lógica-de-colores-led)
8. [Estructura del Proyecto](#estructura-del-proyecto)
9. [Solución de Problemas](#solución-de-problemas)

---

## ✨ **Características**

- ✅ **Detección en tiempo real** con Roboflow (30 FPS)
- ✅ **Alertas visuales y sonoras** con ESP32 + LED RGB
- ✅ **Dashboard web** para monitoreo y control
- ✅ **Base de datos** SQLite para historial
- ✅ **Sistema modular** y escalable
- ✅ **Detección de 3 tipos de EPP**: Cascos, Chalecos, Gafas

---

## 💻 **Requisitos del Sistema**

### **Software:**

- Python 3.11+
- Node.js 18+ (para frontend)
- Arduino IDE (para ESP32)
- Git

### **Hardware:**

- PC con cámara RTSP o USB
- ESP32 (cualquier modelo)
- LED RGB ánodo común
- Buzzer con transistor NPN
- Resistencias: 3x 220Ω, 1x 1kΩ

---

## 🚀 **Instalación Rápida**

### **1. Clonar el repositorio:**

```bash
git clone https://github.com/santii-dev/VISION-PC-EPP-UCP-2025.git
cd VISION-PC-EPP-UCP-2025
```

### **2. Ejecutar instalación automática:**

```bash
python run_first_open.py
```

Este script instalará:

- ✅ Dependencias Python (backend)
- ✅ Dependencias Node.js (frontend)
- ✅ Base de datos SQLite

### **3. Iniciar el sistema:**

```bash
python run_project.py
```

Esto abrirá:

- **Backend API**: http://localhost:8000
- **Frontend Dashboard**: http://localhost:5173

---

## 📡 **Configuración de Red WiFi**

### **¿Cambias de red WiFi? Sigue estos pasos:**

#### **1. Configurar ESP32 (Arduino):**

Edita: `esp32/arduino/led_server.ino`

```cpp
// Líneas 47-48
const char* WIFI_SSID = "TU_RED_WIFI";        // ← Cambia aquí
const char* WIFI_PASSWORD = "TU_CONTRASEÑA";  // ← Cambia aquí
```

**Sube el código al ESP32** desde Arduino IDE.

#### **2. Obtener la nueva IP del ESP32:**

Abre el **Monitor Serial** en Arduino IDE (115200 baud):

```
✅ WiFi conectado
📍 IP: 192.168.X.XX  ← Anota esta IP
```

#### **3. Actualizar IP en Python:**

Edita: `esp32/esp32_config.py`

```python
# Línea 20
ESP32_IP = "192.168.X.XX"  # ← Pega la IP del Monitor Serial
```

#### **4. Actualizar IP en Backend:**

Edita: `backend/servidor_api.py`

```python
# Líneas 317 y 355 (dentro de las funciones iniciar_camara y detener_camara)
requests.post(
    "http://192.168.X.XX:80/led",  # ← Cambia aquí también
    json={"color": "verde"},
    timeout=1
)
```

**Reinicia el sistema:**

```bash
python run_project.py
```

---

## 🔌 **Hardware ESP32**

### **Conexiones LED RGB (Ánodo Común):**

| ESP32 Pin     | LED Pin   | Resistencia |
| ------------- | --------- | ----------- |
| D14 (GPIO 14) | R (Rojo)  | 220Ω        |
| D26 (GPIO 26) | G (Verde) | 220Ω        |
| D27 (GPIO 27) | B (Azul)  | 220Ω        |
| 3.3V o 5V     | Común (+) | -           |

### **Conexiones Buzzer (con Transistor NPN):**

| Componente        | Pin | Conexión                        |
| ----------------- | --- | ------------------------------- |
| Buzzer (+)        | -   | 5V del ESP32                    |
| Buzzer (–)        | -   | Colector del transistor         |
| Base transistor   | -   | Resistencia 1kΩ → D32 (GPIO 32) |
| Emisor transistor | -   | GND                             |

### **Diagrama visual:**

```
ESP32          LED RGB (Ánodo Común)
D14 ----[220Ω]---- R (Rojo)
D26 ----[220Ω]---- G (Verde)
D27 ----[220Ω]---- B (Azul)
3.3V -------------- Común (+)

ESP32          Buzzer + Transistor
D32 ----[1kΩ]----- Base (NPN)
5V ------------- Buzzer (+)
Colector ------- Buzzer (–)
Emisor --------- GND
```

---

## 🎮 **Uso del Sistema**

### **1. Activar el sistema:**

1. Abre el Dashboard: http://localhost:5173
2. Click en **"Activar Sistema"**
   - LED → 🟢 Verde + beep-beep
3. El sistema iniciará detecciones cada 5 segundos

### **2. Durante las detecciones:**

El LED cambiará según el nivel de cumplimiento EPP:

| Color      | Significado      | Sonido                   |
| ---------- | ---------------- | ------------------------ |
| 🟣 Morado  | Sin detecciones  | Silencio                 |
| 🔴 Rojo    | Personas SIN EPP | Beep cada 1 seg (alarma) |
| 🟠 Naranja | EPP parcial      | Beep corto al cambiar    |
| 🟢 Verde   | EPP completo     | Beep doble al cambiar    |

### **3. Desactivar el sistema:**

1. Click en **"Desactivar Sistema"**
   - LED → ⚫ Apagado + beep

---

## 🎨 **Lógica de Colores LED**

### **🟣 MORADO (Área vacía)**

- **Condición**: No detecta nada
- **Sonido**: Silencio
- **LED**: Rojo + Azul encendidos

### **🔴 ROJO (Incumplimiento - ALARMA)**

- **Condición**: Personas sin ningún EPP
- **Ejemplo**: 1 persona (sin casco, sin chaleco, sin gafas)
- **Sonido**: Beep cada 1 segundo (continuo)
- **LED**: Solo rojo encendido

### **🟠 NARANJA (EPP Parcial)**

- **Condición**: Personas con algunos elementos EPP
- **Ejemplos**:
  - 1 persona + 1 casco ✅
  - 2 personas + 1 casco ✅
  - 1 persona + 1 casco + 1 chaleco ✅
- **Sonido**: Beep corto al cambiar de estado
- **LED**: Rojo + Verde encendidos

### **🟢 VERDE (EPP Completo - TODO OK)**

- **Condición**: Cada persona tiene casco + chaleco + gafas
- **Ejemplos**:
  - 1 persona + 1 casco + 1 chaleco + 1 gafas ✅
  - 2 personas + 2 cascos + 2 chalecos + 2 gafas ✅
- **Sonido**: Beep doble al cambiar de estado
- **LED**: Solo verde encendido

### **⚫ APAGADO (Sistema inactivo)**

- **Condición**: Sistema desactivado
- **Sonido**: Beep corto al apagar
- **LED**: Todo apagado

---

## 📁 **Estructura del Proyecto**

```
EPPdev/
├── backend/                    # API FastAPI
│   ├── servidor_api.py        # Endpoints principales
│   ├── cumplimiento.py        # Lógica de cumplimiento EPP
│   ├── image_utils.py         # Procesamiento de imágenes
│   ├── requirements.txt       # Dependencias Python
│   └── BD/                    # Base de datos
│       ├── crear_bd.py        # Creación de tablas
│       └── operaciones_bd.py  # CRUD operations
│
├── frontend/                   # Dashboard React
│   ├── src/
│   │   ├── App.jsx            # Componente principal
│   │   └── pages/
│   │       ├── Dashboard.jsx  # Panel de control
│   │       ├── Entrenar.jsx   # Entrenamiento
│   │       └── Avanzado.jsx   # Configuración
│   ├── package.json
│   └── vite.config.js
│
├── esp32/                      # Sistema ESP32
│   ├── esp32_config.py        # Configuración y lógica
│   ├── esp32_client.py        # Cliente HTTP
│   ├── esp32_worker.py        # Worker thread
│   ├── __init__.py
│   └── arduino/
│       └── led_server.ino     # Código ESP32
│
├── main.py                     # Detección principal
├── run_project.py             # Iniciar sistema
├── run_first_open.py          # Instalación inicial
└── README.md                   # Este archivo
```

---

## 🔧 **Solución de Problemas**

### **❌ ESP32 no conecta a WiFi**

- Verifica que sea red **2.4 GHz** (ESP32 no soporta 5 GHz)
- Revisa SSID y contraseña en `led_server.ino`
- Abre Monitor Serial para ver mensajes de error

### **❌ PC no puede conectar con ESP32**

- Verifica que estén en la **misma red**
- Haz ping: `ping 192.168.X.XX`
- Revisa IP en `esp32_config.py` y `servidor_api.py`

### **❌ LED RGB no enciende**

- Verifica que sea **ánodo común** (no cátodo)
- Comprueba conexiones y resistencias
- Revisa polaridad del LED (pata larga = +)

### **❌ Buzzer no suena**

- Verifica el transistor NPN (BC547, 2N2222, etc.)
- Comprueba resistencia de 1kΩ en la base
- Revisa que el buzzer sea activo (no pasivo)

### **❌ Detecciones lentas o bloqueadas**

- Verifica FPS de cámara (debe ser 30 FPS)
- Comprueba que ESP32 responda en <500ms
- Revisa logs en consola Python

### **❌ Frontend no carga**

- Ejecuta: `cd frontend && npm install`
- Verifica que puerto 5173 esté libre
- Revisa logs en consola

---

## 📊 **Configuración de Cámara**

### **Cambiar cámara RTSP:**

Edita: `main.py` línea 235

```python
video_reference="rtsp://USUARIO:PASS@IP:PUERTO/stream1"
```

### **Usar cámara USB:**

```python
video_reference=0  # Cámara predeterminada
```

---

## 🤝 **Contribuir**

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Añadir nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT.

---

## 👨‍💻 **Autor**

**Santiago** - [@santii-dev](https://github.com/santii-dev)

---

## 📞 **Soporte**

¿Problemas? Abre un [Issue en GitHub](https://github.com/santii-dev/VISION-PC-EPP-UCP-2025/issues)

---

## 🎯 **Roadmap**

- [ ] Soporte para más tipos de EPP
- [ ] Notificaciones por email
- [ ] Dashboard móvil
- [ ] Múltiples cámaras simultáneas
- [ ] Integración con sistemas externos

---

## ⚡ **Changelog**

### v1.0.0 (2025-11-02)

- ✅ Sistema completo funcional
- ✅ Detección EPP con Roboflow
- ✅ Alertas LED RGB con ESP32
- ✅ Dashboard React
- ✅ Base de datos SQLite
- ✅ Lógica de 4 colores (Morado, Rojo, Naranja, Verde)

---

**¡Gracias por usar el Sistema EPP!** 🚀
