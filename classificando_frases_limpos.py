#!-*- coding: utf8 -*-
from collections import Counter
from sklearn.cross_validation import cross_val_score
import numpy as np
import pandas as pd
import nltk

texto1 = "Se eu comprar cinco anos antecipados, eu ganho algum desconto?"
texto2 = "O exercício 15 do curso de Java 1 está com a resposta errada. Pode conferir pf?"
texto3 = "Existe algum curso para cuidar do marketing da minha empresa?"

# nltk.download('punkt')

classificacoes = pd.read_csv('frases.csv', encoding = 'utf-8')
textosPuros = classificacoes['frase']
frases = textosPuros.str.lower()
textosQuebrados = [nltk.tokenize.word_tokenize(frase) for frase in frases]

# nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

# nltk.download('rslp')
stemmer = nltk.stem.RSLPStemmer()

dicionario = set()
for lista in textosQuebrados:
	validas = [stemmer.stem(palavra) for palavra in lista if palavra not in stopwords and len(palavra) > 2]
	dicionario.update(validas)
# print (dicionario)

totalDePalavras = len(dicionario)
tuplas = zip(dicionario, range(totalDePalavras))
tradutor = {palavra:indice for palavra,indice in tuplas}
print (totalDePalavras)

def vetorizar_texto(texto, tradutor):
	vetor = [0] * len(tradutor)

	for palavra in texto:
		if len(palavra) > 0:
			raiz = stemmer.stem(palavra)
			if raiz in tradutor:
				posicao = tradutor[raiz]
				vetor[posicao] += 1

	return vetor

vetoresDeTexto = [vetorizar_texto(texto, tradutor) for texto in textosQuebrados]
print (vetoresDeTexto[0])
marcas = classificacoes['classificacao']

X = np.array(vetoresDeTexto)
Y = np.array(marcas.tolist())

porcentagem_de_treino = 0.8

tamanho_do_treino = int(porcentagem_de_treino * len(Y))
tamanho_de_validacao = len(Y) - tamanho_do_treino

print (tamanho_do_treino)

treino_dados = X[0:tamanho_do_treino]
treino_marcacoes = Y[0:tamanho_do_treino]

validacao_dados = X[tamanho_do_treino:]
validacao_marcacoes = Y[tamanho_do_treino:]

def fit_and_predict(nome, modelo, treino_dados, treino_marcacoes):
	k = 10
	scores = cross_val_score(modelo, treino_dados, treino_marcacoes, cv = k)
	taxa_de_acerto = np.mean(scores)

	msg = "Taxa de acerto do {0}: {1}".format(nome, taxa_de_acerto)
	print (msg)
	return taxa_de_acerto

resultados = {}

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
modeloOneVsRest = OneVsRestClassifier(LinearSVC(random_state = 0))
resultadoOneVsRest = fit_and_predict("OneVsRest", modeloOneVsRest, treino_dados, treino_marcacoes)
resultados[resultadoOneVsRest] = modeloOneVsRest

from sklearn.multiclass import OneVsOneClassifier
modeloOneVsOne = OneVsOneClassifier(LinearSVC(random_state = 0))
resultadoOneVsOne = fit_and_predict("OneVsOne", modeloOneVsOne, treino_dados, treino_marcacoes)
resultados[resultadoOneVsOne] = modeloOneVsOne

from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()
resultadoMultinomial = fit_and_predict("MultinomialNB", modeloMultinomial, treino_dados, treino_marcacoes)
resultados[resultadoMultinomial] = modeloMultinomial

from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier()
resultadoAdaBoost = fit_and_predict("AdaBoostClassifier", modeloAdaBoost, treino_dados, treino_marcacoes)
resultados[resultadoAdaBoost] = modeloAdaBoost
print (resultados)
maximo = max(resultados)
vencedor = resultados[maximo]
print ("Vencedor: ")
print (vencedor)

vencedor.fit(treino_dados, treino_marcacoes)
resultado = vencedor.predict(validacao_dados)
acertos = (resultado == validacao_marcacoes)

total_de_acertos = sum(acertos)
total_de_elementos = len(validacao_marcacoes)
taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

msg = "Taxa de acerto do vencedor entre os dois algoritmos no mundo real: {0}".format(taxa_de_acerto)
print(msg)


# a eficacia do algoritmo que chuta
# tudo um unico valor(teste do algoritimo burro)
#não funcona no python 3
# acerto_base = max(Counter(validacao_marcacoes).itervalues())
# taxa_de_acerto_base = 100.0 * acerto_base / len(validacao_marcacoes)
# print("Taxa de acerto base: %f" % taxa_de_acerto_base)
# print("Total de testes: %d " % len(validacao_dados))























