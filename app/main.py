from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os
import glob

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

def carregar_gabaritos():
    gabaritos = {}
    pasta = "../gabaritos"
    if not os.path.exists(pasta):
        return gabaritos
    for arquivo in glob.glob(os.path.join(pasta, "*.csv")):
        nome = os.path.splitext(os.path.basename(arquivo))[0]
        df = pd.read_csv(arquivo)
        gabaritos[nome] = df
    return gabaritos

def carregar_escolas():
    escolas = set()
    pasta = "../data"
    if not os.path.exists(pasta):
        return []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".csv"):
            df = pd.read_csv(os.path.join(pasta, arquivo))
            if "Escola" in df.columns:
                escolas.update(df["Escola"].dropna().unique())
    return sorted(escolas)

def desempenho_por_questao(df_alunos, gabaritos, filtro_ano, filtro_comp):
    # Supondo que o nome do gabarito seja "5ºAno_Português" etc.
    chave_gab = f"{filtro_ano}_{filtro_comp}".replace(" ", "").replace("º", "º")
    gab = gabaritos.get(chave_gab)
    if gab is None or df_alunos.empty:
        return pd.DataFrame()
    questoes = gab['Questão'].tolist()
    respostas_gab = gab.set_index('Questão')['Resposta'].to_dict()
    acertos = {q: 0 for q in questoes}
    total = {q: 0 for q in questoes}
    for _, aluno in df_alunos.iterrows():
        for q in questoes:
            col = f"Questão_{q}"
            if col in aluno and pd.notna(aluno[col]):
                total[q] += 1
                if aluno[col] == respostas_gab[q]:
                    acertos[q] += 1
    dados = []
    for q in questoes:
        dados.append({
            "Questão": q,
            "Acertos": acertos[q],
            "Total": total[q],
            "Percentual": (acertos[q]/total[q]*100) if total[q] > 0 else 0
        })
    return pd.DataFrame(dados)

def carregar_opcoes(coluna):
    opcoes = set()
    pasta = "../data"
    if not os.path.exists(pasta):
        return []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".csv"):
            df = pd.read_csv(os.path.join(pasta, arquivo))
            if coluna in df.columns:
                opcoes.update(df[coluna].dropna().unique())
    return sorted(opcoes)

def extrair_filtros():
    escolas, series, turmas, componentes = set(), set(), set(), set()
    pasta = "../data"
    if not os.path.exists(pasta):
        return [], [], [], []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".csv"):
            df = pd.read_csv(os.path.join(pasta, arquivo))
            if "Escola" in df.columns:
                escolas.update(df["Escola"].dropna().unique())
            if "Ano/Série" in df.columns:
                series.update(df["Ano/Série"].dropna().unique())
            if "Turma" in df.columns:
                turmas.update(df["Turma"].dropna().unique())
            if "Componente" in df.columns:
                componentes.update(df["Componente"].dropna().unique())
    return sorted(escolas), sorted(series), sorted(turmas), sorted(componentes)

@app.route("/", methods=["GET"])
def index():
    escolas = carregar_opcoes("Escola")
    series = carregar_opcoes("Ano/Série")    if __name__ == "__main__":
        app.run(debug=True)  # Isso já usa 127.0.0.1:5000 por padrão
    turmas = carregar_opcoes("Turma")
    componentes = carregar_opcoes("Componente")

    df = carregar_dados()
    gabaritos = carregar_gabaritos()

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

    # Gera gráfico de desempenho real se houver filtro de série e componente
    if serie and componente and not df.empty:
        df_graf = desempenho_por_questao(df, gabaritos, serie, componente)
        if not df_graf.empty:
            fig = px.bar(df_graf, x="Questão", y="Percentual", text="Acertos",
                         title="Desempenho Real por Questão (%)",
                         labels={"Percentual": "% de Acertos"})
            fig.update_traces(texttemplate='%{text} acertos', textposition='outside')
            fig.update_layout(yaxis_range=[0, 100])
            graph_html = fig.to_html(full_html=False)
        else:
            graph_html = "<p>Nenhum dado/gabarito encontrado para este filtro.</p>"
    else:
        graph_html = "<p>Selecione uma série e componente para ver o desempenho real.</p>"

    return render_template(
        "index.html",
        graph=graph_html,
        escolas=escolas,
        series=series,
        turmas=turmas,
        componentes=componentes
    )

if __name__ == "__main__":
    app.run(debug=True)  # Isso já usa 127.0.0.1:5000 por padrão