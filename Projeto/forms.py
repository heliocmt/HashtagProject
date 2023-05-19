from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Projeto.models import Usuario

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 12)])
    codigo = StringField('Código de Autenticação', validators=[DataRequired()])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    submit_login = SubmitField('Login')

class CriarContaForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 12)])
    confirmacao_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    codigo = StringField('Código de Autenticação', validators=[DataRequired()])
    submit_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
       usuario = Usuario.query.filter_by(email=email.data).first()
       if usuario:
           raise ValidationError('Email já cadastrado.')