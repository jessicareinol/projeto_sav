from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cad/usuario")
def usuario():
    return render_template('usuario.html', titulo="Cadastro de Usuario")

@app.route("/cad/caduser", methods=['POST'])
def caduser():
    return request.form

@app.route("/cad/anuncio")
def anuncio():
    return render_template('anuncio.html', titulo="Cadastro de Anúncio")

@app.route("/anuncios/pergunta")
def pergunta():
    return render_template('pergunta.html', titulo="Pergunta")

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
    return render_template('categoria.html', titulo="Categorias")

@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relVendas.html', titulo="Relatório de Vendas")

@app.route("/relatorios/compras")
def relCompras():
    return render_template('relCompras.html', titulo="Relatório de Compras")