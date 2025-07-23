# SAE - Sistema de Análise Educacional

## 💡 Objetivo do Projeto
O projeto SAE tem como objetivo criar um site/dashboard interativo para visualizar o desempenho das escolas com base em arquivos CSV. O sistema permitirá a análise de dados educacionais, exibindo gráficos de desempenho por questão e possibilitando a filtragem por escola, ano/série, turma e componente (Português, Matemática).

## 📁 Estrutura do Projeto
```
sae/
├── data/                # CSVs reunidos
├── app/                 # Código da aplicação
│   ├── static/          # CSS, JS, ícones
│   ├── templates/       # HTML com Jinja2
│   └── main.py          # Código backend (Flask)
├── requirements.txt     # Dependências do projeto
├── README.md            # Instruções do projeto
└── .gitignore           # Arquivos a serem ignorados pelo Git
```

## 📦 Dependências
As dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalar as dependências, execute o seguinte comando:

```
pip install -r requirements.txt
```

## 🚀 Como Executar o Projeto
1. **Clone o repositório:**
   ```
   git clone https://github.com/pauloheg33/sae.git
   cd sae
   ```

2. **Instale as dependências:**
   ```
   pip install -r requirements.txt
   ```

3. **Coloque os arquivos CSV na pasta `data/`.**

4. **Execute a aplicação:**
   ```
   python app/main.py
   ```

5. **Acesse o dashboard no navegador:**
   ```
   http://127.0.0.1:5000/
   ```

## 📊 Funcionalidades
- Carregamento de dados a partir de arquivos CSV.
- Filtragem de dados por escola, ano/série, turma e componente.
- Geração de gráficos de desempenho por questão.
- Exibição de tabelas com médias por turma e por escola.

## 📄 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📜 Licença
Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

# SAE Dashboard

Dashboard interativo para análise de desempenho escolar a partir de arquivos CSV.

## Como rodar

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
python main.py
```
Acesse: http://localhost:5000
