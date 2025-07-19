from flask import Blueprint, render_template, request, redirect, url_for, flash
from config_loader import cargar_configuracion
import requests

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def inicio():
    config = cargar_configuracion()
    return render_template('inicio.html', config=config)

@core_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    config     = cargar_configuracion()
    url_script = config.get('URLScriptConfig', '')

    if request.method == 'POST':
        data = {
            'NombreNegocio':  request.form['NombreNegocio'],
            'ColorPrincipal': request.form['ColorPrincipal'],
            'ColorFondo':     request.form['ColorFondo']
        }
        files = {}
        logo = request.files.get('LogoArchivo')
        if logo:
            files['LogoArchivo'] = (logo.filename, logo.read(), logo.mimetype)

        try:
            if files:
                requests.post(url_script, data=data, files=files)
            else:
                requests.post(url_script, json=data)
            flash('Configuración guardada.', 'success')
        except:
            flash('Error guardando configuración.', 'danger')

        return redirect(url_for('core.inicio'))

    return render_template('configuracion.html', config=config)
