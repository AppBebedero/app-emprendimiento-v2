from flask import Flask
from config_loader import cargar_configuracion
from modulos.core.routes import core_bp
from modulos.compras.routes import compras_bp
from modulos.contabilidad.contabilidad import Accounting

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cambia-esta-clave-segura'

    # Cada vez que renderizamos, recargamos la configuración
    @app.context_processor
    def inject_config():
        config = cargar_configuracion()
        return dict(
            config           = config,  # pasamos todo el dict a las plantillas
            nombre_negocio   = config.get('NombreNegocio', ''),
            logo_exists      = bool(config.get('LogoURL')),
            logo_url         = config.get('LogoURL', ''),
            color_principal  = config.get('ColorPrincipal', '#0d6efd'),
            color_fondo      = config.get('ColorFondo', '#ffffff')
        )

    # Instanciamos el módulo contable y lo guardamos en la app
    app.accounting = Accounting()

    # Registramos los blueprints
    app.register_blueprint(core_bp)
    app.register_blueprint(compras_bp, url_prefix='/compras')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
