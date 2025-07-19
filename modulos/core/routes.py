import os, json
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def inicio():
    return render_template('inicio.html')

@core_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    cfg_path = os.path.join(current_app.root_path, 'config.json')

    if request.method == 'POST':
        # 1) Cargo JSON actual
        try:
            with open(cfg_path, encoding='utf-8') as f:
                cfg = json.load(f)
        except:
            cfg = {}

        # 2) Actualizo campos
        cfg['NombreNegocio']  = request.form['NombreNegocio']
        cfg['ColorPrincipal'] = request.form['ColorPrincipal']
        cfg['ColorFondo']     = request.form['ColorFondo']

        # 3) Si suben logo, lo guardo y actualizo URL
        logo = request.files.get('LogoArchivo')
        if logo and logo.filename:
            fn = secure_filename(logo.filename)
            dest = os.path.join(current_app.root_path, 'static', fn)
            logo.save(dest)
            cfg['LogoURL'] = url_for('static', filename=fn, _external=True)

        # 4) Guardo JSON
        with open(cfg_path, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

        flash('Configuración actualizada.', 'success')
        return redirect(url_for('core.inicio'))

    return render_template('configuracion.html')
