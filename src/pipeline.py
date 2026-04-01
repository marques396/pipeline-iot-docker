import pandas as pd
from sqlalchemy import create_engine

# ============================================
# 🔌 CONEXÃO COM O BANCO (DOCKER)
# ============================================
engine = create_engine('postgresql://postgres:admin123@localhost:5432/postgres')

# ============================================
#  PIPELINE DE DADOS
# ============================================
def rodar_pipeline():
    print("\n Iniciando Pipeline de Dados IoT...\n")

    try:
        # ============================================
        #  1. LEITURA DO CSV
        # ============================================
        df = pd.read_csv('data/IOT-temp.csv')
        print(f"✅ Arquivo carregado: {len(df):,} registros")

        # ============================================
        #  2. LIMPEZA E PADRONIZAÇÃO
        # ============================================
        df = df.rename(columns={
            'room_id/id': 'device_id',
            'noted_date': 'datetime',
            'temp': 'temperature',
            'out/in': 'status'
        })

        # Converter data
        df['datetime'] = pd.to_datetime(df['datetime'], dayfirst=True)

        # ============================================
        #  3. REMOVER DUPLICADOS (OPCIONAL MAS BOM)
        # ============================================
        df = df.drop_duplicates()

        # ============================================
        #  4. ENVIO PARA O POSTGRESQL
        # ============================================
        print(" Enviando dados para o PostgreSQL...")

        df.to_sql(
            'temperature_readings',
            engine,
            if_exists='replace',
            index=False
        )

        print("✅ Dados enviados com sucesso!")

        # ============================================
        # 📊 5. RESUMO FINAL
        # ============================================
        print("\n RESUMO:")
        print(f"Total de registros: {len(df):,}")
        print(f"Colunas: {list(df.columns)}\n")

    except Exception as e:
        print(f" Erro no pipeline: {e}")

# ============================================
# ▶️ EXECUÇÃO
# ============================================
if __name__ == "__main__":
    rodar_pipeline()