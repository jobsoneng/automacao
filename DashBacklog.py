import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout= 'wide')
st.title('Gestão Backlog Infraestrutura - 📋')


# Carrega a planilha
arquivo = "Acompanhamento_Backlog_Infra.xlsx"
df = pd.read_excel(arquivo, engine='openpyxl')

#rotas = ['GERAL', 'BA-CAPITAl', 'BA-NORTE', 'BA-OESTE', 'BA-SUL']

st.sidebar.title('Filtros')
#rotas = st.sidebar.selectbox('ROTA', rotass)

#if rotas == 'GERAL':
#    regiao = ''

#query_string = {'ROTA':rotas.lower()}
#response = requests.get(df, params= query_string)

filtro_rotas = st.sidebar.multiselect('ROTA', df['ROTA'].unique())
if filtro_rotas:
    df = df[df['ROTA'].isin(filtro_rotas)]

# DataFrames Intermediuarios

Total_TA_Tipo_Planta =  pd.DataFrame(df.groupby('TIPO_SITE', as_index=False).agg(Total_TA=('TIPO_SITE','count')).sort_values(by='Total_TA', ascending=True))
Total_TA_Responsavel =  pd.DataFrame(df.groupby('RESPONSAVEL', as_index=False).agg(Total_TA2=('RESPONSAVEL','count')))

#df = df[df["UF"] == "BA"]
df_Grupo_Sharing  = df[df["RESPONSAVEL"] == "SHARING"] 
Total_TA_Grupo_Sharing =  pd.DataFrame(df_Grupo_Sharing.groupby('GRUPO_REPONSAVEL', as_index=False).agg(Total_TA3=('GRUPO_REPONSAVEL','count')))

# Graficos 01
fig= px.bar(
    Total_TA_Tipo_Planta,
    x = 'TIPO_SITE', 
    y = Total_TA_Tipo_Planta['Total_TA'], 
    title = "Tipo de Planta x Total TAs",
    text_auto='.2s'
)
fig.update_traces(
    textposition='inside', 
    textfont_size=20, 
    marker=dict(color="purple")  # Cor única para todas as barras
 )

# Alterando o título do eixo X
fig.update_layout(
    title_font={
        'size': 24  # Tamanho da fonte
    },
    xaxis_title="",
    yaxis_title=""
    
)

# Personalizando os eixos
fig.update_layout(
    xaxis=dict(
        tickfont=dict(color='black', size=20),
        
    ),
    yaxis=dict(
        showticklabels=False  # Apagar os valores do eixo Y
    )
)

# Graficos 02
fig2= px.bar(
    Total_TA_Responsavel,
    x = 'RESPONSAVEL', 
    y = Total_TA_Responsavel['Total_TA2'], 
    title = "Responsável x Total TAs",
    text_auto='.2s'
)
fig2.update_traces(
    textposition='inside', 
    textfont_size=20, 
    marker=dict(color="purple")  # Cor única para todas as barras
 )

# Alterando o título do eixo X
fig2.update_layout(
    title_font={
        'size': 24  # Tamanho da fonte
    },
    xaxis_title="",
    yaxis_title=""
    
)

# Personalizando os eixos
fig2.update_layout(
    xaxis=dict(
        tickfont=dict(color='black', size=20),
        
    ),
    yaxis=dict(
        showticklabels=False  # Apagar os valores do eixo Y
    )
)



#fig2= px.bar(Total_TA_Responsavel,x = 'RESPONSAVEL', y = Total_TA_Responsavel['Total_TA2'], title = "Total TAs x Respomsável")
fig3= px.bar(Total_TA_Grupo_Sharing, x = 'GRUPO_REPONSAVEL', y = Total_TA_Grupo_Sharing ['Total_TA3'], title = "Total TAs x Sharing")


tabs = st.tabs(["GERAL", "CAMPO N1", "Gabinete Sharing"])


#aba1, aba2, aba3 = st.tabs(['GERAL', 'CAMPO N1', 'Gabinete Sharing'])


with tabs[0]: 
    c1, c2, c3, c4, c5, c6 = st.columns((6),border=True)
    with c1:
        c1 = st.metric('TOTAL TAS', df.shape[0])
    with c2:
        c2 = st.metric('BA-CAPITAL', df[(df['ROTA']=="BA-CAPITAL") & (df['TIPO_PLANTA']=="Móvel")].shape[0])
    with c3:
        c3 = st.metric('BA-NORTE', df[(df['ROTA']=="BA-NORTE") & (df['TIPO_PLANTA']=="Móvel")].shape[0])
    with c4:
        c4 = st.metric('BA-OESTE', df[(df['ROTA']=="BA-OESTE") & (df['TIPO_PLANTA']=="Móvel")].shape[0])
    with c5:
        c5 = st.metric('BA-SUL', df[(df['ROTA']=="BA-SUL") & (df['TIPO_PLANTA']=="Móvel")].shape[0])
    with c6:
        c6 = st.metric('BA-FIXA', df[df['TIPO_PLANTA']=="Fixa Integrada V2"].shape[0])

    col1, col2 = st.columns((2))
    with col1:
        st.plotly_chart(fig, use_container_width = True)
    with col2:
        st.plotly_chart(fig2, use_container_width = True)

    st.write(Total_TA_Tipo_Planta)
        


with tabs[1]: 
    c1, c2, c3, c4, c5, c6 = st.columns((6))
    with c1:
        c1 = st.metric('ICOMON', df[(df['RESPONSAVEL']=="ICOMON")].shape[0])
    with c2:
        c1 = st.metric('VIVO', df[(df['RESPONSAVEL']=="VIVO N1")].shape[0])   

with tabs[2]:
    c1, c2 = st.columns((2))
    with c1:
        c1 = st.metric('GABINETE SHARING', df[(df['RESPONSAVEL']=="SHARING")].shape[0])
    with c2:
        st.plotly_chart(fig3, use_container_width = True)
        
        
    st.write(df_Grupo_Sharing)
