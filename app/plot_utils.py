import plotly.graph_objs as go
import plotly.io as pio
from models import AlunoResposta, Gabarito
from markupsafe import Markup

def gerar_grafico_desempenho(respostas, serie=None, componente=None):
    if not respostas:
        return "<p>Nenhum dado disponível para o filtro selecionado.</p>"
    # Filtrar gabarito
    questoes = sorted(list(set(r.questao for r in respostas)))
    if serie and componente:
        gabaritos = {g.questao: g.resposta_correta for g in Gabarito.query.filter_by(serie=serie, componente=componente).all()}
    else:
        gabaritos = {g.questao: g.resposta_correta for g in Gabarito.query.all()}
    acertos = {q: 0 for q in questoes}
    total = {q: 0 for q in questoes}
    for r in respostas:
        if r.questao in gabaritos:
            total[r.questao] += 1
            if r.resposta == gabaritos[r.questao]:
                acertos[r.questao] += 1
    questoes_labels = [str(q) for q in questoes]
    percentuais = [100 * acertos[q] / total[q] if total[q] > 0 else 0 for q in questoes]
    fig = go.Figure([
        go.Bar(x=questoes_labels, y=percentuais, marker_color='#1976d2')
    ])
    fig.update_layout(
        title="Percentual de Acertos por Questão",
        xaxis_title="Questão",
        yaxis_title="% de Acertos",
        yaxis=dict(range=[0, 100]),
        plot_bgcolor="#f8fafc",
        paper_bgcolor="#f8fafc"
    )
    graph_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    return Markup(graph_html)

def gerar_grafico_placeholder():
    return "<p>Selecione filtros para visualizar o gráfico.</p>"

def gerar_grafico_por_turma(respostas):
    if not respostas:
        return "<p>Nenhum dado disponível para o filtro selecionado.</p>"
    # Agrupar por turma
    turma_acertos = {}
    turma_total = {}
    for r in respostas:
        turma = r.turma or 'N/A'
        if turma not in turma_acertos:
            turma_acertos[turma] = 0
            turma_total[turma] = 0
        # Buscar gabarito
        gabarito = Gabarito.query.filter_by(serie=r.serie, componente=r.componente, questao=r.questao).first()
        if gabarito and r.resposta == gabarito.resposta_correta:
            turma_acertos[turma] += 1
        turma_total[turma] += 1
    turmas = sorted(turma_acertos.keys())
    percentuais = [100 * turma_acertos[t] / turma_total[t] if turma_total[t] > 0 else 0 for t in turmas]
    fig = go.Figure([
        go.Bar(x=turmas, y=percentuais, marker_color='#42a5f5')
    ])
    fig.update_layout(
        title="Percentual Médio de Acertos por Turma",
        xaxis_title="Turma",
        yaxis_title="% de Acertos",
        yaxis=dict(range=[0, 100]),
        plot_bgcolor="#f8fafc",
        paper_bgcolor="#f8fafc"
    )
    graph_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    return Markup(graph_html)

def gerar_grafico_por_escola(respostas):
    if not respostas:
        return "<p>Nenhum dado disponível para o filtro selecionado.</p>"
    escola_acertos = {}
    escola_total = {}
    for r in respostas:
        escola = r.escola or 'N/A'
        if escola not in escola_acertos:
            escola_acertos[escola] = 0
            escola_total[escola] = 0
        gabarito = Gabarito.query.filter_by(serie=r.serie, componente=r.componente, questao=r.questao).first()
        if gabarito and r.resposta == gabarito.resposta_correta:
            escola_acertos[escola] += 1
        escola_total[escola] += 1
    escolas = sorted(escola_acertos.keys())
    percentuais = [100 * escola_acertos[e] / escola_total[e] if escola_total[e] > 0 else 0 for e in escolas]
    fig = go.Figure([
        go.Bar(x=escolas, y=percentuais, marker_color='#7e57c2')
    ])
    fig.update_layout(
        title="Percentual Médio de Acertos por Escola",
        xaxis_title="Escola",
        yaxis_title="% de Acertos",
        yaxis=dict(range=[0, 100]),
        plot_bgcolor="#f8fafc",
        paper_bgcolor="#f8fafc"
    )
    graph_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    return Markup(graph_html)
