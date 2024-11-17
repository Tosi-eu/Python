# -*- coding: utf-8 -*-
"""projeto_data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17W5_X-Wt-JRQLyUSJ4ktCEN4dydzO29-
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

names = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']
df = pd.read_csv('iris.data', sep=',', names=names)
pd.set_option('display.max_rows', None)
display(df)

df.dtypes

plt.figure(figsize = (7,7))
df['Species'] = df['Species'].astype('category').cat.codes
sns.heatmap(df.corr("spearman"), annot = True, cmap = "YlGnBu")
plt.title("Mapa de Correlação das Variáveis\n", fontsize = 15)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

class Modelo():
    def __init__(self):
        self.df = None
        self.model = None
        self.X_test = None
        self.y_test = None
        self.feature_importances = None

    def CarregarDataset(self, path):
        """
        Carrega o conjunto de dados a partir de um arquivo CSV.
        """
        names = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']
        self.df = pd.read_csv(path, names=names)
        print("Dataset carregado com sucesso. Exemplo de dados:")
        print(self.df.head())

    def TratamentoDeDados(self):
        """
        Realiza o pré-processamento dos dados carregados.
        """
        if self.df is None:
            print("Nenhum dataset carregado.")
            return

        print("Dados antes do tratamento:")
        print(self.df.head())

        self.df.dropna(inplace=True)
        self.df['Species'] = self.df['Species'].astype('category').cat.codes

        print("\nDados após tratamento:")
        print(self.df.head())

        # visualização da distribuição das espécies
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(self.df['SepalLengthCm'], self.df['SepalWidthCm'], c=self.df['Species'], cmap='viridis')
        plt.colorbar(scatter, label="Espécie")
        plt.xlabel("SepalLengthCm")
        plt.ylabel("SepalWidthCm")
        plt.title("Distribuição das Espécies por Comprimento e Largura da Sépala")
        plt.show()

    def Treinamento(self):
        """
        Treina o modelo de machine learning e executa validação cruzada.
        Remove colunas com baixa importância com base nas importâncias das características.
        """
        X = self.df.drop('Species', axis=1)
        y = self.df['Species']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(X_train, y_train)

        scores = cross_val_score(self.model, X_train, y_train, cv=5)
        print(f"Desempenho inicial (validação cruzada): {scores.mean():.2f}")

        self.feature_importances = self.model.feature_importances_
        feature_names = X.columns

        threshold = 0.75  # importância mínima
        print("\nImportância das características:")
        for feature, importance in zip(feature_names, self.feature_importances):
            print(f"{feature}: {importance}")
        print()

        important_features = feature_names[self.feature_importances >= threshold]
        print("Colunas importantes:", important_features.tolist())

        X_train_filtered = X_train[important_features]
        X_test_filtered = X_test[important_features]
        self.model.fit(X_train_filtered, y_train)

        self.X_test = X_test_filtered
        self.y_test = y_test
        print("Modelo treinado com sucesso com colunas importantes.")

    def Teste(self):
        """
        Avalia o desempenho do modelo treinado nos dados de teste.
        """
        if self.model is None:
            print("Modelo não foi treinado.")
            return

        y_pred = self.model.predict(self.X_test)

        # Métricas de desempenho
        acuracia = accuracy_score(self.y_test, y_pred)
        print(f"Acurácia: {acuracia:.2f}")
        print("Relatório de Classificação:")
        print(classification_report(self.y_test, y_pred))

    def Train(self):
        """
        Função principal para o fluxo de treinamento do modelo.
        """
        self.CarregarDataset("iris.data")
        self.TratamentoDeDados()
        self.Treinamento()
        self.Teste()

model = Modelo()
model.Train()