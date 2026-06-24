from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from extensions import bcrypt
from models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(cpf=cpf).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['tipo'] = usuario.tipo

            if usuario.tipo == 'admin':
                return redirect('/dashboard-admin')

            return redirect('/dashboard-aluno')

        flash('CPF ou senha inválidos')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

