from fuctions import functions as f
import streamlit as st
import pandas as pd
pd.set_option('display.max_columns', None)

csv_url = 'https://github.com/eugeniogdiniz/PosTechDataScience_Fiap/blob/main/05_Deep_Learning/arquivos/PEDE_PASSOS_DATASET_FIAP.csv'
df = pd.read_csv(csv_url, delimiter=';')
passos_magicos_22 = f.filter_columns(df, ['2020', '2021'])
passos_magicos_22 = f.cleaning_dataset(passos_magicos_22)
passos_magicos_22 = f.dummie_int(passos_magicos_22, ['BOLSISTA_2022', 'INDICADO_BOLSA_2022', 'PONTO_VIRADA_2022'])
drop_columns = ['DESTAQUE_IEG_2022', 'DESTAQUE_IDA_2022', 'DESTAQUE_IPV_2022', 'REC_AVA_1_2022',
                'REC_AVA_2_2022', 'REC_AVA_3_2022', 'REC_AVA_4_2022', 'NIVEL_IDEAL_2022', 'NOME', 'FASE_2022', 'TURMA_2022', 'ANO_INGRESSO_2022']
passos_magicos_22.drop(columns=drop_columns, inplace=True)
passos_magicos_22 = pd.get_dummies(passos_magicos_22, columns=['PEDRA_2022'], dtype=int)
passos_magicos_22.rename(columns={
    'PEDRA_2022_Ametista':'Ametista',
    'PEDRA_2022_Quartzo':'Quartzo',
    'PEDRA_2022_Topázio':'Topazio',
    'PEDRA_2022_Ágata':'Agata'
}, inplace = True)


st.sidebar.title('Páginas')
paginaSelecionada = st.sidebar.selectbox('Selecione a Página', ['Passos Mágicos - Origem e Problema', 'Solução'])

if paginaSelecionada == 'Passos Mágicos - Origem e Problema':
    # CSS Customizado para Justificação de Texto
    css_code = """
    <style>
    .justified-text {
        text-align: justify;
        font-size: 18px;
    }
    </style>
    <style>
    .centered-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
    }
    </style>
    """

    # HTML com Classe de Justificação
    html_code = """
    <div class='justified-text'>
        <h1>História da Associação Passos Mágicos</h1>
        <p>
        A Associação Passos Mágicos tem uma trajetória de 30 anos de atuação, trabalhando na transformação da vida de crianças e jovens de baixa renda, levando-os a melhores oportunidades de vida. A transformação, idealizada por Michelle Flues e Dimetri Ivanoff, começou em 1992, atuando dentro de orfanatos no município de Embu-Guaçu.
        </p>
        <img src="https://passosmagicos.org.br/wp-content/uploads/2020/10/Passos-magicos-icon-cor.png" alt="Passos Mágicos" id="logo" data-height-percentage="71" class="centered-image"/> 
        <p>
        Em 2016, depois de anos de atuação, decidiram ampliar o programa para que mais jovens tivessem acesso a essa fórmula mágica para transformação que inclui: educação de qualidade, auxílio psicológico/psicopedagógico, ampliação de sua visão de mundo e protagonismo. Passaram então a atuar como um projeto social e educacional, criando assim a Associação Passos Mágicos.
        </p>
        <h2>O que fazemos?</h2>
        <p>
        Oferecemos um programa de educação de qualidade para crianças e jovens do município de Embu-Guaçu. Nossa missão é transformar a vida de jovens e crianças, oferecendo ferramentas para levá-los a melhores oportunidades de vida.
        </p>
        <h2>Missão e Visão</h2>
        <p>
        Nossa visão é viver em um Brasil no qual todas as crianças e jovens têm iguais oportunidades para realizarem seus sonhos e são agentes transformadores de suas próprias vidas. 
        </p>
        <h2>Proposta do grupo: Proposta Preditiva<h2>
        <p>
        Proposta preditiva: Criar um modelo preditivo para prever o comportamento do estudante com base em algumas variáveis que podem ser cruciais para a identificação do desenvolvimento do estudante.
        </p>
    </div>
    """
    # Aplicar CSS e HTML no Streamlit
    st.markdown(css_code + html_code, unsafe_allow_html=True)

elif paginaSelecionada == 'Solução':
    st.title('Estilização com CSS no Streamlit')

    html_code = """
    <style>
    .custom-table {
        width: 100%;
        border-collapse: collapse;
    }
    .custom-table th, .custom-table td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }
    .custom-table th {
        background-color: #f2f2f2;
    }
    </style>
    <table class="custom-table">
    <tr>
        <th>Nome</th>
        <th>Idade</th>
    </tr>
    <tr>
        <td>Maria</td>
        <td>30</td>
    </tr>
    <tr>
        <td>João</td>
        <td>25</td>
    </tr>
    </table>
    """
    st.markdown(html_code, unsafe_allow_html=True)
