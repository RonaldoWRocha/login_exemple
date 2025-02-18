from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from model.UserModel import SessionLocal, UserModel
import random
import string

auth = Blueprint('auth', __name__)

# Inicializa a sessão do banco de dados
db = SessionLocal()
user_model = UserModel(db)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')
        
        # Tenta encontrar o usuário pelo nome de usuário ou e-mail
        user = user_model.get_user_by_username(username_or_email)
        if not user:
            user = user_model.get_user_by_email(username_or_email)
        
        if user and user.password == password:
            get_flashed_messages()  # Limpa as mensagens flash antigas
            flash('Login bem-sucedido', 'success')
            return redirect(url_for('dashboard'))
        
        get_flashed_messages()  # Limpa as mensagens flash antigas
        flash('Usuário ou senha inválidos', 'danger')
    return render_template('index.html')

@auth.route('/register', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        novo_usuario = user_model.create_user(username=username, email=email, password=password)
        flash('Usuário criado com sucesso', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        
        user = user_model.get_user_by_email(email)
        if user:
            new_password = random_password()
            user_model.update_user(user.id, password=new_password)

            get_flashed_messages()  # Limpa as mensagens flash antigas
            flash('Nova senha enviada para o email com sucesso', 'success')
            return redirect(url_for('auth.login'))
        
        get_flashed_messages()  # Limpa as mensagens flash antigas
        flash('Usuário não encontrado', 'danger')
    return render_template('auth/forgot.html')

@auth.route('/logout')
def logout():
    return redirect(url_for('home'))

def random_password():    
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))