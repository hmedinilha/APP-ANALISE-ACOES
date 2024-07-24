import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.express as px
import numpy as np
from datetime import date, datetime
import ta as ta
import fundamentus




st.title('Análise Fundamentalista')
st.caption('Através da análise fundamentalista, podemos encontrar um ativo saudável')
st.divider()


   
c1, c2 = st.columns(2)
with c1:
    
    lista_papel = fundamentus.list_papel_all()
    
    papel = st.selectbox('Escolha o ativo', options=lista_papel, index=3).upper()
    

with c2:
    data_inicial = st.date_input('Data Inicial', format="DD/MM/YYYY", value= date(2023, 1, 1))
    df=pd.DataFrame(yf.download(f'{papel}.SA', start = data_inicial, end = datetime.now()).Close)
    



    

st.header(f'Análise Fundamentalista {papel}')
    
    #Dados tratados para o gráfico#

    #Dados do IBOV#
dadosibov = yf.download('^BVSP', start = data_inicial, end = datetime.now()).Close
dadosibov_normalizado = pd.DataFrame(dadosibov / dadosibov.iloc[0])
dadosibov_normalizado['IBOV'] = dadosibov_normalizado
dadosibov_normalizado['Data'] = dadosibov_normalizado.index

#Dados da seleção#
data_compare = df['Close']
try:
    data_normalizado = pd.DataFrame(data_compare / data_compare.iloc[0])
    data_normalizado[f'{papel}'] = data_normalizado
    data_normalizado['Data']= data_normalizado.index
except IndexError:
     st.error('ATIVO SEM DADOS')
     st.stop()



dadosibov_normalizado = pd.DataFrame(dadosibov / dadosibov.iloc[0])
dadosibov_normalizado['IBOV'] = dadosibov_normalizado
dadosibov_normalizado['Data'] = dadosibov_normalizado.index


data_mesclada = pd.merge(data_normalizado, dadosibov_normalizado, how='inner',on='Data').drop(columns=['Close_x','Close_y'])   
data_melt = pd.melt(data_mesclada, id_vars='Data')
data_melt.columns=('Data','Ticker','Retorno')
data_retorno = data_mesclada.copy()
data_retorno['Retorno'] = np.where((data_retorno[f'{papel}'] >= data_retorno['IBOV']), 
                            'Acima do IBOV', 'Abaixo do IBOV')
dias_acima=  []
try:

    dias_acima=data_retorno['Retorno'].value_counts()['Acima do IBOV']

except KeyError: 
    dias_acima=0

dias_ = len(data_retorno['Retorno'])
status_= data_retorno['Retorno'].iloc[-1]
data_retorno['Diferença%'] = (data_retorno[f'{papel}'] - data_retorno['IBOV']) / data_retorno['IBOV'] * 100
porcentagem_ = round(data_retorno['Diferença%'].iloc[-1], ndigits=2)

#Dados fundamentalistas#
fundamento = pd.DataFrame(fundamentus.get_detalhes_papel(f'{papel}'))








tab1, tab2, tab3 = st.tabs([f"Gráfico Rentabilidade IBOV x {papel}", "Dados do ativo na B3", "Dados Fundamentalistas"])

with tab1:
    fig = px.line(data_melt, x="Data",y="Retorno",
    hover_data={"Data": "|%d %B, %Y"},
    markers=True,
    color="Ticker")
    fig.update_xaxes(
            dtick="M1",
            tickformat="%b\n%Y")
    st.plotly_chart(fig)
    st.write(f'A rentabilidade do ativo ficou {dias_acima} dias acima do IBOV no período de {dias_} dias')
    st.write(f'Atualmente o ativo está com rentabilidade {status_} com distância de {porcentagem_} %')

with tab2:

    
    with st.container(border=True):
            st.subheader('**Dados do ativo na B3**', divider='orange')
            st.metric('**Papel**', value=str(fundamento['Papel'].iloc[0]+' '+fundamento['Tipo'].iloc[0]))
            st.caption('Papel - B3')

            st.write("\n")
            st.metric('**Setor**', value=str(fundamento['Setor'].iloc[0]))
            st.caption('Setor de atuação - B3')


            st.write("\n")
            st.metric('**Subsetor**', value=str(fundamento['Subsetor'].iloc[0]))
            st.caption('Subsetor de atuação - B3')


    
with tab3:
    with st.container(border=True):
            st.subheader('**Dados Fundamentalistas**', divider='orange')      
            st.metric('**P/L**', value=float(fundamento['PL'].iloc[0])/100)
            st.caption('Preço da ação dividido pelo lucro por ação')
            st.write("\n")
            st.metric('**P/VP**', value=float(fundamento['PVP'].iloc[0])/100)
            st.caption('Preço da ação dividido pelo valor patrimonial')
            st.write("\n")
            st.metric('**Dividend Yield**', value=fundamento['Div_Yield'].iloc[0])
            st.caption('Dividendo pago por ação dividido preço da ação')



