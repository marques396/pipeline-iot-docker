#  Dashboard de Temperaturas IoT - Big Data

Este projeto consiste em um pipeline de dados que lê informações de sensores de temperatura (IoT), processa-os via **Python** e os armazena em um banco de dados **PostgreSQL** para visualização em um Dashboard interativo.

---

##  Tecnologias Utilizadas
* **Linguagem:** Python (Pandas para ETL)
* **Banco de Dados:** PostgreSQL (Dockerizado)
* **Visualização:** Streamlit & Plotly
* **Conectividade:** SQLAlchemy

##  Estrutura do Projeto
* `src/pipeline.py`: Script responsável por ler o CSV e carregar no banco.
* `src/app.py`: Interface do Dashboard em Streamlit.
* `data/`: Contém o dataset `IOT-temp.csv`.
* `sql/`: Scripts de criação das Views (`consultas.sql`).

##  Views SQL e Insights
1. **media_por_status**: Compara o clima entre ambientes Internos e Externos.
2. **temp_max_min_por_dia**: Identifica extremos térmicos diários.
3. **leituras_por_hora**: Monitora a frequência de envio dos sensores.

> **Insight Principal:** O sistema processou com sucesso mais de **97 mil registros**, mantendo a performance e gerando métricas precisas sobre a constância térmica (média de 33°C).

---

##  Como Rodar o Projeto
1. Certifique-se de que o **PostgreSQL** está rodando (via Docker ou local).
2. Instale as dependências: `pip install -r requirements.txt` (se houver).
3. Execute o pipeline: `python src/pipeline.py`
4. Inicie o dashboard: `streamlit run src/app.py`