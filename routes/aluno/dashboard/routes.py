from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    flash
)

from extensions import db

from models.usuario import Usuario

from models.treino_modelo import (
    TreinoModelo
)

from models.aluno_treino import (
    AlunoTreino,
    AlunoTreinoExercicio
)

dashboard_aluno_bp = Blueprint(
    'dashboard_aluno',
    __name__
)

@dashboard_aluno_bp.route(
    '/dashboard-aluno'
)
def dashboard_aluno():

    if session.get('tipo') != 'aluno':
        return redirect('/')

    usuario = Usuario.query.get(
        session.get('usuario_id')
    )

    return render_template(
        'aluno/dashboard/dashboard_aluno.html',
        usuario=usuario
    )


@dashboard_aluno_bp.route(
    '/treinos-academia'
)
def treinos_academia():

    if session.get('tipo') != 'aluno':
        return redirect('/')

    treinos = TreinoModelo.query.all()

    meus_treinos = (
        AlunoTreino.query
        .filter_by(
            aluno_id=session.get(
                'usuario_id'
            )
        )
        .all()
    )

    ids_adicionados = [
        treino.nome
        for treino in meus_treinos
    ]

    print("USUARIO:", session.get('usuario_id'))
    print("TREINOS ADICIONADOS:", ids_adicionados)

    return render_template(
        'aluno/treinos/treinos_academia.html',
        treinos=treinos,
        ids_adicionados=ids_adicionados
    )

# ==================================
# ADICIONAR TREINO AO ALUNO
# ==================================
@dashboard_aluno_bp.route(
    '/adicionar-treino/<int:id>'
)
def adicionar_treino(id):

    if session.get('tipo') != 'aluno':
        return redirect('/')

    treino_modelo = (
        TreinoModelo.query
        .get_or_404(id)
    )

    treino_existente = (
        AlunoTreino.query
        .filter_by(
            aluno_id=session.get(
                'usuario_id'
            ),
            nome=treino_modelo.nome
        )
        .first()
    )

    if treino_existente:

        flash(
            'Treino já adicionado.'
        )

        return redirect(
            '/treinos-academia'
        )

    aluno_treino = AlunoTreino(

        aluno_id=session.get(
            'usuario_id'
        ),

        nome=treino_modelo.nome,

        origem='academia'
    )

    db.session.add(
        aluno_treino
    )

    db.session.commit()

    print(
        "TREINO CRIADO:",
        aluno_treino.id,
        aluno_treino.nome,
        aluno_treino.aluno_id
    )

    for item in treino_modelo.itens:

        novo_exercicio = (
            AlunoTreinoExercicio(

                treino_id=
                aluno_treino.id,

                exercicio_id=
                item.exercicio_id,

                peso=
                item.exercicio.peso_padrao,

                series=
                item.exercicio.series_padrao,

                repeticoes=
                item.exercicio.repeticoes_padrao
            )
        )

        db.session.add(
            novo_exercicio
        )

    db.session.commit()

    flash(
        'Treino adicionado com sucesso.'
    )

    return redirect(
        '/treinos-academia'
    )


# ==================================
# MEUS TREINOS
# ==================================
@dashboard_aluno_bp.route(
    '/meus-treinos'
)
def meus_treinos():

    if session.get('tipo') != 'aluno':
        return redirect('/')

    treinos = (
        AlunoTreino.query
        .filter_by(
            aluno_id=session.get(
                'usuario_id'
            )
        )
        .all()
    )

    print(
        "USUARIO LOGADO:",
        session.get(
            'usuario_id'
        )
    )

    print(
        "TREINOS ENCONTRADOS:",
        len(treinos)
    )

    for treino in treinos:

        print(
            "TREINO:",
            treino.id,
            treino.nome
        )

    return render_template(
        'aluno/treinos/meus_treinos.html',
        treinos=treinos
    )


# ==================================
# ABRIR TREINO
# ==================================

@dashboard_aluno_bp.route(
    '/meu-treino/<int:id>'
)
def abrir_treino(id):

    if session.get('tipo') != 'aluno':
        return redirect('/')

    treino = (
        AlunoTreino.query
        .filter_by(
            id=id,
            aluno_id=session.get(
                'usuario_id'
            )
        )
        .first_or_404()
    )

    return render_template(
        'aluno/treinos/abrir_treino.html',
        treino=treino
    )



# ==================================
# EXCLUIR TREINO
# ==================================

@dashboard_aluno_bp.route(
    '/excluir-treino/<int:id>'
)
def excluir_treino(id):

    if session.get('tipo') != 'aluno':
        return redirect('/')

    treino = (
        AlunoTreino.query
        .filter_by(
            id=id,
            aluno_id=session.get(
                'usuario_id'
            )
        )
        .first_or_404()
    )

    for exercicio in treino.exercicios:

        db.session.delete(
            exercicio
        )

    db.session.delete(
        treino
    )

    db.session.commit()

    flash(
        'Treino removido com sucesso.'
    )

    return redirect(
        '/meus-treinos'
    )

