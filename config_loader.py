import os
import json

LOCAL = os.path.join(os.path.dirname(__file__), 'config.json')

def cargar_config():
    # Siempre leemos config.json fresco
    try:
        with open(LOCAL, encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}
