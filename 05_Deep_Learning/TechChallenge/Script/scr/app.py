import streamlit as st
import joblib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Para machine learning
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
# Para deep learning

from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
#Para aplicar o ARIMA:
from statsmodels.tsa.stattools import adfuller          

############################# Streamlit ############################
st.markdown('<style>div[role="listbox"] ul{background-color: #6e42ad}; </style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; '> Modelo Preditivo - Preço por barril do petróleo bruto Brent (FOB)</h1>", unsafe_allow_html = True)

st.warning('''
"Preço por barril do petróleo bruto Brent (FOB)" refere-se ao valor de venda do petróleo bruto Brent por barril, onde FOB significa "Free On Board", 
que é uma cláusula de comércio internacional que indica que o vendedor é responsável por todos os custos associados à entrega do produto até o ponto de embarque.

O petróleo bruto Brent é um tipo de petróleo cru extraído do Mar do Norte e é usado como uma referência para precificar muitos tipos de petróleo ao redor do mundo. 
O preço do petróleo bruto Brent é influenciado por uma série de fatores, incluindo a oferta e demanda global, eventos geopolíticos, políticas dos países produtores de 
petróleo, condições econômicas e muito mais.]
''')

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

# Função para carregar o conteúdo HTML de um arquivo
def load_html(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Carregar o HTML personalizado
custom_html = load_html('05_Deep_Learning\TechChallenge\Script\scr\custom_styles.html')

# Exibir o HTML no Streamlit
st.markdown(custom_html, unsafe_allow_html=True)

# Exemplo de uso dos estilos definidos no HTML
st.markdown('<h1 class="custom-title">Título Personalizado</h1>', unsafe_allow_html=True)
st.markdown('<p class="custom-paragraph">Este é um parágrafo com estilo personalizado.</p>', unsafe_allow_html=True)