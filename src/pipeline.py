import pandas as pd
from sqlalchemy import create_engine, text

# ============================================
# 🔌 CONEXÃO COM O BANCO (DOCKER) 
# ============================================
engine = create_engine('postgresql://postgres:admin123@localhost:5432/postgres')

def rodar_pipeline():
    print("\n Iniciando Pipeline de Dados IoT Turbinado...\n")

    try:
        # 1. LEITURA DO CSV
        df = pd.read_csv('data/IOT-temp.csv')
        print(f"✅ [1/5] Arquivo carregado: {len(df):,} registros")

        # 2. LIMPEZA E PADRONIZAÇÃO
        df = df.rename(columns={
            'room_id/id': 'device_id',
            'noted_date': 'datetime',
            'temp': 'temperature',
            'out/in': 'status'
        })
        df['datetime'] = pd.to_datetime(df['datetime'], dayfirst=True)
        df = df.drop_duplicates()
        print("✅ [2/5] Dados limpos e duplicados removidos")

        # 3. LIMPEZA DE VIEWS ANTIGAS 
        print(" [3/5] Limpando Views antigas no PostgreSQL...")
        with engine.connect() as conn:
            views = [
                'media_por_status', 'leituras_por_hora', 
                'temp_max_min_por_dia', 'avg_temp_in_out_dia',
                'avg_temp_por_dispositivo'
            ]
            for view in views:
                conn.execute(text(f"DROP VIEW IF EXISTS {view} CASCADE;"))
            conn.commit()

        # 4. ENVIO PARA O POSTGRESQL
        print("📤 [4/5] Enviando dados para a tabela 'temperature_readings'...")
        df.to_sql('temperature_readings', engine, if_exists='replace', index=False)

        # 5. CRIAÇÃO DAS NOVAS VIEWS (A "Mágica" do Dashboard)
        print("🛠️ [5/5] Criando novas Views para análise...")
        with engine.connect() as conn:
            # View 1: Média por Status (In/Out)
            conn.execute(text("""
                CREATE OR REPLACE VIEW media_por_status AS
                SELECT status, AVG(temperature) as media_temperatura
                FROM temperature_readings GROUP BY status;
            """))

            # View 2: Leituras por Hora
            conn.execute(text("""
                CREATE OR REPLACE VIEW leituras_por_hora AS
                SELECT EXTRACT(HOUR FROM datetime) as hora, COUNT(*) as contagem
                FROM temperature_readings GROUP BY hora ORDER BY hora;
            """))

            # View 3: Máxima e Mínima por Dia
            conn.execute(text("""
                CREATE OR REPLACE VIEW temp_max_min_por_dia AS
                SELECT DATE(datetime) as data, MAX(temperature) as temp_max, MIN(temperature) as temp_min
                FROM temperature_readings GROUP BY DATE(datetime) ORDER BY data;
            """))

            # View 4: Comparação In/Out por Dia (Nova!)
            conn.execute(text("""
                CREATE OR REPLACE VIEW avg_temp_in_out_dia AS
                SELECT DATE(datetime) AS data, status as out_in, AVG(temperature) AS avg_temp
                FROM temperature_readings GROUP BY DATE(datetime), status ORDER BY data;
            """))

            # View 5: Média por Dispositivo (Para o Gráfico de Scatter)
            conn.execute(text("""
                CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
                SELECT device_id, AVG(temperature) as avg_temp
                FROM temperature_readings GROUP BY device_id;
            """))
            
            conn.commit()

        print("\n✅ PIPELINE FINALIZADO COM SUCESSO! ")
        print(f"Total de registros processados: {len(df):,}")

    except Exception as e:
        print(f" Erro no pipeline: {e}")

if __name__ == "__main__":
    rodar_pipeline()