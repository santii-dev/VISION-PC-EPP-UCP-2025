"""
3_calcular_cumplimiento.py
Módulo para calcular cumplimiento de EPP basado en detecciones
"""
from typing import Dict, List

# Clases EPP reconocidas
CLASES_EPP = {
    "person": "Persona",
    "safety helmet": "Casco",
    "reflective vest": "Chaleco",
    "safety vest": "Chaleco",
    "safety glasses": "Gafas"
}


def calcular_cumplimiento(detecciones_roboflow: Dict) -> Dict:
    """
    Calcula el cumplimiento de EPP basado en las detecciones.
    
    Lógica:
    - Si hay 2 personas y 2 cascos → 100% cumplimiento de casco
    - Si hay 2 personas y 1 casco → 50% cumplimiento de casco
    - Si hay 2 personas y 3 cascos → 100% cumplimiento (máximo)
    - Si hay 0 personas → 0% cumplimiento (no hay nadie que evaluar)
    
    Returns:
        Dict con todas las métricas de cumplimiento
    """
    
    # Extraer datos del modelo
    if "model_1" not in detecciones_roboflow or "data" not in detecciones_roboflow["model_1"]:
        return crear_resultado_vacio()
    
    data = detecciones_roboflow["model_1"]["data"]
    
    if "class_name" not in data:
        return crear_resultado_vacio()
    
    clases_detectadas = data["class_name"]
    
    # Contar detecciones por tipo
    conteo = contar_detecciones(clases_detectadas)
    
    # MODIFICACIÓN: Guardar registro incluso si no hay personas (para estadísticas)
    # Si no hay personas, todos los cumplimientos serán 0%
    if conteo["personas"] == 0:
        # Retornar resultado vacío pero válido
        return crear_resultado_vacio()
    
    # Calcular cumplimiento por elemento
    cumplimiento_casco = calcular_cumplimiento_elemento(
        conteo["personas"], conteo["cascos"]
    )
    cumplimiento_chaleco = calcular_cumplimiento_elemento(
        conteo["personas"], conteo["chalecos"]
    )
    cumplimiento_gafas = calcular_cumplimiento_elemento(
        conteo["personas"], conteo["gafas"]
    )
    
    # Cumplimiento general (promedio de los 3 elementos)
    cumplimiento_general = (
        cumplimiento_casco + cumplimiento_chaleco + cumplimiento_gafas
    ) / 3
    
    # Calcular distribución de personas con/sin cada elemento
    distribucion = calcular_distribucion_personas(conteo)
    
    # Calcular incumplimientos totales
    incumplimientos = (
        distribucion["personas_sin_casco"] +
        distribucion["personas_sin_chaleco"] +
        distribucion["personas_sin_gafas"]
    )
    
    # Generar detecciones individuales (asumiendo distribución proporcional)
    detecciones_individuales = generar_detecciones_individuales(conteo, distribucion)
    
    return {
        "total_personas": conteo["personas"],
        "total_cascos": conteo["cascos"],
        "total_chalecos": conteo["chalecos"],
        "total_gafas": conteo["gafas"],
        "cumplimiento_general": round(cumplimiento_general, 2),
        "cumplimiento_casco": round(cumplimiento_casco, 2),
        "cumplimiento_chaleco": round(cumplimiento_chaleco, 2),
        "cumplimiento_gafas": round(cumplimiento_gafas, 2),
        "personas_con_casco": distribucion["personas_con_casco"],
        "personas_sin_casco": distribucion["personas_sin_casco"],
        "personas_con_chaleco": distribucion["personas_con_chaleco"],
        "personas_sin_chaleco": distribucion["personas_sin_chaleco"],
        "personas_con_gafas": distribucion["personas_con_gafas"],
        "personas_sin_gafas": distribucion["personas_sin_gafas"],
        "incumplimientos_totales": incumplimientos,
        "detecciones_persona": detecciones_individuales
    }


def contar_detecciones(clases: List[str]) -> Dict[str, int]:
    """Cuenta las detecciones de cada tipo de EPP"""
    conteo = {
        "personas": 0,
        "cascos": 0,
        "chalecos": 0,  # Suma de reflective vest + safety vest
        "gafas": 0
    }
    
    for clase in clases:
        clase_normalizada = CLASES_EPP.get(clase, "")
        
        if clase_normalizada == "Persona":
            conteo["personas"] += 1
        elif clase_normalizada == "Casco":
            conteo["cascos"] += 1
        elif clase_normalizada == "Chaleco":
            conteo["chalecos"] += 1
        elif clase_normalizada == "Gafas":
            conteo["gafas"] += 1
    
    return conteo


def calcular_cumplimiento_elemento(num_personas: int, num_elementos: int) -> float:
    """
    Calcula el porcentaje de cumplimiento de un elemento específico.
    
    Ejemplo:
    - 2 personas, 2 cascos → 100%
    - 2 personas, 1 casco → 50%
    - 2 personas, 3 cascos → 100% (no puede ser más de 100%)
    """
    if num_personas == 0:
        return 0.0
    
    # El cumplimiento es min(elementos/personas, 1.0) * 100
    cumplimiento = min(num_elementos / num_personas, 1.0) * 100
    return cumplimiento


def calcular_distribucion_personas(conteo: Dict) -> Dict[str, int]:
    """
    Calcula cuántas personas tienen o no tienen cada elemento.
    Asume distribución proporcional.
    """
    personas = conteo["personas"]
    
    # Calcular personas con cada elemento (mínimo entre elementos y personas)
    personas_con_casco = min(conteo["cascos"], personas)
    personas_con_chaleco = min(conteo["chalecos"], personas)
    personas_con_gafas = min(conteo["gafas"], personas)
    
    return {
        "personas_con_casco": personas_con_casco,
        "personas_sin_casco": personas - personas_con_casco,
        "personas_con_chaleco": personas_con_chaleco,
        "personas_sin_chaleco": personas - personas_con_chaleco,
        "personas_con_gafas": personas_con_gafas,
        "personas_sin_gafas": personas - personas_con_gafas
    }


def generar_detecciones_individuales(conteo: Dict, distribucion: Dict) -> List[Dict]:
    """
    Genera una lista de detecciones individuales por persona.
    Asume que las primeras N personas tienen el elemento si hay N elementos.
    """
    detecciones = []
    
    for i in range(conteo["personas"]):
        persona_num = i + 1
        
        # Asignar elementos proporcionalmente
        tiene_casco = persona_num <= distribucion["personas_con_casco"]
        tiene_chaleco = persona_num <= distribucion["personas_con_chaleco"]
        tiene_gafas = persona_num <= distribucion["personas_con_gafas"]
        
        # Calcular cumplimiento individual (% de elementos que tiene)
        elementos_que_tiene = sum([tiene_casco, tiene_chaleco, tiene_gafas])
        cumplimiento_individual = (elementos_que_tiene / 3) * 100
        
        detecciones.append({
            "numero_persona": persona_num,
            "tiene_casco": tiene_casco,
            "tiene_chaleco": tiene_chaleco,
            "tiene_gafas": tiene_gafas,
            "cumplimiento_persona": round(cumplimiento_individual, 2)
        })
    
    return detecciones


def crear_resultado_vacio() -> Dict:
    """Retorna un resultado vacío cuando no hay detecciones"""
    return {
        "total_personas": 0,
        "total_cascos": 0,
        "total_chalecos": 0,
        "total_gafas": 0,
        "cumplimiento_general": 0.0,
        "cumplimiento_casco": 0.0,
        "cumplimiento_chaleco": 0.0,
        "cumplimiento_gafas": 0.0,
        "personas_con_casco": 0,
        "personas_sin_casco": 0,
        "personas_con_chaleco": 0,
        "personas_sin_chaleco": 0,
        "personas_con_gafas": 0,
        "personas_sin_gafas": 0,
        "incumplimientos_totales": 0,
        "detecciones_persona": []
    }
