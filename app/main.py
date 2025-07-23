from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

def carregar_dados():
    dados = []
    pasta = "../data"
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".csv"):
            df = pd.read_csv(os.path.join(pasta, arquivo))
            dados.append(df)
    if dados:
        return pd.concat(dados, ignore_index=True)
    return pd.DataFrame()

@app.route("/", methods=["GET"])
def index():
    df = carregar_dados()

    escola = request.args.get("escola")
    serie = request.args.get("serie")
    turma = request.args.get("turma")
    componente = request.args.get("componente")

    if escola:
        df = df[df["Escola"] == escola]
    if serie:
        df = df[df["Ano/Série"] == serie]
    if turma:
        df = df[df["Turma"] == turma]
    if componente:
        df = df[df["Componente"] == componente]

    if not df.empty:
        fig = px.bar(df, x="Questão", y="Acertos", title="Desempenho por Questão")
        graph_html = fig.to_html(full_html=False)
        escolas = df["Escola"].unique()
    else:
        graph_html = "<p>Nenhum dado encontrado.</p>"
        escolas = []

    return render_template("index.html", graph=graph_html, escolas=escolas)

if __name__ == "__main__":
    app.run(debug=True)