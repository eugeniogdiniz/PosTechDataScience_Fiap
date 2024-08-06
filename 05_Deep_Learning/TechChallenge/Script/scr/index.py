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

    html_content = f.load_html(r'C:\Users\AMD\Documents\Projetos\PosTechDataScience_Fiap\05_Deep_Learning\TechChallenge\Script\scr\readme.html')
    css_content = f.load_css(r'C:\Users\AMD\Documents\Projetos\PosTechDataScience_Fiap\05_Deep_Learning\TechChallenge\Script\scr\styles.css')
    html_with_css = f"""
    <style>{css_content}</style>
    {html_content}
    """    
    components.html(html_with_css, height=800, scrolling=True)

elif paginaSelecionada == 'Aplicação':
    # Carregar o modelo
    model = joblib.load(r'C:\Users\AMD\Documents\Projetos\PosTechDataScience_Fiap\05_Deep_Learning\TechChallenge\Script\scr\random_forest_model.pkl')

    # Título do aplicativo
    st.title("Previsão de Bolsista 2022")

    # Carregar o conjunto de dados para predição
    uploaded_file = st.file_uploader("Escolha um arquivo CSV para upload", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Dados carregados:")
        st.write(data)
        
        # Verifica se a coluna BOLSISTA_2022 existe e a remove para predição
        if 'BOLSISTA_2022' in data.columns:
            data = data.drop('BOLSISTA_2022', axis=1)
        
        # Faz predições
        predictions = model.predict(data)
        
        # Mostra os resultados
        st.write("Previsões:")
        data['BOLSISTA_2022_PRED'] = predictions
        st.write(data)
        
        # Baixar os resultados como CSV
        st.download_button(
            label="Baixar resultados como CSV",
            data=data.to_csv(index=False).encode('utf-8'),
            file_name='predicoes.csv',
            mime='text/csv',
        )

    def predict_chance(data):
        # Criar um DataFrame a partir dos dados de entrada
        df = pd.DataFrame([data], columns=[
            'INDE_2022', 'CG_2022', 'CF_2022', 'CT_2022', 'IAA_2022', 
            'IEG_2022', 'IPS_2022', 'IDA_2022', 'NOTA_PORT_2022', 'NOTA_MAT_2022', 
            'NOTA_ING_2022', 'QTD_AVAL_2022', 'IPP_2022', 'INDICADO_BOLSA_2022', 
            'PONTO_VIRADA_2022', 'IPV_2022', 'IAN_2022', 'Ametista', 'Quartzo', 
            'Topazio', 'Agata'
        ])
        prediction = model.predict(df)
        return prediction[0]

    # Título do aplicativo
    st.title('Previsão de Entrada na Faculdade')

    # Criação do formulário
    with st.form(key='student_form'):
        st.header('Informações do Aluno')

        INDE_2022 = st.number_input('INDE_2022', format='%.2f')
        CG_2022 = st.number_input('CG_2022', format='%.2f')
        CF_2022 = st.number_input('CF_2022', format='%.2f')
        CT_2022 = st.number_input('CT_2022', format='%.2f')
        IAA_2022 = st.number_input('IAA_2022', format='%.2f')
        IEG_2022 = st.number_input('IEG_2022', format='%.2f')
        IPS_2022 = st.number_input('IPS_2022', format='%.2f')
        IDA_2022 = st.number_input('IDA_2022', format='%.2f')
        NOTA_PORT_2022 = st.number_input('NOTA_PORT_2022', format='%.2f')
        NOTA_MAT_2022 = st.number_input('NOTA_MAT_2022', format='%.2f')
        NOTA_ING_2022 = st.number_input('NOTA_ING_2022', format='%.2f')
        QTD_AVAL_2022 = st.number_input('QTD_AVAL_2022', format='%.2f')
        IPP_2022 = st.number_input('IPP_2022', format='%.2f')
        INDICADO_BOLSA_2022 = st.number_input('INDICADO_BOLSA_2022', format='%.0f')
        PONTO_VIRADA_2022 = st.number_input('PONTO_VIRADA_2022', format='%.0f')
        IPV_2022 = st.number_input('IPV_2022', format='%.2f')
        IAN_2022 = st.number_input('IAN_2022', format='%.2f')
        Ametista = st.number_input('Ametista', format='%.0f')
        Quartzo = st.number_input('Quartzo', format='%.0f')
        Topazio = st.number_input('Topazio', format='%.0f')
        Agata = st.number_input('Agata', format='%.0f')

        submit_button = st.form_submit_button('Prever')

    # Exibir resultado
    if submit_button:
        input_data = {
            'INDE_2022': INDE_2022,
            'CG_2022': CG_2022,
            'CF_2022': CF_2022,
            'CT_2022': CT_2022,
            'IAA_2022': IAA_2022,
            'IEG_2022': IEG_2022,
            'IPS_2022': IPS_2022,
            'IDA_2022': IDA_2022,
            'NOTA_PORT_2022': NOTA_PORT_2022,
            'NOTA_MAT_2022': NOTA_MAT_2022,
            'NOTA_ING_2022': NOTA_ING_2022,
            'QTD_AVAL_2022': QTD_AVAL_2022,
            'IPP_2022': IPP_2022,
            'INDICADO_BOLSA_2022': INDICADO_BOLSA_2022,
            'PONTO_VIRADA_2022': PONTO_VIRADA_2022,
            'IPV_2022': IPV_2022,
            'IAN_2022': IAN_2022,
            'Ametista': Ametista,
            'Quartzo': Quartzo,
            'Topazio': Topazio,
            'Agata': Agata
        }

        result = predict_chance(input_data)

        if result == 1:
            st.success('O aluno tem uma boa chance de ser admitido na faculdade.')
        else:
            st.warning('O aluno tem uma chance menor de ser admitido na faculdade.')
