from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mi_clave_secreta'  # Necesaria para sesiones, login, etc.

    # Importamos las rutas
    from .routes import main
    app.register_blueprint(main)

    return app
