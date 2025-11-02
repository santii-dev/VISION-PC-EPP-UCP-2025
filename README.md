# 🛡️ ProtekSecure - Sistema de Monitoreo EPP# 🛡️ EPP Monitor - Sistema de Monitoreo de Equipos de Protección Personal

Sistema inteligente de visión artificial para monitoreo en tiempo real del cumplimiento de equipos de protección personal (EPP) en entornos industriales.Sistema inteligente para detectar y monitorear el uso correcto de EPP (Equipos de Protección Personal) usando visión por computadora con Roboflow.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)---

[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com/)## 🎯 Características Principales

[![YOLO](https://img.shields.io/badge/YOLO-v8-00FFFF.svg)](https://ultralytics.com/)

- ✅ **Detección en Tiempo Real** - Captura y análisis de video cada 5 segundos

---- ✅ **Control Automático de Cámara** - Inicia/detiene la captura desde el Dashboard

- ✅ **Dashboard Interactivo** - Estadísticas, gráficos y tablas en tiempo real

## 📑 Tabla de Contenidos- ✅ **Glassmorphism Design** - Interfaz moderna con efectos de vidrio y colores azul corporativo

- ✅ **Base de Datos SQLite** - Almacenamiento persistente de registros y detecciones

- [Características](#-características)- ✅ **API REST** - FastAPI con endpoints para gestión de datos y control de cámara

- [Tecnologías](#-tecnologías)- ✅ **Responsive** - Funciona en desktop, tablet y móvil

- [Instalación](#-instalación)

- [Inicio Rápido](#-inicio-rápido)---

- [Estructura del Proyecto](#-estructura-del-proyecto)

- [Documentación API](#-documentación-api)## 🚀 Inicio Rápido

- [Base de Datos](#-base-de-datos)

- [Bugs Solucionados](#-bugs-solucionados)### Opción 1: Inicio Automático (Recomendado)

- [GitHub Setup](#-github-setup)

- [Créditos](#-créditos)```powershell

python INICIAR_TODO.py

---```

## ✨ CaracterísticasEsto iniciará:

### Landing Page1. Backend API (puerto 8000)

- ✅ **15 burbujas flotantes** animadas con gradientes verdes2. Frontend React (puerto 3000)

- ✅ **6 iconos flotantes** (Shield, Lock, Eye, Bell, Zap, Check) que "huyen" del cursor3. Opcionalmente: Captura de cámara (main.py)

- ✅ **Logo con efecto glass** (backdrop-filter blur)

- ✅ **Grid 3x2 de características** (Detección Tiempo Real, Alertas, Reportes, etc.)### Opción 2: Inicio Manual

- ✅ **Formulario login** con animaciones Framer Motion

- ✅ **Botón "Ver Demo"** funcional que redirige al dashboard**Terminal 1 - Backend:**

### Dashboard Principal```powershell

- ✅ **Estadísticas en tiempo real**: Total registros, cumplimiento %, promedio diariopython backend/servidor_api.py

- ✅ **Gráfico de barras**: Cumplimiento por día (últimos 7 días)```

- ✅ **Gráfico circular**: Distribución de elementos detectados

- ✅ **Tabla paginada**: 10 registros por página con filtros**Terminal 2 - Frontend:**

- ✅ **Modal detalle**: Visualización de imagen completa

- ✅ **Modal eliminar**: Confirmación antes de borrar```powershell

- ✅ **Botón "Eliminar Todos"**: Resetea IDs automáticamentecd frontend

- ✅ **Hover effects**: Color-específicos para cada botón (verde, naranja, morado, azul, rojo)npm run dev

````

### Entrenar

- ✅ **Iframe Roboflow**: Integración con modelo público "safety-helmet-z7gvj/9"**Navegador:**

- ✅ **Visualización dataset**: Métricas y ejemplos de entrenamiento

- ✅ **Fullscreen responsivo**: Adaptable a diferentes tamaños- Abre: http://localhost:3000

- Login con cualquier credencial (demo)

### Avanzado- Click en **"Sistema Inactivo"** para iniciar la cámara automáticamente

- ✅ **9 tarjetas características**: Alertas Tiempo Real, Análisis Predictivo, etc.

- ✅ **Iconos Lucide**: Zap, Cloud, BarChart3, Bell, Users, Lock, Cpu, Globe, Workflow---

- ✅ **Grid 3 columnas**: Layout adaptativo

## 🎨 Interfaz de Usuario

### Sistema de Detección (main.py)

- ✅ **YOLO v8 + Roboflow**: Detección de cascos, chalecos, personas### Landing Page

- ✅ **Procesamiento cada 5 segundos**: ~75 frames (cámara 15 FPS)

- ✅ **Worker background**: Cola de 30 peticiones, no bloquea video- Hero section con animaciones fluidas

- ✅ **Guardado automático**: Imágenes en `registros/` + datos en SQLite- 4 feature cards con hover effects

- Modal de login con simulación de carga

---- Footer con información del proyecto y creadores



## 💻 Tecnologías### Dashboard



### Backend- **Tab Overview**: Estadísticas generales (registros, personas, cumplimiento)

```- **Tab Registros**: Tabla con todos los registros históricos

fastapi==0.104.1          # Framework web API REST- **Modal Detalle**: Información por persona (cascos, chalecos, gafas)

uvicorn[standard]==0.24.0 # Servidor ASGI- **Control de Cámara**: Botón para activar/desactivar captura con popup animado

opencv-python==4.8.1.78   # Procesamiento imágenes

ultralytics==8.0.220      # YOLO v8---

pillow==10.1.0            # Manipulación imágenes

python-multipart==0.0.6   # Upload de archivos## 🎥 Control de Cámara

````

El sistema ahora puede controlar la cámara directamente desde el Dashboard:

### Frontend

````json### Iniciar Cámara:

{

  "react": "^18.2.0",1. Click en **"Sistema Inactivo"** (botón en header)

  "vite": "^5.0.8",2. Verás popup: **"Conectando con cámara..."** 🔄

  "framer-motion": "^10.16.16",3. Luego: **"¡Cámara conectada!"** ✅

  "axios": "^1.6.2",4. El sistema comienza a capturar y enviar detecciones al backend

  "lucide-react": "^0.294.0",

  "recharts": "^2.10.3",### Detener Cámara:

  "react-router-dom": "^6.20.1"

}1. Click en **"Sistema Activo"**

```2. Popup: **"Deteniendo cámara..."**

3. La cámara se detiene de forma ordenada

### Infraestructura

- **Python 3.11+** - Lenguaje backend### Verificación Automática:

- **Node.js 18+** - Entorno frontend

- **SQLite3** - Base de datos local- El Dashboard verifica el estado cada 5 segundos

- **Git** - Control de versiones- Si la cámara se cierra externamente, el botón se actualiza automáticamente



------



## 🛠️ Instalación## 📁 Estructura del Proyecto



### 1. Clonar repositorio```

```bashEPPdev/

git clone https://github.com/TU_USUARIO/proteksecure-epp.git├── backend/

cd proteksecure-epp│   ├── BD/

```│   │   ├── epp_registros.db        # Base de datos SQLite

│   │   └── operaciones_bd.py       # CRUD operations

### 2. Instalar dependencias Python│   ├── cumplimiento.py             # Cálculo de cumplimiento EPP

```bash│   ├── image_utils.py              # Procesamiento de imágenes

pip install -r requirements.txt│   └── servidor_api.py             # FastAPI server + control de cámara

```│

├── frontend/

### 3. Instalar dependencias Node│   ├── src/

```bash│   │   ├── pages/

cd frontend│   │   │   ├── LandingPage.jsx     # Página de aterrizaje

npm install│   │   │   ├── Dashboard.jsx       # Dashboard principal + control de cámara

cd ..│   │   │   ├── LandingPage.css

```│   │   │   └── Dashboard.css

│   │   ├── App.jsx                 # Router principal

---│   │   └── index.css               # Estilos globales (colores azules)

│   ├── package.json

## 🚀 Inicio Rápido│   └── vite.config.js

│

### Opción 1: Automático (Recomendado)├── main.py                          # Cliente de captura (controlado por Dashboard)

```bash├── INICIAR_TODO.py                  # Script de inicio automático

python INICIAR_TODO.py├── COMANDOS_MANUALES.md            # Guía completa de comandos

```├── CAMBIOS_FINALES.txt             # Resumen de últimos cambios

Esto inicia:└── README.md                        # Este archivo

1. ✅ Inicializa base de datos SQLite```

2. ✅ Servidor backend FastAPI (puerto 8000)

3. ✅ Servidor frontend Vite (puerto 5173)---

4. ✅ Abre navegador automáticamente

## 🔌 Endpoints API

### Opción 2: Manual

### Registros

**Terminal 1 - Backend:**

```bash- `GET /api/registros` - Obtener todos los registros

cd backend- `GET /api/registros/{id}` - Obtener detalle de un registro

python servidor_api.py- `POST /api/registros` - Crear nuevo registro (usado por main.py)

```- `GET /api/estadisticas` - Estadísticas generales



**Terminal 2 - Frontend:**### Control de Cámara (Nuevo!)

```bash

cd frontend- `GET /api/camera/status` - Verificar estado de la cámara

npm run dev- `POST /api/camera/start` - Iniciar captura de cámara

```- `POST /api/camera/stop` - Detener captura de cámara



**Terminal 3 - Sistema Detección (Opcional):**---

```bash

python main.py## 🛠️ Tecnologías

````

### Backend

**Navegador:**

- Frontend: http://localhost:5173- **FastAPI** - Framework web moderno y rápido

- API Docs: http://localhost:8000/docs- **SQLite** - Base de datos ligera y eficiente

- **Roboflow Inference** - Detección de objetos con IA

---- **OpenCV** - Procesamiento de video

- **psutil** - Control de procesos del sistema

## 📁 Estructura del Proyecto

### Frontend

````

proteksecure-epp/- **React 18** - Librería UI declarativa

│- **Vite** - Build tool ultra rápido

├── 📄 .gitignore                    # Exclusiones Git- **Framer Motion** - Animaciones fluidas

├── 📄 requirements.txt              # Dependencias Python- **Axios** - Cliente HTTP

├── 📄 INICIAR_TODO.py              # Script inicio automático- **React Router** - Navegación SPA

├── 📄 INICIALIZAR.py               # Setup base de datos- **Lucide React** - Iconos modernos

├── 📄 main.py                       # Sistema detección YOLO (214 líneas)

├── 📄 COMANDOS_MANUALES.md         # Guía inicio manual (337 líneas)---

│

├── 📂 backend/## 🎨 Diseño

│   ├── servidor_api.py             # API FastAPI

│   ├── cumplimiento.py             # Lógica análisis EPP### Colores (Marca Corporativa)

│   ├── image_utils.py              # Utilidades imágenes

│   └── BD/- **Primario**: #0066FF (Azul brillante)

│       ├── operaciones_bd.py       # CRUD SQLite (280+ líneas)- **Secundario**: #003D99 (Azul oscuro)

│       └── base_datos.db           # Base datos (auto-generada)- **Acento**: #0088FF (Azul cielo)

│- **Background**: Degradado azul oscuro (#0a1929 → #001e3c)

├── 📂 frontend/

│   ├── package.json                # Dependencias React### Efectos

│   ├── vite.config.js              # Config Vite

│   ├── logo/- **Glassmorphism**: `backdrop-filter: blur(10px)` + fondos semi-transparentes

│   │   ├── ProtekSecure.png        # Logo completo- **Shadows**: Sombras azules con `rgba(0, 102, 255, 0.3)`

│   │   └── ProtekSecure_sintexto.png- **Animations**: Transiciones rápidas (0.2s-0.5s) con Framer Motion

│   └── src/

│       ├── App.jsx                 # Raíz + routing---

│       ├── index.css               # Estilos globales (253 líneas)

│       ├── pages/## 📊 Funcionamiento

│       │   ├── LandingPage.jsx     # Landing (495 líneas)

│       │   ├── Dashboard.jsx       # Dashboard (1037 líneas)### 1. Captura de Video

│       │   ├── Entrenar.jsx        # Roboflow iframe

│       │   └── Avanzado.jsx        # Features avanzadas- main.py se conecta a stream RTSP (configurable)

│       └── styles/- Procesa 1 frame cada 75 frames (~5 segundos a 15 FPS)

│           ├── Dashboard.css       # Estilos dashboard (968 líneas)- Detecta: personas, cascos, chalecos, gafas

│           ├── LandingPage.css     # Animaciones landing

│           ├── Entrenar.css### 2. Procesamiento

│           └── Avanzado.css

│- Calcula cumplimiento proporcional por categoría

└── 📂 registros/- Distribuye EPP de forma justa entre personas detectadas

    ├── .gitkeep                    # Mantiene carpeta en Git- Envía JSON al backend via POST /api/registros

    └── *.jpg (ignorados)           # Imágenes generadas

```### 3. Almacenamiento



**Total Líneas de Código**: ~4,500+- Backend guarda en SQLite:

- Frontend: ~2,800+ líneas (JSX + CSS)  - Tabla `registros`: timestamp, totales, cumplimiento

- Backend: ~850+ líneas (Python)  - Tabla `detecciones_persona`: detalle por persona

- Docs: ~500+ líneas (Markdown)

### 4. Visualización

---

- Dashboard consulta /api/registros cada 5 segundos

## 📡 Documentación API- Calcula estadísticas: promedios, máximos, mínimos

- Muestra gráficos de barras con porcentajes animados

### Base URL- Tabla interactiva con modal de detalle

````

http://localhost:8000---

````

## 🔐 Credenciales de Prueba

### Endpoints

El sistema usa login simulado. Cualquier credencial funciona:

#### 1. Obtener todos los registros

```http```

GET /api/registrosUsuario: admin | Contraseña: admin

```Usuario: demo  | Contraseña: demo

**Response:**Usuario: test  | Contraseña: test

```json```

[

  {---

    "id": 1,

    "timestamp": "2024-01-15T10:30:00",## 🐛 Solución de Problemas

    "total_personas": 5,

    "con_casco": 4,### Puerto ocupado (8000 o 3000)

    "con_chaleco": 3,

    "cumplimiento_total": 70.0,```powershell

    "imagen_path": "registros/deteccion_001.jpg"# Buscar proceso

  }netstat -ano | findstr :8000

]

```# Terminar proceso (reemplaza PID)

taskkill /PID <PID> /F

#### 2. Obtener registro por ID```

```http

GET /api/registros/{id}### Error de módulos Python

````

````powershell

#### 3. Eliminar registropip install -r requirements.txt

```http```

DELETE /api/registros/{id}

```### Error de dependencias Node



#### 4. Eliminar todos los registros```powershell

```httpcd frontend

DELETE /api/registrosrm -Recurse -Force node_modules

```npm install

**Nota**: Resetea automáticamente los IDs (AUTOINCREMENT)```



#### 5. Documentación interactiva### Cámara no inicia desde Dashboard

````

http://localhost:8000/docs1. Verifica que el backend esté corriendo

````2. Abre DevTools (F12) y mira la consola

3. Verifica el estado: GET http://localhost:8000/api/camera/status

---4. Intenta inicio manual: `python main.py` para ver errores



## 🗄️ Base de Datos---



### Esquema SQLite## 📝 Comandos Útiles



**Tabla: `registros`**### Verificar Backend

```sql

CREATE TABLE registros (```powershell

    id INTEGER PRIMARY KEY AUTOINCREMENT,curl http://localhost:8000

    timestamp TEXT NOT NULL,```

    total_personas INTEGER DEFAULT 0,

    personas_con_casco INTEGER DEFAULT 0,### Verificar Estado de Cámara

    personas_con_chaleco INTEGER DEFAULT 0,

    personas_sin_casco INTEGER DEFAULT 0,```powershell

    personas_sin_chaleco INTEGER DEFAULT 0,curl http://localhost:8000/api/camera/status

    cumplimiento_casco REAL DEFAULT 0.0,```

    cumplimiento_chaleco REAL DEFAULT 0.0,

    cumplimiento_total REAL DEFAULT 0.0,### Ver logs del Backend

    imagen_path TEXT,

    elementos_detectados TEXTLos logs aparecen en la terminal donde corre `servidor_api.py`

);

```### Hard Reload del Frontend



### Reset IDsEn el navegador: `Ctrl + Shift + R`

El sistema resetea automáticamente los IDs al eliminar todos los registros:

```python---

cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'registros'")

conn.commit()## 👥 Creadores

conn.execute("VACUUM")

```**Proyecto Colectivo**

Universidad Católica de Pereira

---

- Santiago Taba Sepúlveda

## 🐛 Bugs Solucionados- Ángel David Sánchez Calle

- Nicolás Patiño Rivera

### 1. Burbujas Saltando al Escribir

**Problema**: `Math.random()` recalculaba posiciones en cada render.---



**Solución**: Usar `useMemo` para calcular una sola vez.## 📄 Licencia

```jsx

const burbujas = useMemo(() => {Este proyecto es parte de un trabajo académico de la Universidad Católica de Pereira.

  return Array.from({ length: 15 }, (_, i) => ({

    id: i,---

    left: Math.random() * 100,

    top: Math.random() * 100,## 📅 Última actualización

    // ...

  }))1 de noviembre de 2025

}, [])

```---



### 2. Conflictos CSS Height/Scroll## 🚀 Próximos Pasos

**Problema**: Landing requiere scroll, Dashboard requiere height fijo.

Si quieres extender el sistema:

**Solución**: Clase condicional `.authenticated` con `useEffect` en App.jsx.

```css1. **Exportar reportes** - Agregar botón para descargar CSV/PDF

/* Sin autenticar: landing page */2. **Notificaciones** - Alertas cuando cumplimiento < 80%

html:not(.authenticated), body:not(.authenticated) {3. **Múltiples cámaras** - Soporte para varios streams simultáneos

  min-height: 100vh;4. **Histórico de imágenes** - Guardar frames con detecciones

  overflow-y: auto;5. **Autenticación real** - JWT tokens con usuarios persistentes

}6. **Configuración** - Panel para ajustar frecuencia de captura



/* Autenticado: dashboard */---

html.authenticated, body.authenticated {

  height: 100%;## 📚 Documentación Adicional

  overflow: hidden;

}- **COMANDOS_MANUALES.md** - Guía detallada de inicio paso a paso

```- **CAMBIOS_FINALES.txt** - Resumen de últimas correcciones

- **CORRECCIONES_APLICADAS.txt** - Historial de bugs corregidos

### 3. IDs No Se Resetean al Borrar Todo

**Problema**: SQLite `AUTOINCREMENT` mantiene contador interno en `sqlite_sequence`.---



**Solución**: Eliminar registro de `sqlite_sequence` + ejecutar `VACUUM`.¡Gracias por usar EPP Monitor! 🛡️✨

```python
def eliminar_todos_registros():
    cursor.execute("DELETE FROM registros")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'registros'")
    conn.commit()  # ← Commit ANTES de VACUUM
    conn.execute("VACUUM")  # ← VACUUM fuera de transacción
````

### 4. Error VACUUM en Transacción

**Problema**: `VACUUM` no puede ejecutarse dentro de una transacción.

**Solución**: Mover `commit()` ANTES de `VACUUM`.

### 5. Animaciones Afectando Inputs

**Problema**: Animaciones causaban re-renders al escribir en login.

**Solución**: `useMemo` evita recálculo de animaciones.

---

## 🌐 GitHub Setup

### 1. Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre: `proteksecure-epp-monitoring`
3. Descripción: `Sistema de monitoreo cumplimiento EPP con YOLO, React y FastAPI`
4. **NO** marcar "Initialize with README"
5. Click "Create repository"

### 2. Subir código

```bash
# Inicializar Git
git init

# Agregar archivos (respeta .gitignore)
git add .

# Commit inicial
git commit -m "Initial commit: ProtekSecure EPP monitoring system"

# Conectar con GitHub (cambiar TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/proteksecure-epp-monitoring.git

# Subir
git branch -M main
git push -u origin main
```

### 3. Archivos excluidos (.gitignore)

- `__pycache__/` y `*.pyc` (binarios Python)
- `node_modules/` (dependencias Node)
- `backend/BD/*.db` (base de datos local)
- `registros/*.jpg` (imágenes generadas)
- Logs y temporales

### 4. Archivos incluidos

- ✅ Todo el código fuente (frontend + backend)
- ✅ Documentación (README, COMANDOS_MANUALES)
- ✅ Scripts de inicio (INICIAR_TODO, INICIALIZAR)
- ✅ requirements.txt y package.json
- ✅ Logos del proyecto
- ✅ .gitignore y .gitkeep

---

## 🎨 Esquema de Colores

### Tema Verde Seguridad

```css
--primary-green: #10b981    /* Verde principal */
--green-600: #059669        /* Verde medio */
--green-400: #34d399        /* Verde claro */
--green-700: #047857        /* Verde oscuro */
```

### Colores Hover Botones

- **Sistema** (verde): `#10b981`
- **Entrenar** (naranja): `#f97316`
- **Avanzado** (morado): `#a855f7`
- **Refresh** (azul): `#3b82f6`
- **Logout** (rojo): `#ef4444`

---

## 🔧 Comandos Útiles

### Backend

```bash
# Iniciar API
python backend/servidor_api.py

# Verificar base de datos
python -c "from backend.BD.operaciones_bd import obtener_todos_registros; print(obtener_todos_registros())"

# Resetear BD
python INICIALIZAR.py
```

### Frontend

```bash
# Desarrollo
cd frontend
npm run dev

# Build producción
npm run build

# Preview build
npm run preview
```

### Sistema Detección

```bash
# Iniciar captura YOLO
python main.py

# Ver logs
tail -f detections_log.txt
```

---

## 🚨 Troubleshooting

### Error: Puerto 8000 ocupado

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Error: Puerto 5173 ocupado

```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Error: Módulo no encontrado

```bash
pip install -r requirements.txt
cd frontend && npm install
```

### Error: Base de datos bloqueada

```bash
python INICIALIZAR.py
```

### Error: Cámara no detectada

```python
# En main.py, cambiar:
pipeline = InferencePipeline.init(
    model_id="safety-helmet-z7gvj/9",
    video_reference=0,  # ← Cambiar a 1, 2, o ruta de video
    # ...
)
```

---

## 📊 Estadísticas del Proyecto

- **Archivos JSX**: 6 (Frontend React)
- **Archivos Python**: 6 (Backend FastAPI)
- **Archivos CSS**: 5 (Estilos)
- **Líneas de código**: ~4,500+
- **Dashboard.jsx**: 1,037 líneas
- **LandingPage.jsx**: 495 líneas
- **operaciones_bd.py**: 280+ líneas
- **Dashboard.css**: 968 líneas
- **index.css**: 253 líneas

---

## 🔮 Mejoras Futuras

### Backend

- [ ] Autenticación JWT real
- [ ] Base de datos PostgreSQL
- [ ] Websockets para actualizaciones tiempo real
- [ ] Rate limiting y validación robusta
- [ ] Exportar datos a CSV/PDF

### Frontend

- [ ] Modo oscuro/claro
- [ ] Filtros avanzados tabla
- [ ] Dashboard personalizable
- [ ] Notificaciones push
- [ ] Gráficos adicionales

### Detección

- [ ] Múltiples cámaras simultáneas
- [ ] Grabación video de incidentes
- [ ] Alertas sonoras
- [ ] Modelo custom entrenado
- [ ] Detección adicional (guantes, botas)

### DevOps

- [ ] Docker containerización
- [ ] CI/CD GitHub Actions
- [ ] Tests unitarios (pytest, jest)
- [ ] Logging estructurado
- [ ] Monitoring (Prometheus/Grafana)

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 👥 Créditos

**Desarrolladores**:

- Santiago Valencia
- Juan Sebastián Moreno

**Tecnologías**:

- React 18 + Vite
- FastAPI + Uvicorn
- YOLO (Ultralytics)
- Roboflow Universe
- SQLite3
- Framer Motion

**Proyecto**: Sistema de Monitoreo Cumplimiento EPP  
**Fecha**: Noviembre 2024 - Enero 2025

---

## 📞 Soporte

Para reportar bugs o solicitar funcionalidades, abre un issue en GitHub:

```
https://github.com/TU_USUARIO/proteksecure-epp-monitoring/issues
```

---

## 🎉 ¡Gracias por usar ProtekSecure!

Si este proyecto te fue útil, considera darle una ⭐ en GitHub.

**¡Mantén tu lugar de trabajo seguro! 🛡️🔒**



# 🚀 GUÍA DE INICIO MANUAL DEL SISTEMA EPP

## 📋 Pre-requisitos

Asegúrate de tener instalado:

- Python 3.11+
- Node.js 18+
- npm o yarn

---

## 🎯 OPCIÓN 1: Inicio Automático (Recomendado)

### Windows PowerShell:

```powershell
python INICIAR_TODO.py
```

Esto iniciará automáticamente:

1. ✅ Backend API (puerto 8000)
2. ✅ Frontend React (puerto 3000)
3. ❓ Preguntará si deseas iniciar la cámara (opcional)

---

## 🔧 OPCIÓN 2: Inicio Manual (Paso a paso)

### 1️⃣ Iniciar el Backend (API)

Abre una terminal PowerShell en la carpeta del proyecto:

```powershell
# Navegar a la carpeta del proyecto
cd c:\Users\santi\Santiago\Universidad\EPPdev

# Iniciar el servidor FastAPI
python backend/servidor_api.py
```

**Verificar:** Deberías ver el mensaje:

```
🚀 Iniciando servidor API EPP...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Probar:** Abre http://localhost:8000 en tu navegador

---

### 2️⃣ Iniciar el Frontend (React)

Abre **OTRA** terminal PowerShell en la carpeta del proyecto:

```powershell
# Navegar a la carpeta del frontend
cd c:\Users\santi\Santiago\Universidad\EPPdev\frontend

# Iniciar el servidor de desarrollo Vite
npm run dev
```

**Verificar:** Deberías ver:

```
  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Abrir:** Ve a http://localhost:3000 en tu navegador

---

### 3️⃣ Iniciar la Cámara (Captura EPP) - OPCIONAL

Puedes iniciar la cámara de 2 formas:

#### A) Desde el Dashboard (Recomendado):

1. Abre http://localhost:3000
2. Inicia sesión (cualquier usuario/contraseña)
3. Click en el botón **"Sistema Inactivo"** en el header
4. Verás un popup: "Conectando con cámara..."
5. Cuando esté listo: "¡Cámara conectada!"

#### B) Manualmente desde terminal:

Abre **OTRA** terminal PowerShell:

```powershell
# Navegar a la carpeta del proyecto
cd c:\Users\santi\Santiago\Universidad\EPPdev

# Iniciar captura de video
python main.py
```

**Verificar:** Deberías ver:

```
🎥 Iniciando pipeline de detección EPP...
📸 Procesando frame cada 5 segundos...
```

---

## 🛑 DETENER EL SISTEMA

### Detener la cámara:

- **Desde Dashboard:** Click en "Sistema Activo" → "Deteniendo cámara..."
- **Desde terminal:** Presiona `Ctrl + C` en la terminal donde corre `main.py`

### Detener el Frontend:

Presiona `Ctrl + C` en la terminal donde corre `npm run dev`

### Detener el Backend:

Presiona `Ctrl + C` en la terminal donde corre `servidor_api.py`

---

## 📊 VERIFICAR QUE TODO FUNCIONE

### Backend funcionando:

```powershell
# Probar endpoint de estado
curl http://localhost:8000
```

Respuesta esperada:

```json
{
  "mensaje": "API EPP funcionando",
  "status": "OK"
}
```

### Frontend funcionando:

Abre http://localhost:3000 en tu navegador

- ✅ Debes ver la página de aterrizaje con efecto glassmorphism azul
- ✅ Footer con Universidad Católica de Pereira
- ✅ Botón "Ingresar al Sistema"

### Cámara funcionando:

```powershell
# Ver estado de la cámara
curl http://localhost:8000/api/camera/status
```

Respuesta esperada:

```json
{
  "status": "running",
  "mensaje": "Cámara activa",
  "pid": 12345
}
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Puerto 8000 ya en uso"

```powershell
# Buscar qué proceso usa el puerto
netstat -ano | findstr :8000

# Matar el proceso (reemplaza PID con el número que viste)
taskkill /PID <PID> /F
```

### Error: "Puerto 3000 ya en uso"

```powershell
# Buscar qué proceso usa el puerto
netstat -ano | findstr :3000

# Matar el proceso
taskkill /PID <PID> /F
```

### Error: "ModuleNotFoundError"

```powershell
# Reinstalar dependencias Python
pip install -r requirements.txt

# O instalar paquetes específicos
pip install fastapi uvicorn inference opencv-python psutil
```

### Error: Frontend no carga

```powershell
# Reinstalar dependencias Node
cd frontend
rm -Recurse -Force node_modules
npm install
npm run dev
```

---

## 📝 ESTRUCTURA DE TERMINALES RECOMENDADA

Para desarrollo, mantén **3 terminales** abiertas:

```
Terminal 1 (Backend):
📂 c:\Users\santi\Santiago\Universidad\EPPdev
▶️ python backend/servidor_api.py

Terminal 2 (Frontend):
📂 c:\Users\santi\Santiago\Universidad\EPPdev\frontend
▶️ npm run dev

Terminal 3 (Cámara - Opcional):
📂 c:\Users\santi\Santiago\Universidad\EPPdev
▶️ python main.py
```

---

## 🎯 FLUJO COMPLETO DE INICIO

### Inicio desde cero:

1. **Abrir 3 terminales PowerShell**

2. **Terminal 1 - Backend:**

   ```powershell
   cd c:\Users\santi\Santiago\Universidad\EPPdev
   python backend/servidor_api.py
   ```

   ✅ Espera ver: "Uvicorn running on http://0.0.0.0:8000"

3. **Terminal 2 - Frontend:**

   ```powershell
   cd c:\Users\santi\Santiago\Universidad\EPPdev\frontend
   npm run dev
   ```

   ✅ Espera ver: "Local: http://localhost:3000/"

4. **Navegador:**

   - Abre: http://localhost:3000
   - Login: cualquier usuario/contraseña (demo)
   - Click en "Sistema Inactivo" para iniciar cámara

5. **Ver resultados:**
   - Tab "Overview": Estadísticas generales
   - Tab "Registros": Tabla con todos los registros
   - Click "Ver Detalle": Modal con info de cada persona

---

## 🔐 CREDENCIALES DE PRUEBA

El sistema usa login simulado. Puedes usar cualquier credencial:

```
Usuario: admin
Contraseña: admin

Usuario: demo
Contraseña: demo

Usuario: test
Contraseña: test
```

---

## 📦 DEPENDENCIAS

### Backend (Python):

- fastapi
- uvicorn
- inference (Roboflow)
- opencv-python
- psutil

### Frontend (Node):

- react
- react-router-dom
- framer-motion
- axios
- lucide-react
- vite

---

## 🎨 CARACTERÍSTICAS PRINCIPALES

✅ **Glassmorphism Design** - Diseño moderno con efecto vidrio
✅ **Colores Azul** - Marca corporativa (#0066FF, #003D99, #0088FF)
✅ **Control de Cámara** - Inicio/detención desde el Dashboard
✅ **Tiempo Real** - Actualización cada 5 segundos
✅ **Detalle de Registros** - Modal con info por persona
✅ **Responsive** - Funciona en desktop, tablet y móvil
✅ **Animaciones Fluidas** - Transiciones rápidas con Framer Motion

---

## 📞 SOPORTE

**Proyecto Colectivo**
Universidad Católica de Pereira

**Creadores:**

- Santiago Taba Sepúlveda
- Ángel David Sánchez Calle
- Nicolás Patiño Rivera

---

## 📅 Última actualización: 1 de noviembre de 2025


# 🚀 GUÍA RÁPIDA - Subir a GitHub

## ✅ Archivos Finales (LIMPIEZA COMPLETADA)

### Raíz del Proyecto

```
✅ .gitignore               # Exclusiones Git
✅ requirements.txt         # Dependencias Python
✅ README.md               # Documentación completa (500+ líneas)
✅ COMANDOS_MANUALES.md    # Guía inicio manual
✅ INICIAR_TODO.py         # Script inicio automático
✅ INICIALIZAR.py          # Setup base de datos
✅ main.py                 # Sistema detección YOLO
```

### Archivos Eliminados ❌

```
❌ INICIAR_SISTEMA.py      # No se usaba
❌ GUIA_TAMAÑOS.md         # Info menor
❌ ESTADO_FINAL.md         # Consolidado en README
❌ DOCUMENTACION_COMPLETA.md  # Consolidado en README
❌ backend/__pycache__/    # Binarios Python
```

---

## 📦 Estructura Final

```
proteksecure-epp/
├── .gitignore
├── requirements.txt
├── README.md (✨ TODO EN UNO ✨)
├── COMANDOS_MANUALES.md
├── INICIAR_TODO.py
├── INICIALIZAR.py
├── main.py
│
├── backend/
│   ├── servidor_api.py
│   ├── cumplimiento.py
│   ├── image_utils.py
│   ├── __init__.py
│   └── BD/
│       ├── operaciones_bd.py
│       ├── __init__.py
│       └── base_datos.db (generado)
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── logo/
│   │   ├── ProtekSecure.png
│   │   └── ProtekSecure_sintexto.png
│   └── src/
│       ├── App.jsx
│       ├── index.css
│       ├── pages/
│       │   ├── LandingPage.jsx
│       │   ├── Dashboard.jsx
│       │   ├── Entrenar.jsx
│       │   └── Avanzado.jsx
│       └── styles/
│           ├── Dashboard.css
│           ├── LandingPage.css
│           ├── Entrenar.css
│           └── Avanzado.css
│
└── registros/
    └── .gitkeep
```

---

## 🌐 PASOS PARA SUBIR A GITHUB

### 1️⃣ Crear Repositorio en GitHub

1. Ve a: https://github.com/new
2. **Nombre**: `proteksecure-epp-monitoring`
3. **Descripción**: `Sistema de monitoreo cumplimiento EPP con YOLO, React y FastAPI`
4. **Visibilidad**: Público o Privado (tu elección)
5. **NO** marcar "Add a README file" (ya tenemos uno)
6. **NO** marcar "Add .gitignore" (ya tenemos uno)
7. Click **"Create repository"**

### 2️⃣ Abrir PowerShell en la Carpeta del Proyecto

```powershell
cd "c:\Users\santi\Santiago\Universidad\EPPdev"
```

### 3️⃣ Inicializar Git (si no está inicializado)

```powershell
git init
```

### 4️⃣ Verificar Archivos a Subir

```powershell
git status
```

Deberías ver todos los archivos en verde/rojo. Los archivos rojos serán ignorados por `.gitignore`.

### 5️⃣ Agregar Todos los Archivos

```powershell
git add .
```

### 6️⃣ Hacer Commit Inicial

```powershell
git commit -m "Initial commit: ProtekSecure EPP monitoring system with YOLO + React + FastAPI"
```

### 7️⃣ Conectar con GitHub

**IMPORTANTE**: Cambia `TU_USUARIO` por tu usuario de GitHub.

```powershell
git remote add origin https://github.com/TU_USUARIO/proteksecure-epp-monitoring.git
```

### 8️⃣ Cambiar Rama a 'main'

```powershell
git branch -M main
```

### 9️⃣ Subir a GitHub

```powershell
git push -u origin main
```

Si te pide usuario y contraseña:

- **Usuario**: Tu usuario de GitHub
- **Contraseña**: Personal Access Token (NO la contraseña de tu cuenta)

#### Crear Personal Access Token:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Marca: `repo` (acceso completo)
4. Generate token
5. Copia el token (aparece una sola vez)
6. Úsalo como contraseña en PowerShell

---

## ✅ Verificar Subida

1. Ve a: `https://github.com/TU_USUARIO/proteksecure-epp-monitoring`
2. Deberías ver:
   - ✅ README.md renderizado con todo el contenido
   - ✅ Carpetas `backend/` y `frontend/`
   - ✅ Archivos `.gitignore`, `requirements.txt`, scripts Python
   - ❌ NO deberías ver `__pycache__`, `node_modules`, `.db`, `registros/*.jpg`

---

## 🔄 Comandos Útiles Futuros

### Subir Cambios Nuevos

```powershell
git add .
git commit -m "Descripción de tus cambios"
git push
```

### Ver Estado

```powershell
git status
```

### Ver Historial

```powershell
git log --oneline
```

### Crear Rama Nueva

```powershell
git checkout -b feature/nueva-funcionalidad
```

### Volver a Rama Main

```powershell
git checkout main
```

---

## 📝 Notas Importantes

### Archivos NO Subidos (por .gitignore)

- `__pycache__/` - Binarios Python compilados
- `node_modules/` - Dependencias Node (muy pesadas)
- `*.db` - Base de datos local
- `registros/*.jpg` - Imágenes generadas (pueden ser muchas)
- `*.log` - Archivos de log
- `.env` - Variables de entorno sensibles

### Archivos SÍ Subidos

- ✅ Todo el código fuente (.py, .jsx, .css, .js)
- ✅ Documentación (.md)
- ✅ Configuración (package.json, vite.config.js)
- ✅ Dependencias (requirements.txt)
- ✅ Scripts de inicio
- ✅ Logos del proyecto
- ✅ .gitignore y .gitkeep

---

## 🎯 Después de Subir

### 1. Agregar Descripción y Tags

En tu repositorio GitHub:

- Settings → About → Edit
- Description: `Sistema de monitoreo cumplimiento EPP con YOLO, React y FastAPI`
- Website: URL del proyecto (si tienes)
- Topics: `yolo`, `react`, `fastapi`, `computer-vision`, `epp`, `safety`, `monitoring`

### 2. Crear GitHub Pages (Opcional)

Si quieres hostear el frontend:

- Settings → Pages
- Source: Deploy from branch
- Branch: `main` / `docs` (si creas carpeta docs con build)

### 3. Agregar Badge README

GitHub genera badges automáticos que puedes agregar al README:

- Stars, Forks, Issues, License, etc.

---

## 🎉 ¡Listo!

Tu proyecto está:

- ✅ Limpio (sin archivos innecesarios)
- ✅ Documentado (README completo)
- ✅ Organizado (estructura clara)
- ✅ Listo para GitHub
- ✅ Profesional

**¡Ahora solo falta ejecutar los comandos y subir! 🚀**
