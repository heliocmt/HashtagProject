from flask import render_template, redirect, url_for, flash, request, abort
from Projeto.forms import LoginForm, CriarContaForm
from Projeto.models import Usuario, Atualizacoes
from Projeto import app, database as db, bcrypt
from flask_login import login_user, login_required, logout_user
import pandas as pd

@app.route('/', methods=['GET', 'POST'])
def login():
    form_login = LoginForm()
    form_criar_conta = CriarContaForm()
    usuario_login = Usuario.query.filter_by(email=form_login.email.data).first()
    usuario_criar_conta = Usuario.query.filter_by(email=form_criar_conta.email.data).first()

    if form_login.validate_on_submit() and 'submit_login' in request.form:
        email = form_login.email.data
        senha = form_login.senha.data
        codigo = form_login.codigo.data

        if usuario_login:
            if codigo == 'uhdfaAADF123' and bcrypt.check_password_hash(usuario_criar_conta.senha, senha):
                login_user(usuario_login, remember = form_login.lembrar_dados.data)
                flash(f'Login feito com sucesso no e-mail: {email}', 'alert-success')
                par_next = request.args.get('next')
                if par_next:
                    return redirect(par_next)
                else:
                    return redirect(url_for('inicio'))
            else:
                flash('Senha incorreta', 'alert-danger')
                return redirect(url_for('login'))
        else:
            flash('Usuário não cadastrado', 'alert-danger')
            return redirect(url_for('login'))

    if form_criar_conta.validate_on_submit() and 'submit_criar_conta' in request.form:
        email = form_criar_conta.email.data
        senha = form_criar_conta.senha.data
        codigo = form_criar_conta.codigo.data
        redirect('/inicio')
        if codigo == 'uhdfaAADF123':
            senha_cript = bcrypt.generate_password_hash(senha).decode("utf-8")
            usuario = Usuario(email=email, senha=senha_cript)
            db.session.add(usuario)
            db.session.commit()
            login_user(usuario)
            flash(f'Conta criada para o e-mail: {email}', 'alert-success')
            return redirect(url_for('inicio'))
        else:
            flash('Código de autenticação incorreto', 'alert-danger')
            return redirect(url_for('login'))

    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)

@app.route('/webhook', methods = ['POST'])
def webhook():
    if request.method == 'POST':
        dados_json = request.get_json()  # Obtém os dados JSON enviados no webhook
        if dados_json:
            nome = dados_json.get('nome')
            email = dados_json.get('email')
            status = dados_json.get('status')
            valor = dados_json.get('valor')
            forma_pagamento = dados_json.get('forma_pagamento')
            parcelas = dados_json.get('parcelas')

            if 'aprovado' in status:
                print(f'Liberar acesso do email: {email} e enviar mensagem de boas vindas')
                acesso = 'Liberado'
                mensagem = 'Enviada'
            elif 'reembolsado' in status:
                print('Retirar o acesso do aluno')
                acesso = 'Retirado'
                mensagem = 'Nada a fazer'
            elif 'recusado' in status:
                print('Enviar mensagem de pagamento recusado')
                acesso = 'Nada a fazer'
                mensagem = 'Enviada'
            else:
                acesso = 'Nada a fazer'
                mensagem = 'Nada a fazer'

            att = Atualizacoes(
                nome=nome,
                email=email,
                status=status,
                valor=valor,
                forma_pagamento=forma_pagamento,
                parcelas=parcelas,
                acesso=acesso,
                mensagem=mensagem
            )
            db.session.add(att)
            db.session.commit()
            return 'success',200
    else:
        return abort(400)

@app.route('/inicio', methods=['GET','POST'])
@login_required
def inicio():
    dados = db.session.query(Atualizacoes).all()

    df = pd.DataFrame([(d.nome, d.email, d.status, d.valor, d.forma_pagamento, d.parcelas, d.acesso, d.mensagem) for d in dados],
                      columns=['Nome', 'Email', 'Status', 'Valor', 'Forma de Pagamento', 'Parcelas', 'Acesso', 'Mensagem'])

    # Verifique se o filtro de email foi enviado no formulário
    filtro_email = request.form.get('filtro_email')
    if filtro_email:
        df = df[df['Email'] == filtro_email]

    # Renderize o DataFrame como uma tabela HTML
    tabela_html = df.to_html(index=False)

    # Renderize a página HTML com o DataFrame
    return render_template('inicio.html', tabela_html=tabela_html)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso', 'alert-success')
    return redirect(url_for('login'))
