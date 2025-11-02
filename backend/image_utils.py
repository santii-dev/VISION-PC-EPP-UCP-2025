"""
4_guardar_imagen.py
Utilidades para guardar imágenes JPG desde Roboflow
"""
import os
import base64
from datetime import datetime
from typing import Optional
import numpy as np
import cv2

# Ruta de la carpeta registros (un nivel arriba de backend)
BACKEND_DIR = os.path.dirname(os.path.dirname(__file__))
REGISTROS_DIR = os.path.join(BACKEND_DIR, "registros")

# Crear carpeta si no existe
os.makedirs(REGISTROS_DIR, exist_ok=True)


def numpy_array_a_jpg(numpy_array: list, fecha_hora: str) -> str:
    """
    Convierte un numpy array (lista) a imagen JPG y la guarda.
    
    Args:
        numpy_array: Lista de píxeles (viene del JSON serializado)
        fecha_hora: Fecha y hora del registro (formato ISO)
    
    Returns:
        Ruta relativa donde se guardó la imagen
    """
    try:
        # Convertir lista a numpy array
        img_array = np.array(numpy_array, dtype=np.uint8)
        
        # Crear nombre de archivo basado en fecha
        fecha_obj = datetime.fromisoformat(fecha_hora.replace('Z', '+00:00'))
        nombre_archivo = f"IMAGE_{fecha_obj.strftime('%Y%m%d_%H%M%S')}.jpg"
        ruta_completa = os.path.join(REGISTROS_DIR, nombre_archivo)
        
        # Guardar imagen
        cv2.imwrite(ruta_completa, img_array)
        
        # Retornar ruta relativa
        return f"registros/{nombre_archivo}"
        
    except Exception as e:
        print(f"❌ Error guardando imagen: {e}")
        return ""


def base64_a_jpg(base64_string: str, fecha_hora: str) -> str:
    """
    Convierte una imagen en base64 a JPG y la guarda.
    
    Args:
        base64_string: String en base64 de la imagen
        fecha_hora: Fecha y hora del registro (formato ISO)
    
    Returns:
        Ruta relativa donde se guardó la imagen
    """
    try:
        # Remover prefijo si existe
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decodificar base64
        img_data = base64.b64decode(base64_string)
        
        # Crear nombre de archivo
        fecha_obj = datetime.fromisoformat(fecha_hora.replace('Z', '+00:00'))
        nombre_archivo = f"IMAGE_{fecha_obj.strftime('%Y%m%d_%H%M%S')}.jpg"
        ruta_completa = os.path.join(REGISTROS_DIR, nombre_archivo)
        
        # Guardar imagen
        with open(ruta_completa, 'wb') as f:
            f.write(img_data)
        
        # Retornar ruta relativa
        return f"registros/{nombre_archivo}"
        
    except Exception as e:
        print(f"❌ Error guardando imagen desde base64: {e}")
        return ""


def extraer_imagen_del_output(output_roboflow: dict) -> Optional[str]:
    """
    Extrae la imagen del output de Roboflow en el formato que esté disponible.
    
    Prioridad:
    1. _numpy_image (lista de píxeles)
    2. _base64_image (string base64)
    
    Returns:
        Ruta donde se guardó la imagen o None si no se pudo
    """
    if "output_image" not in output_roboflow:
        return None
    
    output_image = output_roboflow["output_image"]
    
    # Extraer fecha/hora del video metadata
    fecha_hora = output_roboflow.get("output_image", {}).get(
        "_video_metadata", {}
    ).get("frame_timestamp", datetime.now().isoformat())
    
    # Intentar desde numpy array (ya convertido a lista)
    if "_numpy_image" in output_image and output_image["_numpy_image"]:
        numpy_array = output_image["_numpy_image"]
        if isinstance(numpy_array, list):
            return numpy_array_a_jpg(numpy_array, fecha_hora)
    
    # Intentar desde base64
    if "_base64_image" in output_image and output_image["_base64_image"]:
        base64_str = output_image["_base64_image"]
        if isinstance(base64_str, str) and base64_str:
            return base64_a_jpg(base64_str, fecha_hora)
    
    return None
