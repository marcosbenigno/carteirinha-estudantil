from flask import Flask, render_template, request, url_for, redirect, Response, make_response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#classes dos objetos do banco
class Aluno(db.Model):
    cpf = db.Column(db.String(11), primary_key=True, unique=True)
    password = db.Column(db.String(12))
    def __init__(self, cpf, password):
        self.cpf = cpf
        self.password = password
    def __repr__(self):
        return '<Aluno %r>' % self.cpf

class Dados(db.Model):
    cpf = db.Column(db.String(11), primary_key=True, unique=True)
    curso = db.Column(db.String(3))
    dre = db.Column(db.String(9))
    nasc = db.Column(db.String(8))
    nome = db.Column(db.String(80))
    foto = db.Column(db.String(40))
    ativo = db.Column(db.String(1))
    def __init__(self, cpf, curso, dre, nasc, nome, foto, ativo):
        self.cpf = cpf
        self.curso = curso
        self.dre = dre
        self.nasc = nasc
        self.nome = nome
        self.foto = foto
        self.ativo = ativo
    def __repr__(self):
        return '<Dados %r>' % self.cpf
    



#login válido cpf='11111111111' e password='2222'




@app.route('/')
def login():
    return render_template('login.html')

@app.route('/carteirinha/')
def carteirinha():
    return render_template('carteirinha.html')

@app.route('/auth/', methods=['POST'])
def auth():
    messageLogin = request.get_data().decode('utf-8')
    user_form = messageLogin.split()[2]
    password_form = messageLogin.split()[4]
    usuario = Aluno.query.filter_by(cpf=user_form).first()
    return make_response(verificacao(user_form, password_form))
    
def verificacao(cpf_form, senha_form):
    usuario = Aluno.query.filter_by(cpf=cpf_form).first()
    dados = Dados.query.filter_by(cpf=cpf_form).first()
    if usuario:
        if senha_form == usuario.password:
            if dados.ativo == "0":
                return "4   DRE INATIVO\n"
            elif not(dados.foto):
                return "5 FOTO INEXISTE\n"
            return geraMsg(cpf_form)
        else:
            return "2 SENHA INCORRE\n"
    elif cpf_form == "PASS":
        return "1 ID NECESSARIA\n"
    elif not(usuario):
        return "3 CPF NAO EXISTE\n"
    

def geraMsg(cpf_form):
    dados = Dados.query.filter_by(cpf=cpf_form).first()
    msg = "STATUS        0\nCURSO       " +dados.curso+"\nDRE   "+dados.dre+"\nNASC   "+dados.nasc+"\nTAMANHO      XX\nNOME "+dados.nome+"\nFOTO "+dados.foto+"\n"
    return msg

if __name__ == '__main__':
    app.run()