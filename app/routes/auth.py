from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.modelUser import ModelUser

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return redirect(url_for('auth.register'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = ModelUser.login(username, password)
        if user:
            login_user(user)
            return redirect(url_for('vacas.registrar_vaca'))
        else:
            flash('Usuario o contraseña incorrectos.')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash("Usuario y contraseña son obligatorios.")
            return redirect(url_for('auth.register'))
        try:
            user = ModelUser.register(username, password)
            flash("Registro exitoso. Iniciá sesión.")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(str(e))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.')
    return redirect(url_for('auth.login'))