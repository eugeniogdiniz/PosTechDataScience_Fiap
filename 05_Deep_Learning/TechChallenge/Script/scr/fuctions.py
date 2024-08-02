import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
class functions:
    def __init__(self):
        self
    
    def filter_columns(df, filters: list): # adiciono no array o padrão que existe nas colunas e que não quero que tenha na saída final
        selected_columns = [True] * len(df.columns)  # Inicializa todas as colunas como True
        for index, column in enumerate(df.columns):
            if any(filter in column for filter in filters): selected_columns[index] = False
        return df[df.columns[selected_columns]]

    def cleaning_dataset(df):
        _df = df.dropna(subset=df.columns.difference(['NOME']), how='all') # executa o dropna para todas as colunas sem visualizar a coluna NOME
        _df = _df[~_df.isna().all(axis=1)] # remove linhas com apenas NaN, se tiver algum dado na linha não remove
        return _df

    def plot_exact_counter(size, x, y, df) -> None:
        plt.figure(figsize=size)
        barplot = plt.bar(y.index, y.values)
        plt.xlabel(x)
        plt.ylabel('Count')

        for index, value in enumerate(y.values):
            plt.text(index, value, round(value, 2), color='black', ha="center")

        plt.show()

    def dummie_int(df, list_columns):
        _df = df
        for columns in list_columns:
            _df[columns] = _df[columns].replace(['Sim', 'Não'], [1,0])
        return _df