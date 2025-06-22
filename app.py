from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simulando base de datos en memoria (usa PostgreSQL luego)
usuarios = {}

# Clase User para flask-login
class User(UserMixin):
    def __init__(self, id_, username, password_hash):
        self.id = id_
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    user = usuarios.get(user_id)
    if user:
        return User(user_id, user['username'], user['password_hash'])
    return None

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Buscar usuario
        for id_, user in usuarios.items():
            if user['username'] == username:
                if check_password_hash(user['password_hash'], password):
                    user_obj = User(id_, username, user['password_hash'])
                    login_user(user_obj)
                    return redirect(url_for('dashboard'))
                else:
                    flash('Contraseña incorrecta')
                    break
        else:
            flash('Usuario no encontrado')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validar usuario único
        if any(u['username'] == username for u in usuarios.values()):
            flash('El nombre de usuario ya existe')
        else:
            user_id = str(len(usuarios) + 1)
            password_hash = generate_password_hash(password)
            usuarios[user_id] = {'username': username, 'password_hash': password_hash}
            flash('Usuario creado correctamente, por favor inicia sesión')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
