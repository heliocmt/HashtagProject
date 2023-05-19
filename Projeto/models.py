from Projeto import database as db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    __tablename__= 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    senha = db.Column(db.String(20), nullable=False)

class Atualizacoes(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    __tablename__= 'atualizacoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    valor = db.Column(db.Integer, nullable = True)
    forma_pagamento = db.Column(db.String, nullable=False)
    parcelas = db.Column(db.Integer, nullable=True)
    acesso = db.Column(db.String, nullable=False)
    mensagem = db.Column(db.String, nullable=False)


