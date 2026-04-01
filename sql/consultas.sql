import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Carrega as configurações do arquivo .env (Segurança)
load_dotenv()

def rodar_pipeline():
    print("\n🚀 Iniciando Pipeline de Dados IoT...")

    # Configurações do Banco de Dados (Docker)
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASS = os.getenv('DB_PASS', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5434')
    DB_NAME = os.getenv('DB_NAME', 'postgres')

    # Cria a conexão com o banco
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    try:
        # 2. Leitura do arquivo CSV
        # Certifique-se que o arquivo IOT-temp.csv está na pasta raiz do projeto
        caminho_csv = 'IOT-temp.csv'
        
        if not os.path.exists(caminho_csv):
            print(f"❌ Erro: O arquivo {caminho_csv} não foi encontrado!")
            return

        print(f"📖 Lendo arquivo {caminho_csv}...")
        df = pd.read_csv(caminho_csv)

        # 3. Limpeza e Tratamento de Dados
        # Ajustando nomes de colunas para o padrão do banco (minúsculas e sem espaços)
        df.columns = ['id', 'room_id', 'noted_date', 'temp', 'out_in']
        
        # Renomeando para ficar igual às suas VIEWS do SQL
        df = df.rename(columns={
            'noted_date': 'datetime',
            'temp': 'temperature',
            'out_in': 'status',
            'room_id': 'device_id'
        })

        # Convertendo a coluna de data para o formato correto do Python/SQL
        df['datetime'] = pd.to_datetime(df['datetime'], dayfirst=True)

        print(f"✅ Arquivo carregado: {len(df):,} registros")

        # 4. Envio para o PostgreSQL
        print("⏳ Enviando dados para o PostgreSQL (isso pode demorar alguns segundos)...")
        
        # O 'replace' recria a tabela. O 'index=False' não envia o número da linha.
        df.to_sql('temperature_readings', engine, if_exists='replace', index=False)

        print("✅ Dados enviados com sucesso!")

    except Exception as e:
        print(f"❌ Erro no pipeline: {e}")

    finally:
        # 5. Fechamento Seguro da Conexão
        engine.dispose()
        print("✅ Conexões liberadas com sucesso!")

    # 6. Resumo Final no Terminal
    print(f"\n📊 RESUMO DO PROCESSO:")
    print(f"Total de registros processados: {len(df):,}")
    print(f"Colunas finais: {list(df.columns)}")
    print("-" * 30)

if __name__ == "__main__":
    rodar_pipeline()