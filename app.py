"""
API em Flask com Pydantic e Flask-Pydantic-Spec


passo a passo:
1 - pip install flask
2 - pip install flask_pydantic_spec
3 - pip install pydantic

"""

from conect_mysql import conecta_mysql
from flask import Flask, request, jsonify, render_template
from flask_pydantic_spec import FlaskPydanticSpec, Request
from pydantic import BaseModel

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
spec = FlaskPydanticSpec('Flask', title='Explicação API - Projeto PI 1')
spec.register(server)


@server.get('/')
def index():
    return render_template('index.html')



@server.get('/lojas')  # Rota, endpoint, recurso ...
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



@server.post('/lojas')
@spec.validate(
    body=Request(LojasSchema)
)
def inserir_loja():
    """Insere uma Pessoa no banco de dados."""
    body = request.context.body.dict()
    cursor.execute('INSERT INTO lojas (id, nome_loja, cep, rua, complemento, numero, observacao, bairro, \
        horario_funcionamento, pontos_interesse, resumo_estabelecimento, link_site_rede_social, imagem) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (body['id'], body['nome_loja'], body['cep'], \
        body['rua'], body['complemento'], body['numero'], body['observacao'], body['bairro'], \
        body['horario_funcionamento'], body['pontos_interesse'], body['resumo_estabelecimento'], \
        body['link_site_rede_social'], body['imagem']))
    conectando.commit()


@server.put('/pessoas/<int:id>')
@spec.validate(
    body=Request(LojasSchema)
)
def alterar_loja(id):
    """Altera uma Pessoa no banco de dados."""
    body = request.context.body.dict()
    cursor.execute('UPDATE lojas SET nome_loja = %s, cep = %s, rua = %s, complemento = %s, numero = %s, \
        observacao = %s, bairro = %s, horario_funcionamento = %s, pontos_interesse = %s, resumo_estabelecimento = %s, \
        link_site_rede_social = %s, imagem = %s WHERE id = %s', (body['nome_loja'], body['cep'], body['rua'], \
        body['complemento'], body['numero'], body['observacao'], body['bairro'], \
        body['horario_funcionamento'], body['pontos_interesse'], body['resumo_estabelecimento'], \
        body['link_site_rede_social'], body['imagem'], id))
    conectando.commit()
    return "Loja alterada com sucesso!"

@server.delete('/pessoas/<int:id>')
def deletar_loja(id):
    """Remove uma Pessoa do banco de dados."""
    cursor.execute('DELETE FROM lojas WHERE id = %s', (id,))
    conectando.commit()
    return "Loja removida com sucesso!"


if __name__ == '__main__':
    server.run(debug=True)
