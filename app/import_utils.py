import os
import pandas as pd
from models import db, AlunoResposta, Gabarito
from flask import current_app as app


def importar_csvs():
    # Garante que as pastas existem
    if not os.path.exists("../data"):
        os.makedirs("../data")
    if not os.path.exists("../gabaritos"):
        os.makedirs("../gabaritos")
    if not os.path.exists("sae.db"):
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
                                db.session.add(
                                    AlunoResposta(
                                        escola=row.get("Escola"),
                                        serie=row.get("Ano/Série"),
                                        turma=row.get("Turma"),
                                        componente=row.get("Componente"),
                                        aluno=row.get("Aluno"),
                                        questao=questao,
                                        resposta=resposta,
                                    )
                                )
            # Importa gabaritos
            for arquivo in os.listdir("../gabaritos"):
                if arquivo.endswith(".csv"):
                    df = pd.read_csv(os.path.join("../gabaritos", arquivo))
                    serie, componente = arquivo.replace(".csv", "").split("_")
                    for _, row in df.iterrows():
                        db.session.add(
                            Gabarito(
                                serie=serie,
                                componente=componente,
                                questao=row["Questão"],
                                resposta_correta=row["Resposta"],
                            )
                        )
            db.session.commit()
