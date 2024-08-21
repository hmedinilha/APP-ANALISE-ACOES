import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import date, datetime, timedelta
import ta as ta
import fundamentus
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.row import row
from deep_translator import GoogleTranslator
import requests
from bcb import sgs


tradutor = GoogleTranslator(source= "auto", target= "pt")



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

@st.cache_data
def cdi_data():
    cdi = sgs.get({'CDI' : 4390}, start=data_inicial)
    cdi['Data']=cdi.index
    return cdi

cdi=cdi_data()

ibov_cdi= pd.merge(dadosibov_normalizado, cdi, how='inner', on='Data')



data_mesclada = pd.merge(data_normalizado, ibov_cdi, how='inner',on='Data').drop(columns=['Close_x','Close_y'])   
data_melt = pd.melt(data_mesclada, id_vars='Data')
data_melt.columns=('Data','Ticker','Retorno')

data_retorno = pd.merge(data_normalizado, dadosibov_normalizado, how='inner',on='Data').drop(columns=['Close_x','Close_y'])

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



#calculo volatilidade
     
df['vols'] = (df['Close'].pct_change()[1:]).std()*np.sqrt(252)

# grafico boxplot
def boxplot():
     fig = go.Figure()
     fig.add_trace(go.Box(y=df['Close'], name='Preços',
                marker_color = 'lightseagreen'))
     return fig

valorhj=df['Close'].iloc[-1]


#Dados fundamentalistas#
fundamento = pd.DataFrame(fundamentus.get_papel(f'{papel}'))








tab1, tab2, tab3 = st.tabs([f"Gráfico Rentabilidade {papel}", "Dados do ativo na B3", "Dados Fundamentalistas"])

with tab1:
    cc1, cc2 = st.columns([1,1])
    fig = px.line(data_melt, x="Data",y="Retorno",
    hover_data={"Data": "|%d %B, %Y"},
    markers=True,
    color="Ticker")
    fig.update_xaxes(
            dtick="M1",
            tickformat="%b\n%Y")
    cc1.subheader('Gráfico Retorno do ativo')
    
    cc1.plotly_chart(fig)

    cc1.write(f'A rentabilidade do ativo ficou {dias_acima} dias acima do IBOV no período de {dias_} dias')
    cc1.write(f'Atualmente o ativo está com rentabilidade {status_} com distância de {porcentagem_} %')
    
    cc2.subheader('Distribuição do preço')
   
    cc2.plotly_chart(boxplot())
    cc2.write(f'O índice de volatilidade do ativo ficou em {round(df['vols'].iloc[0]*100, ndigits=2)} % no período de {dias_} dias')
    cc2.write(f'O preço atual do ativo é R$ {round(valorhj, ndigits=2)}.')

    

with tab2:

    col1, col2 = st.columns([1,1])
    df2 = yf.Ticker(f"{papel.upper()}.SA").info
    try:
         colab=df2['fullTimeEmployees']
    except KeyError:
         colab='não informado'
    
    with col1, st.container(border=True):
            
            st.subheader('**Dados do ativo na B3**', divider='orange')
            row1 = row([0.2, 0.8], vertical_align="center")
            try:
                img=f'https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/{papel}.png'
                response = requests.get(img)
                if response.status_code == 404:
                    row1.image('no-logo.png',width=85)
                else:
                    row1.image(img, width=85)
            except requests.exceptions.RequestException as e:
                      print(f"Erro ao acessar o link {img}: {e}")

            row1.metric('**Papel**', value=str(fundamento['Papel'].iloc[0]+' '+fundamento['Tipo'].iloc[0]), help='Papel - B3')
            
            st.write("\n")
            st.metric('**Setor**', value=str(fundamento['Setor'].iloc[0]), help='Setor de atuação - B3')
            
            st.write("\n")
            st.metric('**Subsetor**', value=str(fundamento['Subsetor'].iloc[0]), help='Subsetor de atuação - B3')

            st.write("\n")
            st.metric('**Colaboradores**', value=colab)

            st.write("\n")
            st.write(df2['website'])
            st.caption('Site da companhia')

           

            
    
    with col2, st.container(border=True):
         
         st.subheader('**Conselho Administração**', divider='orange')
         
         tabela = pd.DataFrame(df2['companyOfficers'])
         tabela.drop(['maxAge', 'exercisedValue', 'unexercisedValue'], axis='columns', inplace=True)
         tabela.rename(columns={'name': 'Nome', 'age':'Idade', 'title':'Cargo', 'yearBorn':'Nasc.'}, inplace=True)
         tabela = tabela.map(str)
         st.table(tabela)
         
         st.write('\n')
         st.subheader('**Descrição do negócio**', divider='orange')
         texto=df2['longBusinessSummary']
         st.write(tradutor.translate(texto))
        
style_metric_cards(border_left_color='#ccc9')
         


    
with tab3:
    
    df3 = pd.DataFrame(yf.Ticker(f"{papel.upper()}.SA").dividends)
    df3['Data'] = df3.index.year
    df3['div'] = df3['Dividends']
    data_atual = datetime.now()
    year5 = data_atual - timedelta(days=1800)
    mask = (df3["Data"] > year5.year)
    df3['Data'] =df3['Data'].loc[mask].dropna()
    
    sub = df3.groupby('Data')['div'].sum().reset_index()
    sub['div2']=round(sub['div'], ndigits=2)
    ebit = pd.DataFrame(yf.Ticker(f"{papel.upper()}.SA").income_stmt)
    #st.dataframe(fundamento)
    
    #verificador do dataframe

    if fundamento['PL'].iloc[0] == '-':
         pl = 'não informado'
    else:
         pl = float(fundamento['PL'].iloc[0])/100

    if fundamento['EV_EBITDA'].iloc[0] == '-':
         ev_ebitda = 'não informado'
    else:
         ev_ebitda = float(fundamento['EV_EBITDA'].iloc[0])/100

    if fundamento['PVP'].iloc[0] == '-':
         pvp = 'não informado'
    else:
         pvp = float(fundamento['PVP'].iloc[0])/100

    if fundamento['Marg_Liquida'].iloc[0] == '-':
         m_liq = 'não informado'
    else:
         m_liq = fundamento['Marg_Liquida'].iloc[0]

    if fundamento['Div_Yield'].iloc[0] == '-':
         dyeld = 'não informado'
    else:
         dyeld = fundamento['Div_Yield'].iloc[0]

    if fundamento['Liquidez_Corr'].iloc[0] == '-':
         liq_corr = 'não informado'
    else:
         liq_corr = float(fundamento['Liquidez_Corr'].iloc[0])/100 


    #print(list(fundamento))
    cb1, cb2 = st.columns([1,1])
    with cb1, st.container(border=True):
            st.subheader('**Dados Fundamentalistas**', divider='orange') 
            row2=row([1,1])     
            row2.metric('**P/L**', value=pl, help='Preço da ação dividido pelo lucro por ação')
            row2.metric('**EV/EBITDA**', value=ev_ebitda, help='O EV (Enterprise Value ou Valor da Firma), indica quanto custaria para comprar todos os ativos da companhia, descontando o caixa. Este indicador mostra quanto tempo levaria para o valor calculado no EBITDA pagar o investimento feito para compra-la. Saiba mais em: https://statusinvest.com.br/termos/e/ev-ebitda')
            
            st.write("\n")
            row2.metric('**P/VP**', value=pvp, help='Preço da ação dividido pelo valor patrimonial')
            row2.metric('**Magerm Liquida**', value=m_liq, help='Revela a porcentagem de lucro em relação às receitas de uma empresa.')
            st.write("\n")
            row2.metric('**Dividend Yield**', value=dyeld, help='Dividendo pago por ação dividido preço da ação')
            row2.metric('**Liquidez Corrente**', value=liq_corr, help='Indica a capacidade de pagamento da empresa no curto prazo. Saiba mais em: https://statusinvest.com.br/termos/l/liquidez-corrente')
           
    cb2.subheader('Dividendos últimos 5 anos', divider='orange')
    fig2 = px.bar(sub, x='Data', y='div2',
             hover_data=['div2'], color='div2',
             labels={'div2':'Dividendos em R$'})
    cb2.plotly_chart(fig2)
    
    


