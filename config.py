class Config:

    SECRET_KEY = 'academia_secret'

    SQLALCHEMY_DATABASE_URI = (
        'postgresql://postgres:123456@localhost/treinos_db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    