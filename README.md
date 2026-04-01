#  Dashboard de Temperaturas IoT - Big Data

Este projeto consiste em um pipeline de dados que lê informações de sensores de temperatura (IoT), processa-os via Python e os armazena em um banco de dados PostgreSQL para visualização em um Dashboard interativo.

##  Tecnologias Utilizadas
- **Python**: Processamento e Pipeline (Pandas).
- **PostgreSQL**: Banco de Dados Relacional.
- **SQLAlchemy**: Conexão e persistência de dados.
- **Streamlit & Plotly**: Dashboard interativo e gráficos.

## Views SQL e Propósitos
1. **media_por_status**: Calcula a média de temperatura agrupada pelo local (Interno/Externo). Serve para comparar o clima entre ambientes.
2. **temp_max_min_por_dia**: Identifica os picos de calor e frio de cada dia monitorado. Essencial para análise de extremos térmicos.
3. **leituras_por_hora**: Agrupa a contagem de registros por hora. Ajuda a verificar se os sensores estão enviando dados de forma constante ao longo do dia.

##  Insights Obtidos
- **Constância Térmica**: Notou-se que a temperatura média geral se mantém estável em torno de 33°C.
- **Volume de Dados**: O sistema processou com sucesso mais de 97 mil registros, demonstrando robustez no pipeline de Big Data.