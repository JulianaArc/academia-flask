from flask import Flask

from config import Config
from extensions import db, bcrypt

from models import *

from routes.auth.routes import auth_bp

from routes.admin.dashboard.routes import dashboard_bp
from routes.admin.alunos.routes import alunos_bp
from routes.admin.planos.routes import planos_bp
from routes.admin.exercicios.routes import exercicios_bp
from routes.admin.treinos.routes import treinos_bp
from routes.aluno.treinos.routes import treinos_aluno_bp

from routes.aluno.dashboard.routes import dashboard_aluno_bp


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_bp)

app.register_blueprint(dashboard_bp)
app.register_blueprint(alunos_bp)
app.register_blueprint(planos_bp)
app.register_blueprint(exercicios_bp)
app.register_blueprint(treinos_bp)
app.register_blueprint(treinos_aluno_bp)


app.register_blueprint(dashboard_aluno_bp)


def criar_admin():
    admin = Usuario.query.filter_by(cpf='admin').first()

    if not admin:
        senha_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')

        novo_admin = Usuario(
            nome='Administrador',
            cpf='admin',
            telefone='',
            senha=senha_hash,
            tipo='admin'
        )

        db.session.add(novo_admin)
        db.session.commit()

        print('✅ Admin criado')


with app.app_context():
    db.create_all()
    criar_admin()


if __name__ == '__main__':
    app.run(debug=True)


