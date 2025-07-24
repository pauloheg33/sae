from flask import Flask, render_template, request
from models import db, AlunoResposta, Gabarito
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sae.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def importar_csvs():
    # Garante que as pastas existem
    if not os.path.exists("../data"):
        os.makedirs("../data")
    if not os.path.exists("../gabaritos"):
        os.makedirs("../gabaritos")
    if not os.path.exists('sae.db'):
        with app.app_context():
            db.create_all()
            # Importa respostas dos alunos
            for arquivo in os.listdir("../data"):
                if arquivo.endswith(".csv"):
                    df = pd.read_csv(os.path.join("../data", arquivo))
                    for _, row in df.iterrows():
                        for col in df.columns:
                            if col.startswith("Questão_"):
                                questao = col.replace("Questão_", "")
                                resposta = row[col]
                                db.session.add(AlunoResposta(
                                    escola=row.get("Escola"),
                                    serie=row.get("Ano/Série"),
                                    turma=row.get("Turma"),
                                    componente=row.get("Componente"),
                                    aluno=row.get("Aluno"),
                                    questao=questao,
                                    resposta=resposta
                                ))
            # Importa gabaritos
            for arquivo in os.listdir("../gabaritos"):
                if arquivo.endswith(".csv"):
                    df = pd.read_csv(os.path.join("../gabaritos", arquivo))
                    serie, componente = arquivo.replace(".csv", "").split("_")
                    for _, row in df.iterrows():
                        db.session.add(Gabarito(
                            serie=serie,
                            componente=componente,
                            questao=row["Questão"],
                            resposta_correta=row["Resposta"]
                        ))
            db.session.commit()

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

    series = [r[0] for r in db.session.query(AlunoResposta.serie).distinct() if r[0]]
    turmas = [r[0] for r in db.session.query(AlunoResposta.turma).distinct() if r[0]]
    componentes = [r[0] for r in db.session.query(AlunoResposta.componente).distinct() if r[0]]

    # Query filtrada
    query = AlunoResposta.query
    if escola: query = query.filter_by(escola=escola)
    if serie: query = query.filter_by(serie=serie)
    if turma: query = query.filter_by(turma=turma)
    if componente: query = query.filter_by(componente=componente)
    respostas = query.all()

    # Exemplo: gráfico vazio para evitar erro
    graph_html = "<p>Selecione filtros para visualizar o gráfico.</p>"

    return render_template(
        "index.html",
        escolas=escolas,
        series=series,
        turmas=turmas,
        componentes=componentes,
        graph=graph_html
    )

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)