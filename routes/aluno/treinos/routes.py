from flask import (
    Blueprint,
    render_template,
    session,
    redirect
)

from models.treino_modelo import TreinoModelo

treinos_aluno_bp = Blueprint(
    'treinos_aluno',
    __name__
)

@treinos_aluno_bp.route(
    '/treinos-academia'
)
def treinos_academia():

    if session.get('tipo') != 'aluno':
        return redirect('/')

    treinos = TreinoModelo.query.all()

    return render_template(
        'aluno/treinos/treinos_academia.html',
        treinos=treinos
    )

