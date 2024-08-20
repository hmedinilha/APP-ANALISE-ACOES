import streamlit as st
from streamlit_extras.stylable_container import stylable_container


st.header('App Análise de ações :bar_chart:')










col1, col2 = st.columns([1,1], gap='large', vertical_alignment='top')

with col1, stylable_container(key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 1rem;
                box-shadow: 10px 10px 5px 0px rgba(179,170,170,0.75);
                padding: calc(1em - 1px)
            }
            """,
    ):
    container = st.container(border=True, height=300)
    container.subheader('Análise técnica :chart_with_upwards_trend:')
    container.page_link("apps/1_analise_tecnica.py", label="Analise Técnica", icon=':material/candlestick_chart:')
    container.markdown('___')
    container.write('A partir da seleção, o app plota os dados historicos com a data de início indicada e o '
                        'ativo escolhido, promove também a inclusão de médias móveis, volume de negócios, IFR e sumário do ativo baseado em seu desempenho na B3. '
                        'O app também dispõe de uma ferramenta de análise onde podemos gerar visões específicas.')
    
    

with col2, stylable_container(key="container_with_border2",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 1rem;
                box-shadow: 10px 10px 5px 0px rgba(179,170,170,0.75);
                padding: calc(1em - 1px)
            }
            """,
    ):
    container2 = st.container(border=True, height=300)
    container2.subheader('Fundamentalista :book:')
    container2.page_link("apps/2_fundamento_acoes.py", label="Análise Fundamentalista", icon=':material/book_3:')
    container2.divider()
    container2.write('A partir da seleção, o app plota os dados fundamentalistas do '
                'ativo escolhido baseado nos dados do provedor https://fundamentus.com.br .')
    



