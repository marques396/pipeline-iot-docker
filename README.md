# 🌡️ Dashboard de Temperaturas IoT - Big Data

Este projeto consiste em um pipeline de dados automatizado que processa informações de sensores de temperatura (IoT). O fluxo vai desde a leitura de arquivos brutos via **Python/Pandas** até o armazenamento em **PostgreSQL** (Docker) e visualização em um Dashboard dinâmico.

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x (Pandas para ETL)
* **Banco de Dados:** PostgreSQL (Containerizado via Docker)
* **Visualização:** Streamlit & Plotly Express (Gráficos Interativos)
* **Conectividade:** SQLAlchemy & Psycopg2
* **Gestão de Banco:** DBeaver (Auditoria e Validação)

## 📂 Estrutura do Projeto
* `src/pipeline.py`: Script de ETL que limpa o CSV, gerencia o banco e cria as Views SQL.
* `src/app.py`: Interface do Dashboard com KPIs e análise visual.
* `requirements.txt`: Lista de dependências para execução do ambiente.
* `Relatorio_Tecnico.pdf`: Documentação teórica e insights do projeto.

##  Análises e Views SQL (Otimização de Big Data)
O pipeline automatiza a criação de 5 visões estratégicas diretamente no banco de dados:
1. **media_por_status**: Comparação térmica entre ambientes Internos e Externos.
2. **temp_max_min_por_dia**: Monitoramento de extremos térmicos diários.
3. **leituras_por_hora**: Auditoria de tráfego e constância dos sensores.
4. **avg_temp_in_out_dia**: Evolução temporal comparativa.
5. **avg_temp_por_dispositivo**: Distribuição térmica por ID de sensor.

> **🚀 Performance:** Processamento eficiente de **97.605 registros** com camada de visão (Views) para consultas de baixa latência.

---

##  Como Rodar o Projeto
1. **Banco de Dados:** Certifique-se de que o PostgreSQL está rodando no Docker (Porta 5432) com as credenciais configuradas nos scripts.
2. **Dependências:** `pip install -r requirements.txt`
3. **Processar Dados:** Execute `python src/pipeline.py` para popular o banco e criar as views.
4. **Visualizar:** `streamlit run src/app.py` para abrir o Dashboard no navegador.