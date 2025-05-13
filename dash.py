import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import locale

try:
    # Tentando definir o locale para pt_BR com codificação UTF-8
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except locale.Error:
        pass


# Definição da paleta de cores para os gráficos
minha_paleta_de_cores_graficos = ['#8A3FFC', '#FF8C00', '#A076F9', '#FFB74D', '#D946EF', '#FF7043']

st.set_page_config(layout="wide")

# Incluindo o CSS customizado
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');

    html, body, [class*="st-"], [class*="css-"], .stButton>button, .stSelectbox, .stDateInput {
        font-family: 'Open Sans', sans-serif !important;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EAEAEA !important;
        border-radius: 10px !important;
        padding: 15px 20px 15px 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 10px !important;
    }

    div[data-testid="stMetricLabel"] > div {
        color: #5A5A5A !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #262730 !important;
        font-size: 1.75rem !important;
        font-weight: 600 !important;
    }
    
    h1 {
         font-weight: 700 !important;
         color: #31333F !important; 
    }

    h2, h3 { 
         font-weight: 600 !important;
         color: #31333F !important; 
         margin-top: 20px; 
         margin-bottom: 10px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("Benefícios concedidos do INSS")

caminho_base = "output/base_final.csv"

try:
    base_inss = pd.read_csv(caminho_base)
    if 'MES' in base_inss.columns:
        base_inss['MES'] = pd.to_datetime(base_inss['MES'])
        base_inss['MES_STR'] = base_inss['MES'].dt.strftime('%Y-%m')
    else:
        st.error("Coluna 'MES' não encontrada no arquivo. Esta coluna é essencial.")
        st.stop()

    if 'QTD_BENEFICIOS' in base_inss.columns:
        base_inss['QTD_BENEFICIOS'] = pd.to_numeric(base_inss['QTD_BENEFICIOS'], errors='coerce').fillna(0)
    if 'POPULACAO' in base_inss.columns:
        base_inss['POPULACAO'] = pd.to_numeric(base_inss['POPULACAO'], errors='coerce').fillna(0)

except FileNotFoundError:
    st.error(f"Arquivo não encontrado em: {caminho_base}")
    st.stop()
except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {e}")
    st.stop()

st.sidebar.header("Filtros")

min_data_disponivel = base_inss['MES'].min().date()
max_data_disponivel = base_inss['MES'].max().date()

st.sidebar.markdown("#### Selecione o Período (jun/24 a mar/25):")
data_inicio_selecionada = st.sidebar.date_input(
    "Início:",
    value=min_data_disponivel,
    min_value=min_data_disponivel,
    max_value=max_data_disponivel,
    key="data_inicio",
    help="O filtro considera o mês inteiro. Selecione o 1º dia do mês desejado."
)
data_fim_selecionada = st.sidebar.date_input(
    "Fim:",
    value=max_data_disponivel,
    min_value=min_data_disponivel,
    max_value=max_data_disponivel,
    key="data_fim",
    help="O filtro considera o mês inteiro. Selecione o 1º dia do mês desejado."
)

if data_inicio_selecionada > data_fim_selecionada:
    st.sidebar.error("A data de início não pode ser posterior à data de fim.")
    st.stop()

if 'REGIAO_PAIS' in base_inss.columns and not base_inss.empty:
    regioes = sorted(base_inss["REGIAO_PAIS"].dropna().unique())
    regioes_selecionadas = st.sidebar.multiselect("Região:", regioes, default=regioes)
else:
    regioes_selecionadas = []

if 'CID_TIPO' in base_inss.columns and not base_inss.empty:
    cids = sorted(base_inss["CID_TIPO"].dropna().unique())
    cids_selecionados = st.sidebar.multiselect("Categoria do CID:", cids, default=cids)
else:
    cids_selecionados = []

try:
    st.sidebar.image("imagens/beckz.png", use_container_width='stretch')
except FileNotFoundError:
    st.sidebar.warning("Arquivo da imagem 'imagens/beckz.png' não encontrado.")
except Exception as e:
    st.sidebar.error(f"Erro ao carregar a imagem: {e}")

base_inss_filtrada = base_inss.copy()

if 'REGIAO_PAIS' in base_inss_filtrada.columns and regioes_selecionadas:
    base_inss_filtrada = base_inss_filtrada[base_inss_filtrada["REGIAO_PAIS"].isin(regioes_selecionadas)]

periodo_inicio_filtro = pd.to_datetime(data_inicio_selecionada).to_period('M')
periodo_fim_filtro = pd.to_datetime(data_fim_selecionada).to_period('M')
base_inss_filtrada = base_inss_filtrada[
    base_inss_filtrada['MES'].dt.to_period('M').between(periodo_inicio_filtro, periodo_fim_filtro, inclusive='both')
]

if 'CID_TIPO' in base_inss_filtrada.columns and cids_selecionados:
    base_inss_filtrada = base_inss_filtrada[base_inss_filtrada["CID_TIPO"].isin(cids_selecionados)]

if base_inss_filtrada.empty:
    st.warning("Nenhum dado corresponde aos filtros selecionados.")
else:
    # BIG NUMBERS
    st.subheader("Indicadores Chave do Período Filtrado")

    total_beneficios_kpi = base_inss_filtrada['QTD_BENEFICIOS'].sum()

    if 'REGIAO_PAIS' in base_inss_filtrada.columns and 'POPULACAO' in base_inss_filtrada.columns:
        populacao_df_sum = base_inss_filtrada.groupby('REGIAO_PAIS')['POPULACAO'].first()
        populacao_coberta_kpi = populacao_df_sum.sum() if not populacao_df_sum.empty else 0
    else:
        populacao_coberta_kpi = 0

    if pd.isna(populacao_coberta_kpi):
        populacao_coberta_kpi = 0

    taxa_geral_kpi = (total_beneficios_kpi / populacao_coberta_kpi) * 100000 if populacao_coberta_kpi > 0 else 0
    meses_cobertos_kpi = base_inss_filtrada['MES_STR'].nunique() if 'MES_STR' in base_inss_filtrada.columns else 0

    # Visual
    #kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    #with kpi_col1:
        #st.metric(label="Total de Benefícios", value=f"{total_beneficios_kpi:,.0f}")
    #with kpi_col2:
        #st.metric(label="População Coberta", value=f"{populacao_coberta_kpi:,.0f}" if populacao_coberta_kpi > 0 else "N/D")
    #with kpi_col3:
        #st.metric(label="Taxa Geral (por 100K hab.)", value=f"{taxa_geral_kpi:,.2f}" if taxa_geral_kpi > 0 else "N/D")
    #with kpi_col4:
        #st.metric(label="Meses no Filtro", value=meses_cobertos_kpi)

    # Layout com 4 colunas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        fig1 = go.Figure(go.Indicator(
            mode="number",
            value=total_beneficios_kpi,
            title={"text": "Total de Benefícios"},
            number={"valueformat": ","}
        ))
        # Configurando os separadores no layout da figura
        fig1.update_layout(
            height=180,
            margin=dict(t=30, b=0, l=0, r=0),
            separators=',.'
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = go.Figure(go.Indicator(
            mode="number",
            value=populacao_coberta_kpi,
            title={"text": "População Coberta"},
            number={"valueformat": ","}
        ))
        # Configurando os separadores no layout da figura
        fig2.update_layout(
            height=180,
            margin=dict(t=30, b=0, l=0, r=0),
            separators=',.'
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        fig3 = go.Figure(go.Indicator(
            mode="number",
            value=round(taxa_geral_kpi, 2),
            title={"text": "Taxa Geral (por 100k hab.)"},
            number={"valueformat": ",.2f"}
        ))
        # Configurando os separadores no layout da figura
        fig3.update_layout(
            height=180,
            margin=dict(t=30, b=0, l=0, r=0),
            separators=',.' # ',' para decimal, '.' para milhar
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = go.Figure(go.Indicator(
            mode="number",
            value=meses_cobertos_kpi,
            title={"text": "Meses no Filtro"},
            # ",d" formata como inteiro e habilita agrupamento de milhares.
            number={"valueformat": ",d"}
        ))
        # Configurando os separadores no layout da figura
        fig4.update_layout(
            height=180,
            margin=dict(t=30, b=0, l=0, r=0),
            separators=',.'
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    
    # Definição das colunas

    col1_linha1, col2_linha1 = st.columns(2) # Gráfico de rosca dos benefícios por região / Gráfico de barras com o tipo do benefício
    col1_linha2, col2_linha2 = st.columns(2) # Gráfico de pareto por status do beneficiário / Gráfico de barras com a distribuição por faixa etária
    col1_linha3, col2_linha3 = st.columns(2) # Gráfico de barras com a taxa por região / Gráfico de barras com a taxa por mês e sexo
    
    altura_grafico = 450
    plotly_separators_config = ',.' # Definindo o separador de milhar para os gráficos

    # LINHA 1 DE GRÁFICOS
    with col1_linha1:
        st.subheader("Benefícios por Região (%)")
        if 'REGIAO_PAIS' in base_inss_filtrada.columns and 'QTD_BENEFICIOS' in base_inss_filtrada.columns:
            base_inss_regiao_qtd = base_inss_filtrada.groupby('REGIAO_PAIS')['QTD_BENEFICIOS'].sum().reset_index()
            base_inss_regiao_qtd = base_inss_regiao_qtd[base_inss_regiao_qtd['QTD_BENEFICIOS'] > 0]
            if not base_inss_regiao_qtd.empty and base_inss_regiao_qtd['QTD_BENEFICIOS'].sum() > 0 :
                total_beneficios_rosca = base_inss_regiao_qtd['QTD_BENEFICIOS'].sum()
                regiao_maior_valor_linha = base_inss_regiao_qtd.loc[base_inss_regiao_qtd['QTD_BENEFICIOS'].idxmax()]
                nome_maior_regiao = regiao_maior_valor_linha['REGIAO_PAIS']
                percentual_maior_regiao = (regiao_maior_valor_linha['QTD_BENEFICIOS'] / total_beneficios_rosca) * 100
                fig_rosca = px.pie(base_inss_regiao_qtd, names='REGIAO_PAIS', values='QTD_BENEFICIOS', hole=0.5, color_discrete_sequence=minha_paleta_de_cores_graficos)
                fig_rosca.update_layout(height=altura_grafico, annotations=[dict(text=f"<b>{nome_maior_regiao}</b><br>{(percentual_maior_regiao).round()}%", x=0.5, y=0.5, font_size=16, showarrow=False)], legend_title_text='Regiões', margin=dict(t=30, b=20, l=0, r=0), separators=plotly_separators_config)
                fig_rosca.update_traces(textposition='outside', textinfo='percent+label') 
                st.plotly_chart(fig_rosca, use_container_width=True)
            else: st.warning("Dados insuficientes ou zerados para gráfico de rosca por Região.")
        else: st.warning("Colunas 'REGIAO_PAIS' ou 'QTD_BENEFICIOS' não encontradas.")

        st.markdown("---")

    with col2_linha1:
        st.subheader("Benefícios por Tipo")
        if 'BENEF_TIPO' in base_inss_filtrada.columns and 'QTD_BENEFICIOS' in base_inss_filtrada.columns:
            benef_tipo_agg = base_inss_filtrada.groupby('BENEF_TIPO')['QTD_BENEFICIOS'].sum().reset_index()
            benef_tipo_agg = benef_tipo_agg[benef_tipo_agg['QTD_BENEFICIOS'] > 0]
            benef_tipo_agg = benef_tipo_agg.sort_values(by='QTD_BENEFICIOS', ascending=False)
            if not benef_tipo_agg.empty:
                fig_bar_benef_tipo = px.bar(benef_tipo_agg, x='QTD_BENEFICIOS', y='BENEF_TIPO', orientation='h', labels={'QTD_BENEFICIOS': 'Qtd. Benefícios', 'BENEF_TIPO': 'Tipo de Benefício'}, text='QTD_BENEFICIOS', color='BENEF_TIPO', color_discrete_sequence=minha_paleta_de_cores_graficos)
                fig_bar_benef_tipo.update_layout(height=altura_grafico, yaxis={'categoryorder':'total ascending'}, margin=dict(t=30, b=40, l=0, r=0), showlegend=False, separators=plotly_separators_config)
                fig_bar_benef_tipo.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
                st.plotly_chart(fig_bar_benef_tipo, use_container_width=True)
            else: st.warning("Sem dados para gráfico de Benefícios por Tipo.")
        else: st.warning("Colunas 'BENEF_TIPO' ou 'QTD_BENEFICIOS' não encontradas.")

        st.markdown("---")

    # LINHA 2 DE GRÁFICOS
    with col1_linha2:
        st.subheader("Pareto por Status do Beneficiário")
        if 'STATUS_BENEFICIARIO' in base_inss_filtrada.columns and 'QTD_BENEFICIOS' in base_inss_filtrada.columns:
            pareto_data = base_inss_filtrada.groupby('STATUS_BENEFICIARIO')['QTD_BENEFICIOS'].sum().sort_values(ascending=False).reset_index()
            if not pareto_data.empty and pareto_data['QTD_BENEFICIOS'].sum() > 0:
                pareto_data['CUMSUM_BENEFICIOS'] = pareto_data['QTD_BENEFICIOS'].cumsum()
                total_beneficios_pareto = pareto_data['QTD_BENEFICIOS'].sum()
                pareto_data['CUMPERCENT_BENEFICIOS'] = (pareto_data['CUMSUM_BENEFICIOS'] / total_beneficios_pareto) * 100

                fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
                fig_pareto.add_trace(
                    go.Bar(x=pareto_data['STATUS_BENEFICIARIO'], y=pareto_data['QTD_BENEFICIOS'], name='Qtd. Benefícios',
                           marker_color=minha_paleta_de_cores_graficos[0], text=pareto_data['QTD_BENEFICIOS'],
                           texttemplate='%{text:,.0f}', textposition='auto'),
                    secondary_y=False,
                )
                fig_pareto.add_trace(
                    go.Scatter(x=pareto_data['STATUS_BENEFICIARIO'], y=pareto_data['CUMPERCENT_BENEFICIOS'], name='% Acumulado',
                               marker_color=minha_paleta_de_cores_graficos[1], yaxis='y2'),
                    secondary_y=True,
                )
                fig_pareto.update_layout(title_text='Pareto por Status', height=altura_grafico, separators=plotly_separators_config, margin=dict(t=50, b=20, l=0, r=0))
                fig_pareto.update_xaxes(title_text='Status do Beneficiário')
                fig_pareto.update_yaxes(title_text='Qtd. Benefícios', secondary_y=False, tickformat=',.0f') 
                fig_pareto.update_yaxes(title_text='% Acumulado', secondary_y=True, range=[0, 105], ticksuffix='%', tickformat='.0f')
                st.plotly_chart(fig_pareto, use_container_width=True)
            else:
                st.warning("Dados insuficientes para Pareto por Status.")
        else:
            st.warning("Colunas 'STATUS_BENEFICIARIO' ou 'QTD_BENEFICIOS' não encontradas para Pareto.")

        st.markdown("---")

    with col2_linha2:
        st.subheader("Distribuição por Faixa Etária")
        if 'IDADE_FAIXA' in base_inss_filtrada.columns and 'QTD_BENEFICIOS' in base_inss_filtrada.columns:
            hist_idade_data = base_inss_filtrada.groupby('IDADE_FAIXA', as_index=False)['QTD_BENEFICIOS'].sum()
            hist_idade_data = hist_idade_data[hist_idade_data['QTD_BENEFICIOS'] > 0]
            if not hist_idade_data.empty:
                try:
                    hist_idade_data['sort_key'] = hist_idade_data['IDADE_FAIXA'].str.extract(r'(\d+)').astype(int)
                    hist_idade_data = hist_idade_data.sort_values(by='sort_key').reset_index(drop=True)
                except Exception:
                    hist_idade_data = hist_idade_data.sort_values(by='IDADE_FAIXA').reset_index(drop=True)
                
                fig_hist_idade = px.bar(
                    hist_idade_data, x='IDADE_FAIXA', y='QTD_BENEFICIOS',
                    labels={'IDADE_FAIXA': 'Faixa Etária', 'QTD_BENEFICIOS': 'Quantidade de Benefícios'},
                    color='IDADE_FAIXA', color_discrete_sequence=minha_paleta_de_cores_graficos,
                    text='QTD_BENEFICIOS'
                )
                fig_hist_idade.update_layout(
                    height=altura_grafico, separators=plotly_separators_config,
                    yaxis_tickformat=',.0f', xaxis_title="Faixa Etária", yaxis_title="Quantidade de Benefícios",
                    margin=dict(t=30, b=20, l=0, r=0),
                    showlegend=(len(hist_idade_data['IDADE_FAIXA'].unique()) <= 10 and 'color' in fig_hist_idade.layout) 
                )
                fig_hist_idade.update_xaxes(type='category', categoryorder='array', categoryarray=hist_idade_data['IDADE_FAIXA'].tolist())
                fig_hist_idade.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
                st.plotly_chart(fig_hist_idade, use_container_width=True)
            else:
                st.warning("Nenhuma faixa etária com benefícios para o histograma.")
        else:
            st.warning("Colunas 'IDADE_FAIXA' ou 'QTD_BENEFICIOS' não encontradas para o histograma.")

        st.markdown("---")

    # LINHA 3 DE GRÁFICOS
    with col1_linha3:
        st.subheader("Taxa por Região (100k hab)")
        if all(col in base_inss_filtrada.columns for col in ['REGIAO_PAIS', 'QTD_BENEFICIOS', 'POPULACAO']):
            base_inss_agg_regiao_rate = base_inss_filtrada.groupby('REGIAO_PAIS').agg(QTD_BENEFICIOS_TOTAL=('QTD_BENEFICIOS', 'sum'), POPULACAO_DA_REGIAO=('POPULACAO', 'first')).reset_index()
            base_inss_agg_regiao_rate = base_inss_agg_regiao_rate[base_inss_agg_regiao_rate['POPULACAO_DA_REGIAO'] > 0]
            if not base_inss_agg_regiao_rate.empty:
                base_inss_agg_regiao_rate['TAXA_CALCULADA_POR_REGIAO'] = (base_inss_agg_regiao_rate['QTD_BENEFICIOS_TOTAL'] / base_inss_agg_regiao_rate['POPULACAO_DA_REGIAO']) * 100000
                base_inss_agg_regiao_rate = base_inss_agg_regiao_rate.sort_values(by='TAXA_CALCULADA_POR_REGIAO', ascending=False)
                fig_bar_taxa_regiao = px.bar(base_inss_agg_regiao_rate, x='REGIAO_PAIS', y='TAXA_CALCULADA_POR_REGIAO', labels={'TAXA_CALCULADA_POR_REGIAO': 'Taxa por 100k hab.', 'REGIAO_PAIS': 'Região'}, color='REGIAO_PAIS', color_discrete_sequence=minha_paleta_de_cores_graficos)
                fig_bar_taxa_regiao.update_layout(height=altura_grafico, margin=dict(t=30, b=40, l=0, r=0), showlegend=False, separators=plotly_separators_config, yaxis_tickformat=',.2f')
                st.plotly_chart(fig_bar_taxa_regiao, use_container_width=True)
            else: st.warning("Não foi possível calcular a Taxa por Região.")
        else: st.warning("Colunas para Taxa por Região não encontradas.")

    with col2_linha3:
        st.subheader("Taxa por Mês e Sexo")
        if all(col in base_inss_filtrada.columns for col in ['MES_STR', 'SEXO', 'QTD_BENEFICIOS', 'REGIAO_PAIS', 'POPULACAO']):
            populacao_denominador_barras = 0
            if regioes_selecionadas: populacao_denominador_barras = base_inss[base_inss['REGIAO_PAIS'].isin(regioes_selecionadas)].groupby('REGIAO_PAIS')['POPULACAO'].first().sum()
            elif not base_inss.empty: populacao_denominador_barras = base_inss.groupby('REGIAO_PAIS')['POPULACAO'].first().sum()
            if pd.isna(populacao_denominador_barras): populacao_denominador_barras = 0
            if populacao_denominador_barras > 0:
                base_inss_agg_bar = base_inss_filtrada.groupby(["MES_STR", "SEXO"]).agg(QTD_BENEFICIOS_AGRUPADO=('QTD_BENEFICIOS', 'sum')).reset_index()
                base_inss_agg_bar["TAXA_CALCULADA"] = (base_inss_agg_bar["QTD_BENEFICIOS_AGRUPADO"] / populacao_denominador_barras) * 100000
                base_inss_agg_bar = base_inss_agg_bar.sort_values("MES_STR")
                fig_bar = px.bar(base_inss_agg_bar, x="MES_STR", y="TAXA_CALCULADA", color="SEXO", labels={"TAXA_CALCULADA": "Taxa por 100k hab.", "MES_STR": "Mês"}, barmode="group", color_discrete_sequence=minha_paleta_de_cores_graficos)
                fig_bar.update_layout(height=altura_grafico, margin=dict(t=30, b=40, l=0, r=0), separators=plotly_separators_config, yaxis_tickformat=',.2f')
                st.plotly_chart(fig_bar, use_container_width=True)
            else: st.warning("População denominador zero ou N/D para Taxa por Mês e Sexo.")
        else: st.warning("Colunas para Taxa por Mês e Sexo não encontradas.")