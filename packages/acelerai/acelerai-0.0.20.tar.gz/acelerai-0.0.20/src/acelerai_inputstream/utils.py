from datetime import date, datetime
from enum import Enum
import hashlib
import json
import os
from uuid import UUID
import msgpack
from decimal import Decimal
from dateutil import parser

import logging
logger = logging.getLogger("AcelerUtil")

def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
        
    if isinstance(obj, Decimal):
        return float(obj)  # Serializar Decimal como flotante
    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")


def decode_datetime(obj):
    for key, value in obj.items():
        if isinstance(value, str):
            try:
                obj[key] = datetime.fromisoformat(value)  # Deserializar datetime
            except ValueError:
                pass
        elif isinstance(value, float):
            obj[key] = float(value)  # Convertir flotantes de regreso a Decimal
    return obj


def load_full_object(file_path):
    """Carga completamente el objeto desde un archivo MessagePack en memoria."""
    try:
        with open(file_path, "rb") as file:
            # Cargar todos los registros en memoria como una lista
            unpacker = msgpack.Unpacker(file, raw=False, object_hook=decode_datetime)
            data = [record for record in unpacker]  # Deserializar todos los registros
        return data
    except Exception as e:
        logger.error(f"Error al cargar el archivo: {e}", exc_info=True)
        return None
    

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        
        elif isinstance(obj, datetime):
            return obj.isoformat()
        
        elif isinstance(obj, date):
            return obj.isoformat()
        
        elif isinstance(obj, UUID):
            return str(obj)
        else:
            return super().default(obj)


class CustomJsonDecoder(json.JSONDecoder):
    def __init__(self, *args ,**kargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kargs)

    def object_hook(self, obj:dict):
        for k, v in obj.items():
            if isinstance(v, str) and 'T' in v and '-' in v and ':' in v and len(v) < 40:
                try:
                    dv = parser.parse(v)
                    dt = dv.replace(tzinfo=None)
                    obj[k] = dt
                except:
                    pass
            elif isinstance(v, str) and '-' in v and len(v) < 11:
                try:
                    obj[k] = parser.parse(v).date()
                except:
                    pass
        return obj



