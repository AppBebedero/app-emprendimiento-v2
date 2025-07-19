# modulos/core/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import os, json
from werkzeug.utils import secure_filename

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def inicio():
    # ya inyectamos config en context, solo render
    return render_template('inicio.html')

@core_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    # Ruta local del JSON de config
    cfg_path = os.path.join(current_app.root_path, 'config.json')

    if request.method == 'POST':
        # Recogemos campos del formulario
        nombre = request.form['NombreNegocio']
        color_p = request.form['ColorPrincipal']
        color_f = request.form['ColorFondo']

        # Leemos el JSON actual
        try:
            with open(cfg_path, encoding='utf-8') as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}

        # Actualizamos valores
        cfg['NombreNegocio'] = nombre
        cfg['ColorPrincipal'] = color_p
        cfg['ColorFondo'] = color_f

        # Si hay logo, lo guardamos en static y actualizamos URL
        logo = request.files.get('LogoArchivo')
        if logo and logo.filename:
            filename = secure_filename(logo.filename)
            logo_path = os.path.join(current_app.root_path, 'static', filename)
            logo.save(logo_path)
            # Asumimos que static está expuesto en /static/
            cfg['LogoURL'] = url_for('static', filename=filename, _external=True)

        # Escribimos el JSON actualizado
        with open(cfg_path, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

        flash('Configuración guardada localmente.', 'success')
        return redirect(url_for('core.inicio'))

    # GET, simplemente cargar la vista
    # El context_processor ya inyecta config
    return render_template('configuracion.html')
