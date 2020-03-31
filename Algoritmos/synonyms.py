import nltk
from nltk.corpus import wordnet
import csv

def leCSV(path):
    lista_palavras = []

    with open(path, mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            #words_list.append({row[1] : row[0]})
            lista_palavras.append(row[0])

    file.close()

    return lista_palavras

def buscar_sinonimos(name):
    lista = []

    for i in wordnet.synsets(name):
        for j in i.lemmas():
            lista.append(j.name())

    return lista

def criaTabelaSinonimo(path, ln):
    with open(path + '.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Sinônimo', 'Palavra'])

        for i in ln:
            lista_sinonimos = buscar_sinonimos(str(i))
                
            for j in lista_sinonimos:
                if (j != i):
                    writer.writerow([str(j), str(i)])
        
    file.close()
   
#lista_palavras = leCSV('oraculo.csv')

#criaTabelaSinonimo('sinonimosPalavras', lista_palavras)
