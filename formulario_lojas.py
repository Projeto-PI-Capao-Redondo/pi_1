from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

def remover_hifen_cep(cep_com_hifen):
    return cep_com_hifen.replace('-', '')

class LojasForm(FlaskForm):
    nome_loja = StringField('Nome da Loja', validators=[DataRequired(), Length(max=100)])
    cep = StringField('CEP', validators=[DataRequired(), Length(max=9), Regexp(r'^\d{5}-\d{3}$', message='CEP inválido')])
    rua = StringField('Rua', validators=[DataRequired(), Length(max=100)])
    complemento = StringField('Complemento', validators=[Length(max=75)])
    numero = IntegerField('Número', validators=[DataRequired()])
    observacao = TextAreaField('Observação', validators=[Length(max=250)])
    bairro = StringField('Bairro', validators=[DataRequired(), Length(max=100)])
    horario_funcionamento = StringField('Horário de Funcionamento', validators=[DataRequired(), Length(max=150)])
    pontos_interesse = StringField('Pontos de Interesse', validators=[DataRequired(), Length(max=250)])
    resumo_estabelecimento = TextAreaField('Resumo do Estabelecimento', validators=[Length(max=500)])
    link_site_rede_social = StringField('Link do Site ou Rede Social', validators=[Length(max=150)])
    imagem = StringField('URL da Imagem', validators=[Length(max=150)])
    
    def validate_cep(form, field):
        cep_sem_hifen = remover_hifen_cep(field.data)
        if not cep_sem_hifen.isdigit() or len(cep_sem_hifen) != 8:
            raise ValidationError('CEP inválido')