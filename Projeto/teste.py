from Projeto import app, database

from models import Usuario, Atualizacoes

with app.app_context():
    #user = Usuario.query.first()
    #print(user.senha)

    att = Atualizacoes.query.first()
    print(att)