"""
INICIALIZAR SISTEMA EPP
Ejecutar UNA VEZ antes de usar el sistema por primera vez
"""
import os
import sys

print("="*80)
print("🔧 INICIALIZANDO SISTEMA EPP")
print("="*80 + "\n")

# 1. Crear la base de datos
print("1️⃣ Creando base de datos...")
try:
    sys.path.append(os.path.dirname(__file__))
    from backend.BD.crear_bd import crear_base_datos
    crear_base_datos()
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# 2. Verificar carpeta registros
print("\n2️⃣ Verificando carpeta registros...")
registros_dir = os.path.join(os.path.dirname(__file__), "registros")
if not os.path.exists(registros_dir):
    os.makedirs(registros_dir)
    print(f"   ✅ Carpeta creada: {registros_dir}")
else:
    print(f"   ✅ Carpeta existe: {registros_dir}")

print("\n" + "="*80)
print("✅ SISTEMA INICIALIZADO CORRECTAMENTE")
print("="*80)
print("\nSiguientes pasos:")
print("1. python INICIAR_TODO.py    (inicia backend + frontend automáticamente)")
print("\nO manualmente:")
print("1. python backend/servidor_api.py   (en una terminal)")
print("2. cd frontend && npm run dev        (en otra terminal)")
print("\n")
