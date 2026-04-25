import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# 2. Recupera a URL de conexão protegida
db_url = os.getenv("DATABASE_URL")

# ==========================================
# 🔌 CONEXÃO COM BANCO (PROTEGIDA)
# ==========================================
# Seguindo as boas práticas de segurança, a senha é carregada via .env
engine = create_engine(db_url)

@st.cache_data(ttl=60)
def load_data(view_name):
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)

# ================================
#     CONFIGURAÇÃO DA PÁGINA
# ================================
st.set_page_config(page_title="Dashboard IoT Osmar", layout="wide")

st.title(' Dashboard de Temperaturas IoT - Osmar')
st.markdown("### 📊 Análise de Dados de Sensores (Big Data)")
st.markdown("---")

try:
    # 1. CARREGAR DADOS
    df_status = load_data('media_por_status')
    df_leituras_hora = load_data('leituras_por_hora')
    df_temp_max_min = load_data('temp_max_min_por_dia')
    df_in_out = load_data('avg_temp_in_out_dia')
    df_avg_temp_disp = load_data('avg_temp_por_dispositivo') # Gráfico do seu amigo

    # ================================
    #   KPIs (TOPO)
    # ================================
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡️ Média Geral", f"{df_status['media_temperatura'].mean():.2f} °C")
    with col2:
        st.metric("🔢 Total de Leituras", f"{int(df_leituras_hora['contagem'].sum()):,}")
    with col3:
        st.metric("📅 Dias Monitorados", df_temp_max_min['data'].nunique())

    st.markdown("---")

    # ================================
    #   GRÁFICOS: LINHA 1
    # ================================
    c1, c2 = st.columns(2)

    with c1:
        st.subheader(' Média por Ambiente (In/Out)')
        fig1 = px.bar(df_status, x='status', y='media_temperatura', color='status', text_auto='.2f')
        st.plotly_chart(fig1, key="bar_status")

    with c2:
        st.subheader(' Leituras por Hora do Dia')
        fig2 = px.line(df_leituras_hora.sort_values('hora'), x='hora', y='contagem', markers=True)
        st.plotly_chart(fig2, key="line_hora")

    # ================================
    #   GRÁFICOS: LINHA 2 (O que veio do seu amigo)
    # ================================
    c3, c4 = st.columns(2)

    with c3:
        st.subheader(' Média de Temperatura por Dispositivo')
        fig_scatter = px.scatter(
            df_avg_temp_disp, 
            x='device_id', 
            y='avg_temp', 
            size='avg_temp', 
            color='device_id',
            labels={'device_id': 'ID', 'avg_temp': 'Média (°C)'}
        )
        st.plotly_chart(fig_scatter, key="scatter_disp")

    with c4:
        st.subheader('🏠 vs 🌳 Comparação Interna/Externa')
        df_in_out['out_in'] = df_in_out['out_in'].replace({'In': 'Interna', 'Out': 'Externa'})
        fig_in_out = px.line(df_in_out.sort_values('data'), x='data', y='avg_temp', color='out_in')
        st.plotly_chart(fig_in_out, key="line_in_out")

    # ================================
    #   LINHA 3: MÁXIMAS E MÍNIMAS
    # ================================
    st.markdown("---")
    st.subheader('📉 Histórico de Temperaturas Máximas e Mínimas')
    fig3 = px.line(df_temp_max_min.sort_values('data'), x='data', y=['temp_max', 'temp_min'], markers=True)
    st.plotly_chart(fig3, key="line_max_min")

except Exception as e:
    st.error(f"❌ Erro ao carregar Dashboard: {e}")
    st.info("Dica: Certifique-se de que o Pipeline rodou e criou as views no Docker.")