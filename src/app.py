import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# ==========================================
# 🔌 CONEXÃO COM BANCO (PADRÃO PROFESSOR)
# ==========================================
# Porta: 5432 | Usuário: postgres | Senha: admin123
engine = create_engine('postgresql://postgres:admin123@localhost:5432/postgres')

# ================================
#  CACHE (PERFORMANCE)
# ================================
@st.cache_data(ttl=60)
def load_data(view_name):
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)

# ================================
#    CONFIGURAÇÃO
# ================================
st.set_page_config(page_title="Dashboard IoT Osmar", layout="wide")

st.title(' Dashboard de Temperaturas IoT - Osmar')
st.markdown("###  Análise de Dados de Sensores IoT")
st.markdown("---")

try:
    # ================================
    #  CARREGAR DADOS
    # ================================
    df_status = load_data('media_por_status')
    df_leituras_hora = load_data('leituras_por_hora')
    df_temp_max_min = load_data('temp_max_min_por_dia')

    # ================================
    #   KPIs (TOPO)
    # ================================
    col1, col2, col3 = st.columns(3)

    with col1:
        # Coluna da View SQL: 'media_temperatura'
        st.metric(" Média Geral", f"{df_status['media_temperatura'].mean():.2f} °C")

    with col2:
        st.metric(" Total de Leituras", int(df_leituras_hora['contagem'].sum()))

    with col3:
        st.metric(" Dias Monitorados", df_temp_max_min['data'].nunique())

    st.markdown("---")

    # ================================
    #  FILTROS
    # ================================
    st.sidebar.header(" Filtros")

    status_options = df_status['status'].unique()

    selected_status = st.sidebar.multiselect(
        "Selecione o Ambiente",
        options=status_options,
        default=status_options
    )

    # Aplicar filtro
    df_status_filtrado = df_status[df_status['status'].isin(selected_status)]

    # ================================
    #   GRÁFICOS EM COLUNAS
    # ================================
    col1, col2 = st.columns(2)

    #  GRÁFICO 1: Barras
    with col1:
        st.subheader('🌡️ Média de Temperatura por Ambiente')

        fig1 = px.bar(
            df_status_filtrado,
            x='status',
            y='media_temperatura',
            color='status',
            text='media_temperatura',
            labels={
                'status': 'Ambiente',
                'media_temperatura': 'Média (°C)'
            }
        )

        fig1.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)

    #  GRÁFICO 2: Linhas (Horas)
    with col2:
        st.subheader(' Leituras por Hora do Dia')

        fig2 = px.line(
            df_leituras_hora.sort_values('hora'),
            x='hora',
            y='contagem',
            markers=True,
            labels={
                'hora': 'Hora',
                'contagem': 'Leituras'
            }
        )

        st.plotly_chart(fig2, use_container_width=True)

    # ================================
    #  GRÁFICO 3: Máximas e Mínimas
    # ================================
    st.subheader(' Temperaturas Máximas e Mínimas por Dia')

    fig3 = px.line(
        df_temp_max_min.sort_values('data'),
        x='data',
        y=['temp_max', 'temp_min'],
        markers=True,
        labels={
            'data': 'Data',
            'value': 'Temperatura (°C)'
        }
    )

    st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f" Erro de Conexão ou View: {e}")
    st.info("Verifique se o seu PostgreSQL na porta 5432 está ativo!")