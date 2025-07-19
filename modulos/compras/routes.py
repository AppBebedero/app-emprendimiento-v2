# modulos/compras/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
from werkzeug.utils import secure_filename

compras_bp = Blueprint('compras', __name__, template_folder='templates')

@compras_bp.route('/', methods=['GET', 'POST'])
def compras():
    if request.method == 'POST':
        # Ejemplo de manejo: simplemente mostramos un flash y redirigimos
        fecha = request.form.get('Fecha', datetime.today().strftime('%Y-%m-%d'))
        n_doc = request.form.get('N_Documento', '')
        total = request.form.get('Total', '')
        flash(f'Compra registrada: {fecha} - Doc {n_doc} - Monto {total}', 'success')
        return redirect(url_for('compras.compras'))

    return render_template('compras.html')
