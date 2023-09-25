# se importan las librerías que se utilizarán

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
from wordcloud import WordCloud
from spacy.lang.es.stop_words import STOP_WORDS

# Ignorar Warnings
import warnings
warnings.filterwarnings('ignore')

sys.path.append("../..")
import utility.plot_settings


class PlotData():
    
    def __init__(self) -> None:
        pass
    
    def importar_manipular_data(self,PATH1='../data/data_procesada/model_process.csv',PATH2='../data/data_procesada/twitts.csv'):
        df1 = pd.read_csv(PATH1)
        df2 = pd.read_csv(PATH2)
        sentimiento=df1['sentimiento']
        
        df=pd.concat([df2,sentimiento],axis=1)
        # cambio de tipo de variable de Objeto a Fecha
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df
    
    def _exportar_figura(self, filename):

        path = f"../visualzaciones/"

        if os.path.exists(path):
            plt.savefig(path + filename + ".png", bbox_inches="tight")

        if not os.path.exists(path):
            os.makedirs(path)
            plt.savefig(path + filename + ".png", bbox_inches="tight")

        print(f"Successfully export {filename}")

    def countplot(self,data,x):
        data=data.sort_values(x)
        plt.figure(figsize=(11,5))
        plt.title(f'Ditribución por {x}',fontsize=16)
        plt.rcParams['figure.facecolor'] = 'White'
        plt.xticks(rotation=30)
        plot = sns.histplot(data=data,x=x)
        # Export figure
        self._exportar_figura(filename=f'Countplot - {x}')

    def lineplot(self,data, y):
        fig, ax = plt.subplots(figsize=(11,5))
        ax = sns.lineplot(data=data, x='Fecha', y=y, ci=None)
        ax.set_title(f'Retweet por {y}', fontsize=16)
        ax.set_xticklabels(labels=['2021-01','2021-02','2021-03','2021-04','2021-05','2021-06','2021-07'])
        ax.set_xlabel('Fecha')
        ax.set_ylabel(y)
        # Export figure
        self._exportar_figura(filename=f'Time Series - {y}')

    def countplot_hue(self,data,x):
        data=data.sort_values(x)
        plt.figure(figsize=(11,5))
        plt.title(f'Ditribución por {x}',fontsize=16)
        plt.rcParams['figure.facecolor'] = 'white'
        plt.xticks(rotation=30)
        plot = sns.histplot(data=data,x=x,hue='sentimiento')
        # Export figure
        self._exportar_figura(filename=f'Countplot - {x} por Sentimiento')

    def lineplot_hue(self,data, y):
        fig, ax = plt.subplots(figsize=(11,5))
        ax = sns.lineplot(data=data, x='Fecha', y=y, ci=None,hue='sentimiento')
        ax.set_title(f'Retweet por {y}', fontsize=16)
        ax.set_xticklabels(labels=['2021-01','2021-02','2021-03','2021-04','2021-05','2021-06','2021-07'])
        ax.set_xlabel('Fecha')
        ax.set_ylabel(y)
        # Export figure
        self._exportar_figura(filename=f'Time series - {y}  por Sentimineto')
        
    def word_cloud(self,texto):
        stop = list(STOP_WORDS)
        wc=WordCloud(stopwords=stop).generate(''.join(texto))
        plt.figure(figsize=[20,10])
        plt.imshow(wc,interpolation='bilinear')
        plt.axis('off')
        plt.show()
        # Export figure
        self._exportar_figura(filename='Nube de Palabras - COVID19')


if __name__ == '__main__':
    test1 = PlotData()
    df=test1.importar_manipular_data()
    test1.word_cloud(df['Texto'])
    test1.countplot(data=df,x='Mes')
    test1.countplot_hue(df,x='Mes')
    test1.lineplot(df,y='Retweets')
    test1.lineplot_hue(df,y='Retweets')