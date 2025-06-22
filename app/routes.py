from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "<h1>Bienvenido a Quadra 🍽️</h1><p>Aquí irá tu landing page.</p>"
