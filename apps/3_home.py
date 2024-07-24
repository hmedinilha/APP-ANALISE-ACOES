import streamlit as st


st.header('App Análise de ações :bar_chart:')



col1, col2 = st.columns([1,1], gap='large', vertical_alignment='top')


container = st.container(border=True)
with col1:
    
    st.write('\n')
    st.subheader('Análise técnica :chart_with_upwards_trend:')
    st.divider()
    st.write('A partir da seleção, o app plota os dados historicos com a data de início indicada e o '
                'ativo escolhido, promove também a inclusão de médias móveis, volume de negócios, IFR e sumário do ativo baseado em seu desempenho na B3. '
                'O app também dispõe de uma ferramenta de análise onde podemos gerar visões específicas.')

with col2:
    
    st.write('\n')
    st.subheader('Fundamentalista :book:')
    st.divider()
    st.write('A partir da seleção, o app plota os dados fundamentalistas do '
                'ativo escolhido baseado nos dados do provedor https://fundamentus.com.br .')
    
st.caption('Desenvolvido por Hernandes Medinilha :link: https://www.linkedin.com/in/hernandes-medinilha/')


