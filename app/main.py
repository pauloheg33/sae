from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models import db, AlunoResposta, Gabarito
import pandas as pd
import os
from import_utils import importar_csvs
from plot_utils import gerar_grafico_desempenho, gerar_grafico_placeholder, gerar_grafico_por_turma, gerar_grafico_por_escola

# Testes automatizados
import pytest

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sae.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

UPLOAD_FOLDER = "../data"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "supersecretkey"  # Para flash messages


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Nenhum arquivo selecionado!")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("Nenhum arquivo selecionado!")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("Arquivo enviado com sucesso!")
            return redirect(url_for("index"))
        else:
            flash("Tipo de arquivo não permitido!")
            return redirect(request.url)
    return render_template("upload.html")


def detectar_escolas_por_arquivo():
    pasta = "../data"
    escolas = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".csv"):
            nome_escola = os.path.splitext(arquivo)[0]
            escolas.append(nome_escola)
    return sorted(escolas)


def detectar_escolas_por_coluna():
    pasta = "../data"
    escolas = set()
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".csv"):
            df = pd.read_csv(os.path.join(pasta, arquivo))
            for col in df.columns:
                if any(x in col.lower() for x in ["escola", "unidade", "instituicao"]):
                    escolas.update(df[col].dropna().unique())
    return sorted(escolas)


def detectar_escolas():
    escolas = set(detectar_escolas_por_arquivo())
    escolas.update(detectar_escolas_por_coluna())
    return sorted(escolas)


@app.route("/", methods=["GET"])
def index():
    escolas = detectar_escolas()

    escola = request.args.get("escola")
    serie = request.args.get("serie")
    turma = request.args.get("turma")
    componente = request.args.get("componente")
    tipo_grafico = request.args.get("tipo_grafico", "questao")

    series = [r[0] for r in db.session.query(AlunoResposta.serie).distinct() if r[0]]
    turmas = [r[0] for r in db.session.query(AlunoResposta.turma).distinct() if r[0]]
    componentes = [r[0] for r in db.session.query(AlunoResposta.componente).distinct() if r[0]]

    # Query filtrada
    query = AlunoResposta.query
    if escola:
        query = query.filter_by(escola=escola)
    if serie:
        query = query.filter_by(serie=serie)
    if turma:
        query = query.filter_by(turma=turma)
    if componente:
        query = query.filter_by(componente=componente)
    respostas = query.all()

    # Seleção do tipo de gráfico
    if tipo_grafico == "turma":
        graph_html = gerar_grafico_por_turma(respostas)
    elif tipo_grafico == "escola":
        graph_html = gerar_grafico_por_escola(respostas)
    else:
        graph_html = gerar_grafico_desempenho(respostas, serie=serie, componente=componente)

    return render_template(
        "index.html",
        escolas=escolas,
        series=series,
        turmas=turmas,
        componentes=componentes,
        graph=graph_html,
        tipo_grafico=tipo_grafico
    )


with app.app_context():
    db.create_all()


# Testes automatizados
def test_index_route():
    app.testing = True
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"SAE" in response.data


if __name__ == "__main__":
    app.run(debug=True)
