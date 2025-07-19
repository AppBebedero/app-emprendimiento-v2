from flask import Flask
from config_loader import cargar_configuracion
from modulos.core.routes import core_bp
from modulos.compras.routes import compras_bp
from modulos.contabilidad.contabilidad import Accounting

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cambia-esta-clave-segura'

    @app.context_processor
    def inject_config():
        config = cargar_configuracion()
        return dict(
            config           = config,
            NombreNegocio    = config.get('NombreNegocio', ''),
            LogoURL          = config.get('LogoURL', ''),
            ColorPrincipal   = config.get('ColorPrincipal', '#0d6efd'),
            ColorFondo       = config.get('ColorFondo', '#ffffff')
        )

    app.accounting = Accounting()
    app.register_blueprint(core_bp)
    app.register_blueprint(compras_bp, url_prefix='/compras')
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
