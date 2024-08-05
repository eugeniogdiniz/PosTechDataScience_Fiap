import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class functions:
    @staticmethod
    def filter_columns(df, filters: list): 
        selected_columns = [True] * len(df.columns)  # Inicializa todas as colunas como True
        for index, column in enumerate(df.columns):
            if any(filter in column for filter in filters):
                selected_columns[index] = False
        return df[df.columns[selected_columns]]

    @staticmethod
    def cleaning_dataset(df):
        _df = df.dropna(subset=df.columns.difference(['NOME']), how='all') # executa o dropna para todas as colunas sem visualizar a coluna NOME
        _df = _df[~_df.isna().all(axis=1)] # remove linhas com apenas NaN, se tiver algum dado na linha não remove
        return _df

    @staticmethod
    def plot_exact_counter(size, x, y, df) -> None:
        plt.figure(figsize=size)
        barplot = plt.bar(y.index, y.values)
        plt.xlabel(x)
        plt.ylabel('Count')

        for index, value in enumerate(y.values):
            plt.text(index, value, round(value, 2), color='black', ha="center")

        plt.show()

    @staticmethod
    def dummie_int(df, list_columns):
        _df = df.copy()  # Adiciona cópia para evitar a modificação direta do DataFrame original
        for column in list_columns:
            _df[column] = _df[column].replace(['Sim', 'Não'], [1,0])
        return _df
