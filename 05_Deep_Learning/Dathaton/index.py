from fuctions import functions as f
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib

pd.set_option('display.max_columns', None)

csv_url = 'https://raw.githubusercontent.com/eugeniogdiniz/PosTechDataScience_Fiap/main/05_Deep_Learning/arquivos/PEDE_PASSOS_DATASET_FIAP.csv'
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
paginaSelecionada = st.sidebar.selectbox('Selecione a Página', ['Passos Mágicos - Origem e Problema', 'Solução Proposta', 'Aplicação'])

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

elif paginaSelecionada == 'Solução Proposta':

    # Título do aplicativo
    st.title("Solução Proposta - Um estudo na Passos Mágicos")

    html_content = f.load_html('05_Deep_Learning/Dathaton/readme.html')
    css_content = f.load_css('05_Deep_Learning/Dathaton/styles.css')
    html_with_css = f"""
    <style>{css_content}</style>
    {html_content}
    """    
    components.html(html_with_css, height=800, scrolling=True)

elif paginaSelecionada == 'Aplicação':
    # Carregar o modelo
    #model = joblib.load('05_Deep_Learning/Dathaton/modelo_xgboost.pkl')
    model = joblib.load('05_Deep_Learning/Dathaton/random_forest_model.pkl')

    # Título do aplicativo
    st.title("Previsão de Bolsista 2022")

    # Título do aplicativo
    st.title('Download da Planilha Modelo')

    # Criar workbook modelo
    sample_workbook = f.create_sample_workbook()

    # Botão para download do Excel
    st.download_button(
        label="Baixar Planilha Modelo",
        data=sample_workbook,
        file_name='planilha_modelo_lista.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.write("Baixe a planilha modelo acima, preencha com as informações dos alunos e faça o upload para prever a chance de entrar na faculdade.")

    # Carregar o conjunto de dados para predição
    uploaded_file = st.file_uploader("Escolha um arquivo Excel para upload", type="xlsx")

    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        st.write("Dados carregados:")
        st.write(data)
        
        # Verifica se a coluna BOLSISTA_2022 existe e a remove para predição
        if 'INDICADO_BOLSA_2022' in data.columns:
            data = data.drop('INDICADO_BOLSA_2022', axis=1)

        # Faz predições
        predictions = model.predict(data)
        
        # Mostra os resultados
        st.write("Previsões:")
        data['INDICADO_BOLSA_2022_PRED'] = predictions
        st.write(data)
        
        # Baixar os resultados como CSV
        st.download_button(
            label="Baixar resultados como Excel",
            data=data.to_csv(index=False).encode('utf-8'),
            file_name='predicoes.xlsx',
            mime='text/xlsx',
        )

    def predict_chance(data):
        # Criar um DataFrame a partir dos dados de entrada
        df = pd.DataFrame([data], columns=[
        'IAA_2022', 'IEG_2022', 'IPS_2022', 'IDA_2022', 'NOTA_PORT_2022',
        'NOTA_MAT_2022', 'NOTA_ING_2022', 'IPP_2022', 'INDICADO_BOLSA_2022'
        ])
        prediction = model.predict(df)
        return prediction[0]

    # Título do aplicativo
    st.title('Previsão de Entrada na Faculdade')

    # Criação do formulário
    with st.form(key='student_form'):
        st.header('Informações do Aluno')

    IAA_2022 = st.number_input('IAA_2022', format='%.2f')
    IEG_2022 = st.number_input('IEG_2022', format='%.2f')
    IPS_2022 = st.number_input('IPS_2022', format='%.2f')
    IDA_2022 = st.number_input('IDA_2022', format='%.2f')
    NOTA_PORT_2022 = st.number_input('NOTA_PORT_2022', format='%.2f')
    NOTA_MAT_2022 = st.number_input('NOTA_MAT_2022', format='%.2f')
    NOTA_ING_2022 = st.number_input('NOTA_ING_2022', format='%.2f')
    IPP_2022 = st.number_input('IPP_2022', format='%.2f')
    
    submit_button = st.form_submit_button('Prever')

    # Exibir resultado
    if submit_button:
        input_data = {
            'IAA_2022': IAA_2022,
            'IEG_2022': IEG_2022,
            'IPS_2022': IPS_2022,
            'IDA_2022': IDA_2022,
            'NOTA_PORT_2022': NOTA_PORT_2022,
            'NOTA_MAT_2022': NOTA_MAT_2022,
            'NOTA_ING_2022': NOTA_ING_2022,
            'IPP_2022': IPP_2022
        }

        result = predict_chance(input_data)

    if result == 1:
        st.success('O aluno tem uma boa chance de ser admitido na faculdade.')
    else:
        st.warning('O aluno tem uma chance menor de ser admitido na faculdade.')