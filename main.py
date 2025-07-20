from flask import Flask, render_template, request, redirect, flash, jsonify
import csv
import os
import requests
from config_loader import cargar_config

app = Flask(__name__)
app.secret_key = 'clave-secreta'
config = cargar_config()

# Función para guardar en CSV
def guardar_en_csv(ruta, datos, encabezados):
    existe = os.path.exists(ruta)
    with open(ruta, mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=encabezados)
        if not existe:
            writer.writeheader()
        writer.writerow(datos)

# -------------------------
# RUTA: INICIO
# -------------------------
@app.route('/')
def inicio():
    return render_template('inicio.html', config=config)

# -------------------------
# RUTA: COMPRAS
# -------------------------
@app.route('/compras', methods=['GET', 'POST'])
def compras():
    proveedores = []
    productos = []
    try:
        with open('datos/proveedores.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            proveedores = [row['Nombre'] for row in reader]
    except: pass

    try:
        with open('datos/productos.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            productos = [row['Nombre'] for row in reader]
    except: pass

    if request.method == 'POST':
        datos = request.form.to_dict()
        datos['Total'] = float(datos['Cantidad']) * float(datos['PrecioUnitario'])

        encabezados = ['Fecha', 'N_Documento', 'Proveedor', 'Producto', 'Cantidad', 'PrecioUnitario', 'Moneda', 'Total', 'Forma_Pago', 'Observaciones']
        guardar_en_csv('datos/compras.csv', datos, encabezados)

        # Envío a Google Sheets
        try:
            requests.post(config['URLScript'], json=datos)
        except Exception as e:
            print("Error enviando a Google Sheets:", e)

        flash('Compra registrada exitosamente')
        return redirect('/compras')

    return render_template('compras.html', config=config, proveedores=proveedores, productos=productos)

# -------------------------
# RUTA: GUARDAR PROVEEDOR
# -------------------------
@app.route('/guardar_proveedor', methods=['POST'])
def guardar_proveedor():
    datos = request.get_json()
    nombre = datos.get('Nombre', '').strip()

    if not nombre:
        return jsonify({'success': False, 'message': 'Nombre requerido'})

    # Validar duplicado
    try:
        with open('datos/proveedores.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Nombre'].strip().lower() == nombre.lower():
                    return jsonify({'success': False, 'message': 'Proveedor ya existe'})
    except: pass

    proveedor = {'Nombre': nombre}
    encabezados = ['Nombre']
    guardar_en_csv('datos/proveedores.csv', proveedor, encabezados)

    try:
        requests.post(config['URLScriptProveedores'], json=proveedor)
    except Exception as e:
        print("Error enviando proveedor a Google Sheets:", e)

    return jsonify({'success': True})

# -------------------------
# RUTA: GUARDAR PRODUCTO
# -------------------------
@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    datos = request.get_json()
    nombre = datos.get('Nombre', '').strip()

    if not nombre:
        return jsonify({'success': False, 'message': 'Nombre requerido'})

    # Validar duplicado
    try:
        with open('datos/productos.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Nombre'].strip().lower() == nombre.lower():
                    return jsonify({'success': False, 'message': 'Producto ya existe'})
    except: pass

    producto = {'Nombre': nombre}
    encabezados = ['Nombre']
    guardar_en_csv('datos/productos.csv', producto, encabezados)

    try:
        requests.post(config['URLScriptProductos'], json=producto)
    except Exception as e:
        print("Error enviando producto a Google Sheets:", e)

    return jsonify({'success': True})

# -------------------------
# RUTA: CONFIGURACIÓN (opcional si la usás)
# -------------------------
@app.route('/configuracion')
def configuracion():
    return render_template('configuracion.html', config=config)

# -------------------------
# MAIN
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
