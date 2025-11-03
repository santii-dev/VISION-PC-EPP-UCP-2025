# 📡 Guía Rápida: Cambiar Red WiFi

## ⚡ Pasos rápidos (3 archivos a editar)

### 1️⃣ **ESP32 Arduino** (`esp32/arduino/led_server.ino`)

```cpp
// Líneas 47-48
const char* WIFI_SSID = "NUEVA_RED";           // ← Tu WiFi
const char* WIFI_PASSWORD = "NUEVA_CONTRASEÑA"; // ← Tu contraseña
```

**Acciones:**

- ✅ Editar líneas 47-48
- ✅ Subir código al ESP32
- ✅ Abrir Monitor Serial (115200 baud)
- ✅ Anotar la IP: `📍 IP: 192.168.X.XX`

---

### 2️⃣ **Python Config** (`esp32/esp32_config.py`)

```python
# Línea 20
ESP32_IP = "192.168.X.XX"  # ← IP del Monitor Serial
```

**Acciones:**

- ✅ Pegar la IP del paso 1

---

### 3️⃣ **Backend API** (`backend/servidor_api.py`)

Busca y reemplaza en **2 lugares**:

**Línea ~317** (función `iniciar_camara`):

```python
requests.post(
    "http://192.168.X.XX:80/led",  # ← Cambiar IP aquí
    json={"color": "verde"},
    timeout=1
)
```

**Línea ~357** (función `detener_camara`):

```python
requests.post(
    "http://192.168.X.XX:80/led",  # ← Cambiar IP aquí
    json={"color": "apagado"},
    timeout=1
)
```

**Acciones:**

- ✅ Reemplazar IP en ambas funciones

---

## 🧪 **Verificar cambios:**

1. **Reinicia el sistema:**

   ```bash
   python run_project.py
   ```

2. **Prueba conexión ESP32:**

   ```bash
   python esp32/esp32_client.py
   ```

3. **Activa cámara desde Dashboard** y verifica LED

---

## 🔍 **Buscar IPs en el proyecto:**

PowerShell:

```powershell
Select-String -Path "*.py","esp32\arduino\*.ino" -Pattern "192\.168\.\d+\.\d+" -Recurse
```

Git Bash:

```bash
grep -r "192\.168\.[0-9]\+\.[0-9]\+" --include="*.py" --include="*.ino"
```

---

## ❌ **Problemas comunes:**

### ESP32 no conecta:

- ❌ Red 5 GHz (ESP32 solo 2.4 GHz)
- ✅ Verifica SSID y contraseña
- ✅ Revisa Monitor Serial

### PC no encuentra ESP32:

- ❌ Diferentes redes
- ✅ Ping: `ping 192.168.X.XX`
- ✅ Firewall bloqueando puerto 80

---

**Resumen:** 3 archivos → 1 Arduino + 2 Python 🚀
