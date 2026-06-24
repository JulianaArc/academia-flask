from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from extensions import db, bcrypt

from models.usuario import Usuario
from models.plano import Plano

alunos_bp = Blueprint(
    'alunos',
    __name__
)

@alunos_bp.route('/alunos')
def alunos_dashboard():

    if session.get('tipo') != 'admin':
        return redirect('/')

    return render_template(
        'admin/alunos/menu_alunos.html'
    )

@alunos_bp.route('/listar-alunos')
def listar_alunos():

    if session.get('tipo') != 'admin':
        return redirect('/')

    alunos = Usuario.query.filter_by(
        tipo='aluno'
    ).all()

    total = len(alunos)

    ativos = len([
        a for a in alunos
        if a.ativo
    ])

    pendentes = total - ativos

    return render_template(
        'admin/alunos/listar_alunos.html',
        alunos=alunos,
        total=total,
        ativos=ativos,
        pendentes=pendentes
    )



@alunos_bp.route(
    '/cadastrar-aluno',
    methods=['GET', 'POST']
)
def cadastrar_aluno():

    if session.get('tipo') != 'admin':
        return redirect('/')

    planos = Plano.query.order_by(
        Plano.nome.asc()
    ).all()

    if request.method == 'POST':

        cpf_existente = Usuario.query.filter_by(
            cpf=request.form['cpf']
        ).first()

        if cpf_existente:

            flash(
                'CPF já cadastrado.'
            )

            return redirect(
                '/cadastrar-aluno'
            )

        senha_hash = bcrypt.generate_password_hash(
            request.form['senha']
        ).decode('utf-8')

        novo_aluno = Usuario(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            telefone=request.form['telefone'],
            senha=senha_hash,
            tipo='aluno',
            ativo=True,
            plano_id=int(
                request.form['plano_id']
            )
        )

        db.session.add(
            novo_aluno
        )

        db.session.commit()

        flash(
            'Aluno cadastrado.'
        )

        return redirect(
            '/alunos'
        )

    return render_template(
        'admin/alunos/cadastrar_aluno.html',
        planos=planos
    )



@alunos_bp.route(
    '/editar-aluno/<int:id>',
    methods=['GET', 'POST']
)
def editar_aluno(id):

    if session.get('tipo') != 'admin':
        return redirect('/')

    aluno = Usuario.query.get_or_404(
        id
    )

    planos = Plano.query.order_by(
        Plano.nome.asc()
    ).all()

    if request.method == 'POST':

        aluno.nome = request.form[
            'nome'
        ]

        aluno.cpf = request.form[
            'cpf'
        ]

        aluno.telefone = request.form[
            'telefone'
        ]

        aluno.plano_id = int(
            request.form[
                'plano_id'
            ]
        )

        db.session.commit()

        flash(
            'Aluno atualizado.'
        )

        return redirect(
            '/alunos'
        )

    return render_template(
        'admin/alunos/editar_aluno.html',
        aluno=aluno,
        planos=planos
    )


@alunos_bp.route(
    '/deletar-aluno/<int:id>'
)
def deletar_aluno(id):

    if session.get('tipo') != 'admin':
        return redirect('/')

    aluno = Usuario.query.get_or_404(
        id
    )

    db.session.delete(
        aluno
    )

    db.session.commit()

    flash(
        'Aluno removido.'
    )

    return redirect(
        '/alunos'
    )



