/*
 * ============================================================================
 * Sistema de Alertas LED - ESP32
 * ============================================================================
 * 
 * Este código crea un servidor HTTP en el ESP32 que recibe comandos
 * para controlar LEDs según las detecciones del sistema EPP.
 * 
 * HARDWARE NECESARIO:
 * - ESP32 (cualquier modelo)
 * - 3 LEDs (Rojo, Naranja/Amarillo, Verde) con resistencias 220-330Ω
 *   O un LED RGB
 * - Cables Dupont
 * - Protoboard (opcional)
 * 
 * LÓGICA DE COLORES (Sistema EPP):
 * - � MORADO: No detecta nada de nada (área vacía - SIN SONIDO)
 * - 🔴 ROJO: Personas sin EPP completo (ALERTA - Beep triple)
 * - � VERDE: Detecta elementos EPP en el área (OK - SIN SONIDO)
 * - � NARANJA: 100% EPP por persona, todos protegidos (EXCELENTE - Beep doble)
 * 
 * CONEXIONES (LED RGB ÁNODO COMÚN):
 * - GPIO 14 (D14) → Pin R (Rojo) con resistencia 220Ω
 * - GPIO 26 (D26) → Pin G (Verde) con resistencia 220Ω
 * - GPIO 27 (D27) → Pin B (Azul) con resistencia 220Ω
 * - Pin COMÚN (+) → 3.3V o 5V del ESP32
 * 
 * CONEXIONES (Buzzer SFM-27 con Transistor NPN):
 * - Buzzer (+) → 5V del ESP32
 * - Buzzer (–) → Colector del transistor NPN
 * - Base del transistor → Resistencia 1kΩ → GPIO 32 (D32)
 * - Emisor del transistor → GND
 * 
 * USO:
 * 1. Instalar Arduino IDE y soporte para ESP32
 * 2. Configurar WIFI_SSID y WIFI_PASSWORD (líneas 45-46)
 * 3. Subir este código al ESP32
 * 4. Anotar la IP que muestra en el Monitor Serial
 * 5. Configurar esa IP en esp32_config.py (línea 20)
 * 
 * ============================================================================
 */

#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

// ============================================================================
// CONFIGURACIÓN WIFI (⚠️ CAMBIAR ESTOS VALORES)
// ============================================================================
const char* WIFI_SSID = "TU_RED_WIFI";        // ← Nombre de tu WiFi
const char* WIFI_PASSWORD = "TU_CONTRASEÑA";  // ← Contraseña de tu WiFi

// ============================================================================
// CONFIGURACIÓN DE PINES (GPIOs) - CONFIRMADOS EN TEST
// ============================================================================
// LED RGB (ÁNODO COMÚN - LOW enciende, HIGH apaga)
const int PIN_LED_ROJO = 14;     // D14 → Pin R del LED RGB
const int PIN_LED_VERDE = 26;    // D26 → Pin G del LED RGB
const int PIN_LED_AZUL = 27;     // D27 → Pin B del LED RGB (para morado)

// BUZZER (CON TRANSISTOR NPN - HIGH suena, LOW silencia)
const int PIN_BUZZER = 32;       // D32 → Base del transistor NPN

// ============================================================================
// SERVIDOR HTTP (Puerto 80)
// ============================================================================
WebServer server(80);

// ============================================================================
// VARIABLES GLOBALES
// ============================================================================
String colorActual = "morado";  // Color inicial (morado = en espera)
unsigned long ultimoComando = 0;
int comandosRecibidos = 0;

// Variables para alarma de ROJO (beep continuo)
bool alarmaRojoActiva = false;
unsigned long ultimoBeepRojo = 0;
const int INTERVALO_BEEP_ROJO = 1000;  // Beep cada 1 segundo cuando está en rojo

// ============================================================================
// FUNCIONES DE CONTROL DE LEDs
// ============================================================================

// ============================================================================
// FUNCIONES DE CONTROL DE BUZZER
// ============================================================================

void beep(int duracion_ms) {
  digitalWrite(PIN_BUZZER, HIGH);  // HIGH suena (con transistor)
  delay(duracion_ms);
  digitalWrite(PIN_BUZZER, LOW);   // LOW silencia
}

void beepCorto() {
  beep(100);  // Beep de 100ms
}

void beepDoble() {
  beep(100);
  delay(100);
  beep(100);
}

void beepTriple() {
  beep(100);
  delay(100);
  beep(100);
  delay(100);
  beep(100);
}

void beepLargo() {
  beep(500);  // Beep de 500ms
}

void beepAlerta() {
  // Sonido de alerta para incumplimiento
  for (int i = 0; i < 3; i++) {
    beep(200);
    delay(100);
  }
}

// ============================================================================
// FUNCIONES DE CONTROL DE LED RGB (ÁNODO COMÚN)
// ============================================================================

void apagarTodosLEDs() {
  // LED Ánodo Común: HIGH apaga
  digitalWrite(PIN_LED_ROJO, HIGH);
  digitalWrite(PIN_LED_VERDE, HIGH);
  digitalWrite(PIN_LED_AZUL, HIGH);
}

void setColorRGB(bool r, bool g, bool b) {
  // LED Ánodo Común: LOW enciende, HIGH apaga
  digitalWrite(PIN_LED_ROJO, r ? LOW : HIGH);
  digitalWrite(PIN_LED_VERDE, g ? LOW : HIGH);
  digitalWrite(PIN_LED_AZUL, b ? LOW : HIGH);
}

void encenderLED(String color) {
  // Apagar todos primero
  apagarTodosLEDs();
  
  // Encender el color y hacer sonido correspondiente
  if (color == "apagado" || color == "off") {
    // ⚫ APAGADO: Sistema inactivo (estado natural)
    apagarTodosLEDs();  // Todo apagado
    beepCorto();  // Beep al apagar sistema
    colorActual = "apagado";
    alarmaRojoActiva = false;
    
  } else if (color == "morado" || color == "purple" || color == "magenta") {
    // 🟣 MORADO: No detecta nada de nada
    setColorRGB(true, false, true);  // R+B = Morado
    // SIN SONIDO (área vacía, silencio)
    colorActual = "morado";
    alarmaRojoActiva = false;
    
  } else if (color == "rojo" || color == "red") {
    // 🔴 ROJO: Personas sin EPP completo → ALARMA CONTINUA
    setColorRGB(true, false, false);  // Solo rojo
    beepTriple();  // Beep triple inicial
    colorActual = "rojo";
    alarmaRojoActiva = true;  // Activar alarma continua
    ultimoBeepRojo = millis();  // Resetear timer
    
  } else if (color == "verde" || color == "green") {
    // 🟢 VERDE: EPP COMPLETO (cada persona tiene casco + chaleco + gafas)
    setColorRGB(false, true, false);  // Solo verde
    beepDoble();  // Doble beep de confirmación
    colorActual = "verde";
    alarmaRojoActiva = false;
    
  } else if (color == "naranja" || color == "orange" || color == "amarillo" || color == "yellow") {
    // 🟠 NARANJA: EPP parcial (algunos elementos)
    setColorRGB(true, true, false);  // R+G = Naranja/Amarillo
    beepCorto();  // Beep corto
    colorActual = "naranja";
    alarmaRojoActiva = false;
    
  } else {
    // Color desconocido, morado por defecto
    setColorRGB(true, false, true);
    colorActual = "morado";
    alarmaRojoActiva = false;
  }
}

// ============================================================================
// ENDPOINTS HTTP
// ============================================================================

// Endpoint principal: POST /led
void handleLED() {
  if (server.method() == HTTP_POST) {
    
    // Leer JSON del body
    String body = server.arg("plain");
    
    // Parsear JSON
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, body);
    
    if (error) {
      // Error al parsear JSON
      server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"JSON inválido\"}");
      return;
    }
    
    // Extraer color del JSON
    String color = doc["color"];
    
    if (color == "") {
      server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"Falta campo 'color'\"}");
      return;
    }
    
    // Cambiar LED
    encenderLED(color);
    
    // Actualizar estadísticas
    ultimoComando = millis();
    comandosRecibidos++;
    
    // Respuesta exitosa
    String response = "{\"status\":\"ok\",\"color\":\"" + colorActual + "\",\"comandos\":" + String(comandosRecibidos) + "}";
    server.send(200, "application/json", response);
    
    // Log en Serial
    Serial.println("✅ Comando recibido: " + color + " → LED: " + colorActual);
    
  } else {
    server.send(405, "text/plain", "Método no permitido. Usar POST.");
  }
}

// Endpoint de estado: GET /
void handleRoot() {
  unsigned long tiempoEncendido = millis() / 1000;
  unsigned long tiempoUltimoComando = (millis() - ultimoComando) / 1000;
  
  String html = "<!DOCTYPE html><html><head><meta charset='UTF-8'>";
  html += "<title>ESP32 - Sistema EPP</title>";
  html += "<style>body{font-family:Arial;margin:40px;background:#f0f0f0;}";
  html += ".container{background:white;padding:20px;border-radius:10px;box-shadow:0 2px 5px rgba(0,0,0,0.1);}";
  html += ".status{font-size:24px;margin:20px 0;}";
  html += ".led{width:50px;height:50px;border-radius:50%;display:inline-block;margin:10px;}";
  html += ".rojo{background:red;} .naranja{background:orange;} .verde{background:green;}";
  html += ".activo{box-shadow:0 0 20px currentColor;}</style></head><body>";
  html += "<div class='container'>";
  html += "<h1>🚦 Sistema de Alertas EPP</h1>";
  html += "<div class='status'>Estado: <strong>" + colorActual + "</strong></div>";
  html += "<div>";
  html += "<span class='led rojo " + String(colorActual == "rojo" ? "activo" : "") + "'></span>";
  html += "<span class='led naranja " + String(colorActual == "naranja" ? "activo" : "") + "'></span>";
  html += "<span class='led verde " + String(colorActual == "verde" ? "activo" : "") + "'></span>";
  html += "</div>";
  html += "<p>📊 Comandos recibidos: " + String(comandosRecibidos) + "</p>";
  html += "<p>⏱️ Tiempo encendido: " + String(tiempoEncendido) + "s</p>";
  html += "<p>🕐 Último comando: hace " + String(tiempoUltimoComando) + "s</p>";
  html += "<hr><p><small>API: POST /led con JSON {\"color\": \"rojo|naranja|verde\"}</small></p>";
  html += "</div></body></html>";
  
  server.send(200, "text/html", html);
}

// Endpoint de prueba: GET /test
void handleTest() {
  Serial.println("🧪 Iniciando secuencia de prueba...");
  
  // Probar cada LED
  String colores[] = {"rojo", "naranja", "verde"};
  
  for (int i = 0; i < 3; i++) {
    encenderLED(colores[i]);
    delay(500);
  }
  
  // Volver a rojo
  encenderLED("rojo");
  
  server.send(200, "text/plain", "Prueba completada. Revisa los LEDs.");
  Serial.println("✅ Prueba completada");
}

// ============================================================================
// SETUP (Inicialización)
// ============================================================================
void setup() {
  // Inicializar Serial
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n");
  Serial.println("================================================================================");
  Serial.println("🚦 SISTEMA DE ALERTAS LED - ESP32");
  Serial.println("================================================================================");
  
  // Configurar pines como salida
  pinMode(PIN_LED_ROJO, OUTPUT);
  pinMode(PIN_LED_VERDE, OUTPUT);
  pinMode(PIN_LED_AZUL, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  
  // Apagar todos los LEDs y buzzer
  apagarTodosLEDs();
  digitalWrite(PIN_BUZZER, LOW);
  
  // Encender LED morado (estado inicial - en espera, sin detecciones)
  setColorRGB(true, false, true);  // Morado sin sonido
  colorActual = "morado";
  alarmaRojoActiva = false;
  
  Serial.println("✅ Pines GPIO configurados (ÁNODO COMÚN + TRANSISTOR)");
  Serial.println("   - LED Rojo: GPIO " + String(PIN_LED_ROJO) + " (D14)");
  Serial.println("   - LED Verde: GPIO " + String(PIN_LED_VERDE) + " (D26)");
  Serial.println("   - LED Azul: GPIO " + String(PIN_LED_AZUL) + " (D27)");
  Serial.println("   - Buzzer: GPIO " + String(PIN_BUZZER) + " (D32 - Transistor NPN)");
  
  // Conectar a WiFi
  Serial.println("\n📡 Conectando a WiFi: " + String(WIFI_SSID));
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 30) {
    delay(500);
    Serial.print(".");
    intentos++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi conectado");
    Serial.println("📍 IP: " + WiFi.localIP().toString());
    Serial.println("🌐 URL: http://" + WiFi.localIP().toString() + "/");
    Serial.println("📡 API: POST http://" + WiFi.localIP().toString() + "/led");
    
    // Parpadeo de éxito (verde 3 veces) - SIN sonido
    for (int i = 0; i < 3; i++) {
      setColorRGB(false, true, false);  // Verde
      delay(200);
      apagarTodosLEDs();
      delay(200);
    }
    // Volver a morado (estado inicial - en espera)
    setColorRGB(true, false, true);  // Morado sin sonido
    colorActual = "morado";
    alarmaRojoActiva = false;
    
  } else {
    Serial.println("\n❌ ERROR: No se pudo conectar a WiFi");
    Serial.println("⚠️ Verifica SSID y contraseña en líneas 45-46");
    
    // Parpadeo de error (rojo rápido)
    while (true) {
      digitalWrite(PIN_LED_ROJO, HIGH);
      delay(100);
      digitalWrite(PIN_LED_ROJO, LOW);
      delay(100);
    }
  }
  
  // Configurar endpoints del servidor
  server.on("/", handleRoot);
  server.on("/led", handleLED);
  server.on("/test", handleTest);
  
  // Iniciar servidor
  server.begin();
  Serial.println("✅ Servidor HTTP iniciado en puerto 80");
  
  Serial.println("================================================================================");
  Serial.println("✅ SISTEMA LISTO");
  Serial.println("================================================================================");
  Serial.println("💡 Configura esta IP en esp32_config.py (PC):");
  Serial.println("   ESP32_IP = \"" + WiFi.localIP().toString() + "\"");
  Serial.println("================================================================================\n");
}

// ============================================================================
// LOOP (Bucle principal)
// ============================================================================
void loop() {
  // Procesar peticiones HTTP
  server.handleClient();
  
  // 🚨 ALARMA CONTINUA cuando está en ROJO
  if (alarmaRojoActiva && (millis() - ultimoBeepRojo > INTERVALO_BEEP_ROJO)) {
    beepCorto();  // Beep cada segundo
    ultimoBeepRojo = millis();
  }
  
  // Watchdog: Si no recibe comandos en 60 segundos, parpadear naranja
  if (comandosRecibidos > 0 && (millis() - ultimoComando) > 60000) {
    // Parpadeo de advertencia (Naranja = Rojo + Verde)
    static unsigned long ultimoParpadeo = 0;
    static bool estadoParpadeo = false;
    
    if (millis() - ultimoParpadeo > 1000) {
      if (estadoParpadeo) {
        setColorRGB(true, true, false);  // Encender Naranja (R+G)
      } else {
        apagarTodosLEDs();  // Apagar todo
      }
      estadoParpadeo = !estadoParpadeo;
      ultimoParpadeo = millis();
    }
  }
}

// ============================================================================
// NOTAS ADICIONALES
// ============================================================================
/*
 * PRUEBAS:
 * 
 * 1. Desde navegador web:
 *    - Abre http://IP_DEL_ESP32/ para ver estado
 *    - Abre http://IP_DEL_ESP32/test para probar LEDs
 * 
 * 2. Desde PowerShell (PC):
 *    Invoke-RestMethod -Uri "http://IP_DEL_ESP32/led" -Method POST -Body '{"color":"verde"}' -ContentType "application/json"
 * 
 * 3. Desde Python:
 *    python esp32/esp32_client.py
 * 
 * TROUBLESHOOTING:
 * 
 * - Si no conecta a WiFi:
 *   → Verifica SSID y contraseña
 *   → Asegúrate que sea red 2.4GHz (ESP32 no soporta 5GHz)
 * 
 * - Si la PC no puede conectar:
 *   → Verifica que estén en la misma red
 *   → Haz ping: ping IP_DEL_ESP32
 * 
 * - Si los LEDs no encienden:
 *   → Verifica las conexiones
 *   → Prueba con LED integrado cambiando pines a LED_BUILTIN
 *   → Verifica polaridad de los LEDs (pata larga = +)
 */
