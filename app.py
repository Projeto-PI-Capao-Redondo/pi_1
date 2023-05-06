"""
API em Flask com Pydantic e Flask-Pydantic-Spec


passo a passo:
1 - pip install flask
2 - pip install flask_pydantic_spec
3 - pip install pydantic

"""
from datetime import datetime
from conect_mysql import conecta_mysql
from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
from flask_pydantic_spec import FlaskPydanticSpec, Request
from pydantic import BaseModel
from formulario_lojas import LojasForm
from flask_wtf.csrf import CSRFProtect

class LojasSchema(BaseModel):
    """ Lojas para o backend """
    id : int | None = None
    nome_loja: str
    cep: str
    rua: str
    complemento: str | None = None
    numero: int
    observacao: str | None = None
    bairro: str
    horario_funcionamento: str
    pontos_interesse: str
    resumo_estabelecimento: str | None = None
    link_site_rede_social: str | None = None
    imagem: str | None = None


conectando = conecta_mysql()
cursor = conectando.cursor()


server = Flask(__name__)
server.config['SECRET_KEY'] = 'teste'
csrf = CSRFProtect(server)
spec = FlaskPydanticSpec('Flask', title='Explicação API - Projeto PI 1')
spec.register(server)

@server.get('/')
def index():
    now = datetime.now()
    return render_template('index.html', active='index', now=now)

@server.route('/lojas', methods=['GET'])
def lojas():
    now = datetime.now()
    cursor.execute('SELECT * FROM lojas')
    lojas = cursor.fetchall()
    return render_template('lojas.html', active='lojas', now=now, lojas=lojas)

@server.route('/lojas/cadastrar', methods=['GET', 'POST'])
def cadastrar_loja():
    now = datetime.now()
    form = LojasForm(request.form)

    if request.method == 'POST':
        nome_loja = request.form['nome_loja']
        cep = request.form['cep'].replace('-', '')
        rua = request.form['rua']
        complemento = request.form['complemento']
        numero = request.form['numero']
        observacao = request.form['observacao']
        bairro = request.form['bairro']
        horario_funcionamento = request.form['horario_funcionamento']
        pontos_interesse = request.form['pontos_interesse']
        resumo_estabelecimento = request.form['resumo_estabelecimento']
        link_site_rede_social = request.form['link_site_rede_social']
        imagem = request.form['imagem']

        # Verifica se a loja já existe no banco de dados
        cursor.execute('SELECT id FROM lojas WHERE nome_loja = %s OR cep = %s', (nome_loja, cep))
        resultado = cursor.fetchone()
        if resultado:
            flash('Loja já cadastrada', 'danger')
        else:
            inserir_loja(nome_loja, cep, rua, complemento, numero, bairro, horario_funcionamento, pontos_interesse, observacao,
                resumo_estabelecimento, link_site_rede_social, imagem)
            flash('Loja cadastrada com sucesso!', 'success')
            return redirect(url_for('lojas'))
    return render_template('cadastrar_loja.html', active='cadastrar_loja', now=now, form=form)


@server.route('/roteiro', methods=['GET'])
def roteiro():
    now = datetime.now()
    return render_template('roteiro.html', active='roteiro', now=now)


def listar_lojas():
    """Retorna todas as Pessoas da base de dados."""
    cursor.execute('SELECT * FROM lojas')
    dados = cursor.fetchall()
    json = {}
    for dado in dados:
        json[dado[0]] = {"id": dado[0], "nome_loja": dado[1], "cep": dado[2], "rua": 
        dado[3], "complemento": dado[4], "numero": dado[5], "observacao": dado[6], 
        "bairro": dado[7], "horario_funcionamento": dado[8], "pontos_interesse": dado[9], 
        "resumo_estabelecimento": dado[10], "link_site_rede_social": dado[11], "imagem": dado[12]}
    return jsonify(json)


def inserir_loja(nome_loja, cep, rua, complemento, numero, bairro, horario_funcionamento, pontos_interesse, observacao="Sem Informação",
                resumo_estabelecimento="Sem Informação", link_site_rede_social="Sem Informação", imagem="Sem Informação"):
    """Insere uma Loja no banco de dados e confere se já existe com mysql."""

    # Insere a loja no banco de dados
    cursor.execute('INSERT INTO lojas (nome_loja, cep, rua, complemento, numero, observacao, bairro, \
        horario_funcionamento, pontos_interesse, resumo_estabelecimento, link_site_rede_social, imagem) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nome_loja, cep, rua, complemento, numero, \
        observacao, bairro, horario_funcionamento, pontos_interesse, resumo_estabelecimento, \
        link_site_rede_social, imagem))
    conectando.commit()

    # Retorna a mensagem de sucesso
    return {'mensagem': 'Loja cadastrada com sucesso'}, 201


@spec.validate(
    body=Request(LojasSchema)
)
def alterar_loja(request: Request, id: int):
    """Altera uma Pessoa no banco de dados."""
    body = request.body.dict()
    cursor.execute('UPDATE lojas SET nome_loja=%s, cep=%s, rua=%s, complemento=%s, numero=%s, observacao=%s, \
        bairro=%s, horario_funcionamento=%s, pontos_interesse=%s, resumo_estabelecimento=%s, \
        link_site_rede_social=%s, imagem=%s WHERE id=%s', (body['nome_loja'], body['cep'], body['rua'], \
        body['complemento'], body['numero'], body['observacao'], body['bairro'], body['horario_funcionamento'], \
        body['pontos_interesse'], body['resumo_estabelecimento'], body['link_site_rede_social'], \
        body['imagem'], id))
    conectando.commit()
    # Retorna a mensagem de sucesso
    return {'mensagem': f'Loja com id {id} alterada com sucesso'}, 200

@server.route('/lojas/excluir_loja', methods=['DELETE'])
def excluir_loja(id):
    """Remove uma loja do banco de dados."""
    cursor.execute('DELETE FROM lojas WHERE id = %s', (id,))
    conectando.commit()
    return "Loja removida com sucesso!"