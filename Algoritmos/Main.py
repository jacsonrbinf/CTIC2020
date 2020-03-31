import numpy as np
import math
import re
import pandas as pd
import random
import matplotlib.pyplot as plt
import string
import pymongo
import csv
from pymongo import MongoClient
import PreProcessamentoTexto
from PreProcessamentoTexto import *
from nltk import FreqDist
from synonyms import leCSV
import time
import datetime
from datetime import *

def create_csv():
    cli = MongoClient('localhost', 27017)
    db = cli['IssuesGithubDB_MSR']

    _names =  db.list_collection_names()
    with open('IssuesGithubDB_MSR.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["repo", "id","tipo", "conteudo"])

        for c in _names:
            lista_issues = db[c].find({})

            for issue in lista_issues:
                writer.writerow([str(issue['Nome do Repositório']),
                          str(issue['id']),
                          'Titulo',
                          str(issue['Título'])])

                writer.writerow([str(issue['Nome do Repositório']),
                          str(issue['id']),
                          'Descricao',
                          str(issue['Descrição'])])

                if(issue['Comentários'] is not None):
                    for comm in issue['Comentários']:
                        writer.writerow([str(issue['Nome do Repositório']),
                          str(issue['id']),
                          'Comentario',
                          str(comm['Comentário'])])
                
    file.close()
    cli.close()

def retornaListaTokenizadaPorTipo(data, tipo):
    a = []

    for ind, r in data.iterrows():
        d = r['limpo']
    
        if(r['tipo'] == tipo):
            for i in word_tokenize(d):
                a.append(i)
    
    print('Tokenização da lista de ' + str(tipo) + ' concluída!')

    return a

def grafico_de_barras_horizontal(lista, nome):

    x = []
    y = []

    for m in lista:
        for i, j in m.items():
            x.append(i)
            y.append(j)

    y_pos = np.arange(len(x))
    plt.barh(y_pos, y, height=0.8, left=None, align='center')
    plt.yticks(y_pos, x)

    #plt.figure(figsize=(10,7))
    
    plt.savefig(nome, dpi=199)

    plt.clf()

def retornaOcorrenciasPalavras(var_Frequencia, palavras):
    tabela_freq = []

    for p in palavras:
        dist = var_Frequencia[p.lower()]
        registry = {str(p) : dist}
        if(registry not in tabela_freq):
            tabela_freq.append(registry)
    
    return tabela_freq
     
def tokenizar_lista(l):
    ls = []

    for i in l:
        for j in word_tokenize(i):
            ls.append(j.lower())

    return ls

def ordernar_pela_freq(registro):
    for i, j in registro.items():
        return j

def save_table(lista, nome):

    with open(nome, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Termo", "Ocorrência"])

        for m in lista:
            for i, j in m.items():
                writer.writerow([str(i), str(j)])
                
    file.close()

#create_csv()

# Carrega dados        
colunas = ["repo", "id","tipo", "conteudo"]

dataAdc = pd.read_csv("database01.csv")

data = dataAdc.drop(0)

# Realiza limpeza da base de dados
data['limpo'] = [limpando_issue(str(x)) for x in data.conteudo]

# Faz a leitura do arquivo de palavras específicas
oraculo = leCSV('oraculo.csv')
oraculo = list(set(oraculo)) # Remove possíveis duplicados
oraculo = tokenizar_lista(oraculo) # Tokeniza palavras

# Faz leitura do arquivo de palavras complementares
sinonimos = leCSV('sinonimosPalavras.csv')
sinonimos = list(set(sinonimos)) # Remove possíveis duplicados
sinonimos = tokenizar_lista(sinonimos) # Tokeniza palavras

termos_adicionados = 0
# Adiciona apenas as palavras do arquivo complementar se o arquivo não a palavra
for s in sinonimos:
    if(s not in oraculo):
        oraculo.append(s)
        termos_adicionados += 1

# Separa e tokeniza todos os textos dos titulos das issues
lista_titulo  = retornaListaTokenizadaPorTipo(data, 'Titulo')
# Separa e tokeniza todos os textos das descrições das issues
lista_descricao  = retornaListaTokenizadaPorTipo(data, 'Descricao')

# Separa e tokeniza todos os textos dos comentários
lista_comentario  = retornaListaTokenizadaPorTipo(data, 'Comentario')

# Reune todos os textos em uma só estrutura. Para análise das recorrências totais
total_dataset = lista_titulo + lista_descricao + lista_comentario

# Analise frequências das palavras
freq_Titulo = FreqDist(lista_titulo)
freq_Descricao = FreqDist(lista_descricao)
freq_Comentario = FreqDist(lista_comentario)
freq_Total = FreqDist(total_dataset)

# Analise as frequências dos termos que foram técnicos na base dados. 
# Ocorrência das palavras no titulo, descrição e comentários da issue. Assim como em todo o texto
ocorrencias_titulo = retornaOcorrenciasPalavras(freq_Titulo, oraculo)
ocorrencias_desc = retornaOcorrenciasPalavras(freq_Descricao, oraculo)
ocorrencias_comm = retornaOcorrenciasPalavras(freq_Comentario, oraculo)
ocorrencias_totais = retornaOcorrenciasPalavras(freq_Total, oraculo)

# Ordena as listas por quantidade de ocorrências das palavras
ocorrencias_titulo.sort(key=ordernar_pela_freq, reverse=True)
ocorrencias_desc.sort(key=ordernar_pela_freq, reverse=True)
ocorrencias_comm.sort(key=ordernar_pela_freq, reverse=True)
ocorrencias_totais.sort(key=ordernar_pela_freq, reverse=True)

# Seleciona os 25 termos mais recorrentes e cria gráfico
q = 25
plt.figure(figsize=(10,7))

grafico_de_barras_horizontal(ocorrencias_titulo[:q], 'fig_titulo.png')
grafico_de_barras_horizontal(ocorrencias_desc[:q], 'fig_descricao.png')
grafico_de_barras_horizontal(ocorrencias_comm[:q], 'fig_comentario.png')
grafico_de_barras_horizontal(ocorrencias_totais[:q], 'fig_ocorren_geral.png')

# Salva os dados das ocorrências e os termos em tabelas
save_table(ocorrencias_titulo, 'ocorrencias_oraculo_titulo.csv')
save_table(ocorrencias_desc, 'ocorrencias_oraculo_desc.csv')
save_table(ocorrencias_comm, 'ocorrencias_oraculo_comm.csv')
save_table(ocorrencias_totais, 'ocorrencias_geral_total.csv')

print_termo_total = str('Quantidade de termos totais ' + str(len(total_dataset)) + '\n')
print_termo_titulo = str('Quantidade de termos no título ' + str(len(lista_titulo))+ '\n')
print_termo_descricao = str('Quantidade de termos descrição ' + str(len(lista_descricao))+ '\n')
print_termo_comentario = str('Quantidade de termos comentários ' + str(len(lista_comentario))+ '\n')
print_documentos_analisados = str('Quantidade de documentos analisados '+str(len(data['limpo']))+ '\n')
print_termos_novos_adicionados = str('Quantidade de termos novos adicionados no vocabulário '+str(termos_adicionados)+ '\n')

arquivo = open('Dados_Processamento.txt', 'w')

arquivo.writelines(print_termo_total)
print(print_termo_total)
arquivo.writelines(print_termo_titulo)
print(print_termo_titulo)
arquivo.writelines(print_termo_descricao)
print(print_termo_descricao)
arquivo.writelines(print_termo_comentario)
print(print_termo_comentario)
arquivo.writelines(print_documentos_analisados)
print(print_documentos_analisados)
arquivo.writelines(print_termos_novos_adicionados)
print(print_termos_novos_adicionados)

arquivo.close()

print(' Processo terminado.')