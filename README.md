#  Dashboard de Temperaturas IoT - Big Data

Este projeto consiste em um pipeline de dados automatizado que processa informações de sensores de temperatura (IoT). O fluxo vai desde a leitura de arquivos brutos via **Python/Pandas** até o armazenamento em **PostgreSQL** (Docker) e visualização em um Dashboard dinâmico.

## 📊 Base de Dados
O conjunto de dados utilizado neste projeto é o **"Temperature Readings: IoT Devices"**, disponível publicamente no Kaggle.
* **Link:** [Kaggle - IoT Temperature Readings](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices)
* **Volumetria:** 97.605 registros de sensores de temperatura (ambientes internos e externos).


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


##  Análises e Views SQL (Otimização de Big Data)
O pipeline automatiza a criação de 5 visões estratégicas diretamente no banco de dados:
1. **media_por_status**: Comparação térmica entre ambientes Internos e Externos.
2. **temp_max_min_por_dia**: Monitoramento de extremos térmicos diários.
3. **leituras_por_hora**: Auditoria de tráfego e constância dos sensores.
4. **avg_temp_in_out_dia**: Evolução temporal comparativa.
5. **avg_temp_por_dispositivo**: Distribuição térmica por ID de sensor.

> ** Performance:** Processamento eficiente de **97.605 registros** com camada de visão (Views) para consultas de baixa latência.

---


## Como Rodar o Projeto
Siga os passos abaixo para configurar o ambiente e visualizar os dados:

1. ## Configuração do Banco de Dados (Docker)
Com o Docker Desktop aberto, execute o comando abaixo no terminal para subir o container do PostgreSQL com a senha configurada:

`docker run --name postgres-db -e POSTGRES_PASSWORD=suasenhaaqui -p 5432:5432 -d postgres`


2. ## Instalação de Dependências
No terminal, dentro da pasta do projeto (e com seu ambiente virtual ativo), instale as bibliotecas necessárias:


`pip install -r requirements.txt`


3. ## Processar Dados (Pipeline ETL)
Execute o script principal para realizar a limpeza dos dados, carga no banco e criação automática das Views SQL:

`python src/pipeline.py`

4. ## Visualizar Dashboard
Inicie a interface gráfica do Streamlit para abrir o Dashboard interativo no seu navegador:


 `python -m streamlit run src/app.py`