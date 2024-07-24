
import pandas as pd
import yfinance as yf
import streamlit as st
import mplfinance as mpf
import numpy as np
from datetime import date, datetime
import ta as ta
from pygwalker.api.streamlit import StreamlitRenderer



@st.cache_data(persist='disk')
def get_data(symbol, date_from):
    data = get_historical_data(symbol, str(date_from))
    if len(data) == 0:
        st.error('ATIVO SEM DADOS')
        st.stop()
    else:
        return data


@st.cache_data(persist='disk')
def get_historical_data(symbol, start_date = None):
    df = yf.download(f'{symbol}.SA', start=start_date, end=datetime.now())
    for col in df.columns:
        df[col] = df[col].astype(float)
    df.index = pd.to_datetime(df.index)
    if start_date:
        df = df[df.index >= start_date]
    return df

st.title('Análise Técnica Ações')
st.caption('Através da análise técnica, podemos encontrar o melhor ponto de entrada no ativo')
st.divider()

c1, c2, = st.columns([1,1],vertical_alignment='center')

ticker = st.checkbox('Digitar o ativo no campo', False)



with c1:
    
    if ticker:
        symbol = st.text_input('Digite o ativo',value = 'PETR4', help='SEMPRE USE O TICKER PADRÃO B3').upper()
        
    else:
        
        list_bovespa_full = pd.read_csv('ticker ibov.csv', delimiter=';')
        symbol = st.selectbox('Escolha o ativo', options=list_bovespa_full['Código'], index=2)
        

            
with c2:
        
        date_from = st.date_input('Data Inicial',format="DD/MM/YYYY", value= date(2023, 1, 1))
    

st.markdown('---')


## PLOTAR O GRAFICO ATRAVES DA FUNÇÃO ##

def plot_data(symbol, date_from, data):
    
    data2 = data.copy()
    if data2['Open'] is not 0:
        data2.drop(data.tail(1).index, inplace=True)
        data2['media_1'] = data2['Close'].rolling(window=mav1).mean()
        data2['media_2'] = data2['Close'].rolling(window=mav2).mean()
        data2['volume_medio'] = data2['Volume'].rolling(window=mav3).mean()
        data2['RSI'] = ta.momentum.rsi(data2['Close'], window=14)
        data2['30'] = 30
        data2['70'] = 70


        data2['MMS20BB'] = data2['Close'].rolling(window = 20).mean()
        data2['Desvio_Padrao'] = data2['Close'].rolling(window = 20).std()
        data2['Banda_Superior'] = data2['MMS20BB'] + (data2['Desvio_Padrao'] * 2)
        data2['Banda_Inferior'] = data2['MMS20BB'] - (data2['Desvio_Padrao'] * 2)
    else:
        data2['media_1'] = data2['Close'].rolling(window=mav1).mean()
        data2['media_2'] = data2['Close'].rolling(window=mav2).mean()
        data2['volume_medio'] = data2['Volume'].rolling(window=mav3).mean()
        data2['RSI'] = ta.momentum.rsi(data2['Close'], window=14)
        data2['30'] = 30
        data2['70'] = 70


        data2['MMS20BB'] = data2['Close'].rolling(window = 20).mean()
        data2['Desvio_Padrao'] = data2['Close'].rolling(window = 20).std()
        data2['Banda_Superior'] = data2['MMS20BB'] + (data2['Desvio_Padrao'] * 2)
        data2['Banda_Inferior'] = data2['MMS20BB'] - (data2['Desvio_Padrao'] * 2)

#canal desvio padrao com regressao linear, calcular a regressao linear, calcular uma coluna com +2 desvios e -2 desvios informando o periodo

        
## GRAFICOS AUXILIARES ##
    if volume:
        painel=2
    else:
        painel=1

    linha30 = mpf.make_addplot(data2['30'], 
                            color='red',
                            linestyle='-.',
                            panel = painel
                            )
    
    linha70 = mpf.make_addplot(data2['70'], 
                            color='green',
                            linestyle='-.',
                            panel = painel
                            )
    ifrplot = mpf.make_addplot(data2['RSI'], 
                label='IFR', 
                panel=painel,
                color='red',
                ylim=(10, 90)                                 
            )
    
        
    ax_media1 = mpf.make_addplot(data2['media_1'],
                    label=f'Média 1 {mav1}',
                    color='green',
                    panel=0,
                    )
    ax_media2 = mpf.make_addplot(data2['media_2'],
                    label=f'Média 2 {mav2}',
                    color='blue',
                    panel=0,
                    )
    volumeplot = mpf.make_addplot(data2['volume_medio'], 
                label=f'Vol Média {mav3}', 
                panel=1,
                color='red'
                )
    
    bbollinger_plotm = mpf.make_addplot(data2['MMS20BB'], 
                label='Bandas de Bollinger Média', 
                panel=0,
                linestyle='-.',
                color='orange')  
                
    bbollinger_plotbs = mpf.make_addplot(data2['Banda_Superior'],
                    label='Bandas de Bollinger Superior',
                    panel=0,
                    color='green'
                    )
    bbollinger_plotbi = mpf.make_addplot(data2['Banda_Inferior'],
                    label='Bandas de Bollinger Inferior',
                    panel=0,
                    color='red'
                    )
    
## LOGICA DE EXIBIÇÃO ##
    
    if volume and ifr and medias and not bbollinger:
        plotar = [volumeplot,
                ax_media1,
                ax_media2,
                ifrplot,
                linha30,
                linha70
        ]
        
    elif volume and ifr and medias and bbollinger:
        plotar = [volumeplot,
                bbollinger_plotm,
                bbollinger_plotbi,
                bbollinger_plotbs,
                ifrplot,
                linha30,
                linha70
        ]

    elif volume and ifr and not medias and not bbollinger:
        plotar = [volumeplot,
                ifrplot,
                linha30,
                linha70
                
        ]

    elif volume and ifr and not medias and bbollinger:
        plotar = [volumeplot,
                ifrplot,
                linha30,
                linha70,
                bbollinger_plotm,
                bbollinger_plotbi,
                bbollinger_plotbs

        ]

    elif volume and not ifr and medias and not bbollinger:
        plotar = [volumeplot,
                ax_media1,
                ax_media2
        ]

    elif volume and not ifr and not medias and bbollinger:
        plotar = [volumeplot,
                bbollinger_plotm,
                bbollinger_plotbi,
                bbollinger_plotbs
        ]
        
    elif volume and not ifr and not medias and not bbollinger:
        plotar = [volumeplot,
                
        ]   
    
    elif not volume and ifr and not medias and bbollinger:
        plotar = [bbollinger_plotbi,
                bbollinger_plotbs,
                bbollinger_plotm,
                ifrplot,
                linha30,
                linha70         
        ]
        
    elif not volume and ifr and not medias and not bbollinger:
        plotar = [ifrplot,
                linha30,
                linha70         
        ] 
        
    elif not volume and not ifr and medias and not bbollinger:
        plotar = [ax_media1,
                ax_media2
                        
        ] 
        
    elif not volume and ifr and medias and not bbollinger:
        plotar = [ax_media1,
                ax_media2,
                ifrplot,
                linha30,
                linha70
                        
        ]
        
    elif not volume and not ifr and not medias and bbollinger:
        plotar = [bbollinger_plotbi,
                bbollinger_plotbs,
                bbollinger_plotm
                        
        ]
        
    elif volume and not ifr and medias and bbollinger:
        plotar = [bbollinger_plotbi,
                bbollinger_plotbs,
                bbollinger_plotm,
                volumeplot
                        
        ]
        
    elif not volume and ifr and medias and bbollinger:
        plotar = [bbollinger_plotbi,
                bbollinger_plotbs,
                bbollinger_plotm,
                ifrplot,
                linha30,
                linha70
                        
        ]
        
    elif not volume and ifr and medias and not bbollinger:
        plotar = [ax_media1,
                ax_media2,
                ifrplot,
                linha30,
                linha70
                        
        ]
        
    elif not volume and not ifr and medias and bbollinger:
        plotar = [bbollinger_plotbi,
                bbollinger_plotbs,
                bbollinger_plotm
                        
        ]
    
    else:
        
        plotar = [

        ]

                    
## DESENHAR O GRAFICO ##
    

    fig, ax = mpf.plot(
        data2,
        title= f'Ticker {symbol}, Companhia {symbol}, Dados desde: {date_from.strftime("%d/%m/%Y")}',
        type=chart_type,
        show_nontrading=show_nontrading_days,
        datetime_format='%d-%m-%Y',
        volume=volume,
        style=chart_style,
        addplot=plotar,
        
        ylabel='Preço do Ativo',
        ylabel_lower = 'Volume',
        figsize=(16,10),     

        returnfig=True
    )



    st.pyplot(fig)



with st.expander('Análise Técnica'):
    st.write('Parâmetros Gráficos')
    
    c1, c2, c3 = st.columns([1,1,1])
    

    with c1:

        show_nontrading_days = st.checkbox('Mostrar finais de semana?', False)
        volume=st.checkbox('Plotar Volume?', True)
    
    with c2:

        chart_styles = [
            'default', 'binance', 'blueskies', 'brasil', 
            'charles', 'checkers', 'classic', 'yahoo',
            'mike', 'nightclouds', 'sas', 'starsandstripes'
        ]
        chart_style = st.selectbox('Estilo do Gráfico', options=chart_styles, index=chart_styles.index('yahoo'))

    with c3:
        chart_types = ['candle', 'ohlc', 'line']
        chart_type = st.selectbox('Tipo de gráfico', options=chart_types, index=chart_types.index('candle'))
    
    
    

    st.markdown('---')
    medias =st.checkbox('Médias Aritiméticas')
    visibilidade = 'collapsed'
    habilitar=True
    if medias:
        visibilidade = "visible"
        habilitar=False
    
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        mav1 = st.number_input('Média 1', min_value=3, max_value=30, value=9, step=1, label_visibility=visibilidade, disabled=habilitar)
    with c2:
        mav2 = st.number_input('Média 2', min_value=3, max_value=30, value=20, step=1, label_visibility=visibilidade, disabled=habilitar)
    with c3:
        mav3 = st.number_input('Média Vol', min_value=3, max_value=200, value=50, step=1, label_visibility=visibilidade, disabled=habilitar)
        
        
            
    st.markdown('---')
    st.write('Indicadores Técnicos')
    c1, c2 = st.columns([1,1])
    with c1:
            ifr = st.checkbox('IFR 14 períodos', value=False)
    with c2:
            bbollinger = st.checkbox('Bandas de Bollinger', value = False)
            

## METRICAS PARA CALIBRAR O GRAFICO ##

def cards():
    data = get_data(symbol, date_from)
    c1, c2, c3, c4  = st.columns([1,1,1,1])
    
    with c1:
        b1=st.container(border=True)
        data1 = data.copy()
        data2 = data1.dropna()
        media52dias = pd.to_datetime('today') - pd.DateOffset(days=90)
        media52 = data2.index >= media52dias
        positions = media52
        media52_filtrada = data2.iloc[positions]['Close']
        delta52 = data2['Close'].pct_change(periods=90)

        b1.metric('Média de 90 dias', value = round(media52_filtrada.mean(), ndigits=2), delta = round(delta52.iloc[-1]*100, ndigits=2))
        
        
    with c2:
        b2=st.container(border=True)
        media30dias = pd.to_datetime('today') - pd.DateOffset(days=30)
        media30 = data2.index >= media30dias
        positions1 = np.flatnonzero(media30)
        media30_filtrada = data2.iloc[positions1]['Close']
        delta30 = data2['Close'].pct_change(periods=30)
        b2.metric('Média de 30 dias', value = round(media30_filtrada.mean(), ndigits=2),delta = round((delta30.iloc[-1])*100, ndigits=3))

    with c3:
        b3=st.container(border=True)
        media9dias = pd.to_datetime('today') - pd.DateOffset(days=9)
        media9 = data2.index >= media9dias
        positions2 = np.flatnonzero(media9)
        media9_filtrada = data2.iloc[positions2]['Close']
        delta9 = data2['Close'].pct_change(periods=9)
        b3.metric('Média de 9 dias', value = round(media9_filtrada.mean(), ndigits=2), delta = round((delta9.iloc[-1])*100, ndigits=3))

    with c4:
        b4=st.container(border=True)
        price = data2['Close'].tail(1).unique()
        var_dia = data2['Close'].pct_change()
        b4.metric('Último Fechamento', value = round(float(price), ndigits=2), delta = round((var_dia.iloc[-1])*100, ndigits=3))

tab1, tab2 = st.tabs(['Gráfico', 'Exploração Personalizada'])    

with tab1:
    cards()
    plot_data(symbol, date_from, get_data(symbol, date_from))

with tab2:
    st.write('O PyGWalker transforma seus dados em aplicativos de visualização interativa e permite que você compartilhe suas análises com um clique :sunglasses:.')
    dadostab= get_data(symbol,date_from)
    def pyg_renderer() -> "StreamlitRenderer":
            tabela = pd.DataFrame(dadostab)
            tabela['Date']= tabela.index
            return StreamlitRenderer(tabela, spec="./gw_config.json", spec_io_mode="rw")
    renderizacao = pyg_renderer()
    renderizacao.explorer()




    
    