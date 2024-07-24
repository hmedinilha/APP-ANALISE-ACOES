
import streamlit as st


appat = st.Page("apps/1_analise_tecnica.py", title="Analise Tecnica", icon=':material/candlestick_chart:')
appaf= st.Page("apps/2_fundamento_acoes.py", title="Analise Fundamentalista", icon=':material/book_3:')
apphome = st.Page("apps/3_home.py", title = 'Inicial', icon=':material/home:', default=True)




pg = st.navigation(pages={'Home':[apphome],"Aplicativos":[appat,appaf] })
st.set_page_config(layout='wide', page_title=pg.title, page_icon=pg.icon)
st.sidebar.text(f'APP ativo: \n'
                f'{pg.title}')
st.sidebar.caption('_Desenvolvido_ _por_ _Hernandes Medinilha_ :link: _https://www.linkedin.com/in/hernandes-medinilha/_')

pg.run()






