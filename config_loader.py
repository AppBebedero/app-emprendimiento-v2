import os
import json
import requests

LOCAL_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def cargar_configuracion():
    """
    Intenta primero obtener configuración desde el Apps Script.
    Si falla, lee el config.json local.
    """
    # 1) Leer config local
    try:
        with open(LOCAL_CONFIG_PATH, encoding='utf-8') as f:
            local = json.load(f)
    except Exception:
        local = {}

    # 2) Intentar obtener de Apps Script
    url_script = local.get('URLScriptConfig', '')
    if url_script:
        try:
            resp = requests.get(url_script)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            pass

    # 3) Devolver config local en último recurso
    return local
