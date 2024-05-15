import streamlit as st
import joblib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

import pandas as pd
import torch
import torch.nn as nn
from torch.optim import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

# Para machine learning
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
# Para deep learning
from keras.models import Sequential
from keras.layers import LSTM,Dense,Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import MeanSquaredError
from keras.models import load_model
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

# Importando os dados do IBOVESPA para o modelo
alpha = 0.09   # Fator de suavização

df = pd.read_csv(r'C:\Users\EugênioLenineGueiros\OneDrive - TPF-EGC\Documentos\FIAP\base_ipea.csv', sep = ';')
df['data'] = pd.to_datetime(df['data']) #realizando a conversão da data para formato datetime
df['preco'] = df['preco'].str.replace(',', '.').astype(float) #realizando a conversão da data para tipo float
df = df.sort_values(by='data', ascending=True)
df['Smoothed_Close'] = df['preco'].ewm(alpha=alpha, adjust=False).mean()
df.drop(columns=['preco'], inplace=True)

st.table(df.head())
st.table(df.tail())
st.write("Fonte: http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view ")

close_data = df['Smoothed_Close'].values
close_data = close_data.reshape(-1,1) #transformar em array

scaler = MinMaxScaler(feature_range=(0, 1))
scaler = scaler.fit(close_data)
close_data = scaler.transform(close_data)

split_percent = 0.80
split = int(split_percent*len(close_data))

close_train = close_data[:split]
close_test = close_data[split:]

date_train = df['data'][:split]
date_test = df['data'][split:]

# Gerar sequências temporais para treinamento e teste em um modelo de aprendizado de máquina

look_back = 5

train_generator = TimeseriesGenerator(close_train, close_train, length=look_back, batch_size=20)
test_generator = TimeseriesGenerator(close_test, close_test, length=look_back, batch_size=1)

with open('lstm_model.joblib', 'rb') as file:
    modelo = joblib.load(file)

# 1. Fazer previsões usando o conjunto de teste
test_predictions = modelo.predict(test_generator)

# 2. Inverter qualquer transformação aplicada aos dados
test_predictions_inv = scaler.inverse_transform(test_predictions.reshape(-1, 1))
test_actuals_inv = scaler.inverse_transform(np.array(close_test).reshape(-1, 1))

# Ajuste as dimensões
test_actuals_inv = test_actuals_inv[:len(test_predictions_inv)]

# Calcular o MAPE
mape = np.mean(np.abs((test_actuals_inv - test_predictions_inv) / test_actuals_inv)) * 100

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
prediction = modelo.predict(test_generator)

close_train = close_train.reshape((-1))
close_test = close_test.reshape((-1))
prediction = prediction.reshape((-1))

trace1 = go.Scatter(
    x = date_train,
    y = close_train,
    mode = 'lines',
    name = 'data'
)
trace2 = go.Scatter(
    x = date_test,
    y = prediction,
    mode = 'lines',
    name = 'Prediction'
)
trace3 = go.Scatter(
    x = date_test,
    y = close_test,
    mode='lines',
    name = 'Ground Truth'
)
layout = go.Layout(
    title = "Predições da Preço do Petroleo",
    xaxis = {'title' : "Data"},
    yaxis = {'title' : "Fechamento"}
)
fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
st.plotly_chart(fig, width=1200, height=1000)
st.write(f"##### Sobre o modelo:")
st.warning('''
Este estudo propõe um modelo baseado em redes neurais recorrentes (LSTM) para prever o preço do petróleo bruto Brent (FOB). Os dados são pré-processados e 
divididos em conjuntos de treinamento e teste. O modelo é treinado com os dados de treinamento e avaliado com os dados de teste, utilizando métricas como MAPE, 
MSE e RMSE. Os resultados são visualizados em um gráfico interativo. Conclui-se que o modelo LSTM apresenta potencial na previsão de preços do petróleo, mas requer 
contínua avaliação e aprimoramento.
''')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------



# Avaliando o modeloo nos dados de teste


# O RMSE é a raiz quadrada do MSE (Mean Squared Error), que é a média dos quadrados das diferenças entre as previsões do modeloo e os valores reais.


# ----------------------------------------------------------------------------------------------------------------------------------------------------------
st.write(f"##### ANALISANDO O MAPE, MSE e RMSE")

st.write(f"###### MAPE: {mape:.2f}%")
st.warning('''
MAPE, abreviação para Erro Percentual Absoluto Médio, é uma métrica comumente utilizada para avaliar a precisão de modelos de previsão. Nesse contexto, um 
MAPE de 1.72% significa que, em média, as previsões do modelo estão errando aproximadamente 1.72% em relação aos valores reais.
''')

mse = modelo.evaluate(test_generator, verbose=1)
st.write(f"###### Erro Quadrático Médio (MSE): {mse[0]:.5f}")
st.warning('''
Erro Quadrático Médio (MSE) é outra métrica de avaliação de modelos, que calcula a média dos quadrados das diferenças entre as previsões do modelo e os valores 
reais. No caso apresentado, o MSE é de 0.00001, o que indica um baixo erro quadrático médio, sugerindo que as previsões estão próximas dos valores reais.
''')

rmse_value = np.sqrt(mse[0])
st.write(f"###### RMSE: {rmse_value:.5f}")
st.warning('''
RMSE, ou Raiz do Erro Quadrático Médio, é a raiz quadrada do MSE. É uma medida comumente usada para expressar o desvio padrão das diferenças entre previsões e 
valores reais. No contexto do texto, o valor do RMSE é 0.00231, o que significa que, em média, as previsões do modelo estão desviando cerca de 0.00231 
unidades do valor real.
''')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# Inicio da Analise
st.write('### UTILIZANDO O MODELO')
st.write('#### Selecione as datas que você pretende utilizar para analise')

st.write('##### Selecione a data que o modelo deve utilizar para iniciar sua analise')
date_in_input = st.date_input("Selecionar apenas datas a partir de:", value=None, key="date_in")

# Fim da Analise
st.write('##### Selecione uma data que corresponda até onde você quer que o modelo prediza')
date_fin_input = st.date_input("Selecionar apenas datas a partir de:", value=None, key="date_fim")

close_data = close_data.reshape((-1))

# Função para prever os próximos 'num_prediction' pontos da série temporal
# Utiliza o modelo treinado para prever cada ponto sequencialmente
# A cada iteração, adiciona a previsão à lista 'prediction_list'

def predict(num_prediction, modelo):
    prediction_list = close_data[-look_back:]

    for _ in range(num_prediction):
        x = prediction_list[-look_back:]
        x = x.reshape((1, look_back, 1))
        out = modelo.predict(x)[0][0]
        prediction_list = np.append(prediction_list, out)
    prediction_list = prediction_list[look_back-1:]

    return prediction_list

# Função para gerar as datas dos próximos 'num_prediction' dias
# Assume que o DataFrame 'df' possui uma coluna 'Date' contendo as datas

def predict_dates(num_prediction):
    last_date = df['data'].values[-1]
    prediction_dates = pd.date_range(last_date, periods=num_prediction+1).tolist()
    return prediction_dates

# Concatenando os DataFrames usando concat

if date_in_input and date_fin_input != None:
    data_max = pd.Timestamp(max(df['data']))
    date_fin_input_timestamp = pd.Timestamp(date_fin_input)
    data_diff = date_fin_input_timestamp - data_max
    num_prediction = data_diff.days #definição dos próximos dias
    forecast = predict(num_prediction, modelo) #resultado de novos dias
    forecast_dates = predict_dates(num_prediction)

    df_ltsm_suav = pd.DataFrame(df)
    df_past = df_ltsm_suav[['data','Smoothed_Close']]
    df_past.rename(columns={'Smoothed_Close': 'Actual'}, inplace=True)         #criando nome das colunas
    df_past['data'] = pd.to_datetime(df_past['data'])                          #configurando para datatime
    df_past['Forecast'] = np.nan                                               #Preenchendo com NAs
    df_past['Forecast'].iloc[-1] = df_past['Actual'].iloc[-1]

    # Faz a transformação inversa das predições
    forecast = forecast.reshape(-1, 1) #reshape para array
    forecast = scaler.inverse_transform(forecast)

    df_future = pd.DataFrame(columns=['data', 'Actual', 'Forecast'])
    df_future['data'] = forecast_dates
    df_future['Forecast'] = forecast.flatten()
    df_future['Actual'] = np.nan

    frames = [df_past, df_future]
    results = pd.concat(frames, ignore_index=True).set_index('data')
    result_final =  results.loc[date_in_input:]

    plot_data = [
        go.Scatter(
            x=result_final.index,
            y=result_final['Actual'],
            name='actual'
        ),
        go.Scatter(
            x=result_final.index,
            y=result_final['Forecast'],
            name='prediction'
        )
    ]

    plot_layout = go.Layout(
            title='Forecast Petroleo Brent'
        )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    st.plotly_chart(fig, width=1200, height=1000)
else:
    st.write('Aguardando datas para realizar a analise')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
