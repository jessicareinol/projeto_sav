from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import url_for


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testeuser:toledo22@localhost:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    user = db.Column('usu_user', db.String(256))
    senha = db.Column('usu_senha', db.String(256))
    end = db.Column('usu_end', db.String(256))
    num = db.Column('usu_num', db.String(256))
    complemento = db.Column('usu_complemento', db.String(256))
    tel = db.Column('usu_tel', db.String(256))


    def __init__(self, nome, email, user, senha, end, num, complemento, tel):
        self.nome = nome
        self.email = email
        self.user = user
        self.senha = senha
        self.end = end
        self.num = num
        self.complemento = complemento
        self.tel = tel

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__ (self, nome, desc):
        self.nome = nome
        self.desc = desc

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id


class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column('perg_id', db.Integer, primary_key=True)
    conteudo = db.Column('perg_conteudo', db.String(512))
    data = db.Column('perg_data', db.DateTime, default=db.func.current_timestamp())
    anu_id = db.Column('anu_id', db.Integer, db.ForeignKey("anuncio.anu_id"))
    usu_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, conteudo, anu_id, usu_id):
        self.conteudo = conteudo
        self.anu_id = anu_id
        self.usu_id = usu_id


class Resposta(db.Model):
    __tablename__ = "resposta"
    id = db.Column('resp_id', db.Integer, primary_key=True)
    conteudo = db.Column('resp_conteudo', db.String(512))
    data = db.Column('resp_data', db.DateTime, default=db.func.current_timestamp())
    perg_id = db.Column('perg_id', db.Integer, db.ForeignKey("pergunta.perg_id"))

    def __init__(self, conteudo, perg_id):
        self.conteudo = conteudo
        self.perg_id = perg_id


@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('paginanaoencontrada.html')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cad/usuario")
def usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all (), titulo="Usuário")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    usuario = Usuario(request.form.get('nome'),
                      request.form.get('email'),
                      request.form.get('user'),
                      request.form.get('senha'),
                      request.form.get('end'),
                      request.form.get('num'),
                      request.form.get('complemento'),
                      request.form.get('tel')
                      )
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        return usuario.nome
    else:
        return "Usuário não encontrado", 404
    
@app.route("/usuario/editar/<int:id>", methods=['GET', 'POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email'),
        usuario.user = request.form.get('user'),
        usuario.senha = request.form.get('senha'),
        usuario.end = request.form.get('end'),
        usuario.num = request.form.get('num'),
        usuario.complemento = request.form.get('complemento'),
        usuario.tel = request.form.get('tel')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))
    
    return render_template('editarusuario.html', usuario = usuario, titulo="Usuario")   

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/cad/anuncio")
def anuncio():
    return render_template('anuncio.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncio/criar", methods=['POST'])
def criaranuncio():
    anuncio = Anuncio(request.form.get('nome'),
                      request.form.get('desc'),
                      request.form.get('qtd'),
                      request.form.get('preco'),
                      request.form.get('cat'),
                      request.form.get('usu'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/anuncio/editar/<int:id>", methods=['GET', 'POST'])
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.nome = request.form.get('nome')
        anuncio.desc = request.form.get('desc')
        anuncio.qtd = request.form.get('qtd')
        anuncio.preco = request.form.get('preco')
        anuncio.cat_id = request.form.get('cat')
        anuncio.usu_id = request.form.get('usu')
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncio'))

    return render_template('editaranuncio.html', anuncio=anuncio, categorias=Categoria.query.all(), usuarios=Usuario.query.all(), titulo="Editar Anúncio")

@app.route("/anuncio/deletar/<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/perguntas")
def listar_perguntas():
    perguntas = Pergunta.query.all()
    return render_template('listar_perguntas.html', perguntas=perguntas, titulo="Perguntas")

@app.route("/respostas")
def listar_respostas():
    respostas = Resposta.query.all()
    return render_template('listar_respostas.html', respostas=respostas, titulo="Respostas")


@app.route("/anuncios/compra")
def compra():
    print("anúncio comprado")
    return ""

@app.route("/anuncio/favoritos")
def favoritos():
    print("favorito inserido")
    return f"<h4>Favorito adicionado com sucesso!</h4>"

@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/categoria/editar/<int:id>", methods=['GET', 'POST'])
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome = request.form.get('nome')
        categoria.desc = request.form.get('desc')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))

    return render_template('editarcategoria.html', categoria=categoria, titulo="Editar Categoria")


@app.route("/categoria/deletar/<int:id>")
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))


@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relVendas.html', titulo="Relatório de Vendas")

@app.route("/relatorios/compras")
def relCompras():
    return render_template('relCompras.html', titulo="Relatório de Compras")

if __name__ == 'sav':
    with app.app_context():
        db.create_all()