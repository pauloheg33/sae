from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AlunoResposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    escola = db.Column(db.String(128))
    serie = db.Column(db.String(32))
    turma = db.Column(db.String(32))
    componente = db.Column(db.String(32))
    aluno = db.Column(db.String(128))
    questao = db.Column(db.String(16))
    resposta = db.Column(db.String(8))

class Gabarito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serie = db.Column(db.String(32))
    componente = db.Column(db.String(32))
    questao = db.Column(db.String(16))
    resposta_correta = db.Column(db.String(8))