"""
🚀 SCRIPT DE INICIO COMPLETO - BACKEND + FRONTEND
Inicia todo el sistema EPP Monitor automáticamente
"""
import subprocess
import time
import sys
import os
import psutil

def cerrar_procesos_python():
    """Cierra todos los procesos Python excepto este script"""
    print("\n🧹 Limpiando procesos Python anteriores...")
    
    proceso_actual = os.getpid()
    procesos_cerrados = 0
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Verificar si es un proceso Python
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    # No cerrar este script
                    if proc.info['pid'] != proceso_actual:
                        # Verificar si es main.py, servidor_api.py, u otros scripts del proyecto
                        cmdline = proc.info.get('cmdline', [])
                        if cmdline and any('main.py' in str(arg) or 
                                          'servidor_api' in str(arg) or 
                                          'start_backend' in str(arg) or
                                          'uvicorn' in str(arg) for arg in cmdline):
                            print(f"   🛑 Cerrando: PID {proc.info['pid']} - {' '.join(cmdline[:2])}")
                            proc.terminate()
                            procesos_cerrados += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Esperar a que terminen
        time.sleep(2)
        
        if procesos_cerrados > 0:
            print(f"   ✅ {procesos_cerrados} proceso(s) Python cerrado(s)")
        else:
            print("   ℹ️  No se encontraron procesos Python previos")
            
    except Exception as e:
        print(f"   ⚠️  Error al limpiar procesos: {e}")

def iniciar_sistema_completo():
    print("="*80)
    print("🚀 INICIANDO SISTEMA EPP MONITOR COMPLETO")
    print("="*80)
    
    # Limpiar procesos Python anteriores
    cerrar_procesos_python()
    
    procesos = []
    
    try:
        # 1. Iniciar Backend API
        print("\n📡 [1/2] Iniciando Backend API...")
        backend_process = subprocess.Popen(
            [sys.executable, "backend/servidor_api.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        procesos.append(("Backend API", backend_process))
        time.sleep(3)
        print("✅ Backend API iniciado en nueva consola (puerto 8000)")
        
        # 2. Iniciar Frontend React
        print("\n🎨 [2/2] Iniciando Frontend Dashboard...")
        
        # Verificar si node_modules existe
        frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
        node_modules = os.path.join(frontend_path, "node_modules")
        
        if not os.path.exists(node_modules):
            print("📦 Instalando dependencias del frontend (primera vez)...")
            install_process = subprocess.run(
                ["npm", "install"],
                cwd=frontend_path,
                shell=True
            )
            if install_process.returncode != 0:
                print("❌ Error instalando dependencias")
                raise Exception("npm install failed")
        
        # Iniciar frontend
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_path,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0,
            shell=True
        )
        procesos.append(("Frontend Dashboard", frontend_process))
        time.sleep(3)
        print("✅ Frontend iniciado en nueva consola (puerto 3000)")
        
        # 3. Información del sistema
        print("\n" + "="*80)
        print("✅ SISTEMA INICIADO CORRECTAMENTE")
        print("="*80)
        print("💡 Se abrieron 2 ventanas nuevas:")
        print("   🔹 Backend API → http://localhost:8000")
        print("   🔹 Frontend Dashboard → http://localhost:5173")
        print("="*80)
        print("🌐 Abre tu navegador en: http://localhost:5173")
        print("   Desde el Dashboard puedes activar/desactivar la cámara")
        print("="*80)
        print("⚠️  Para detener TODO el sistema, presiona Ctrl+C aquí")
        print("="*80 + "\n")
        
        # Mantener el script corriendo
        print("⏳ Sistema activo. Esperando...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️  Señal de detención recibida...")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo sistema...")
    except Exception as e:
        print(f"\n❌ Error al iniciar: {e}")
    finally:
        # Cerrar todos los procesos
        print("\n🛑 Cerrando procesos...")
        for nombre, proceso in procesos:
            try:
                proceso.terminate()
                print(f"   ✅ {nombre} cerrado")
            except:
                pass
        
        # Dar tiempo para cerrar
        time.sleep(1)
        
        # Forzar cierre si es necesario
        for nombre, proceso in procesos:
            try:
                proceso.kill()
            except:
                pass
        
        print("\n✅ Sistema detenido completamente")
        print("="*80)

if __name__ == "__main__":
    iniciar_sistema_completo()
