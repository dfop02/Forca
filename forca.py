#-*- coding: utf-8 -*-

import random
import string

# Dicas: [Palavras]
palavras = {'Animal': ['formiga', 'peixe-boi', 'esquilo', 'jacare', 'jabuti', 'elefante', 'tigre', 'escorpiao', 'macaco', 'crocodilo', 'lesma', 'rinoceronte'],
			'Cidade': ['tokyo', 'nova york', 'roma', 'las vegas', 'viena', 'moscou', 'viena', 'lisboa', 'punta del leste', 'buenos aires', 'paris'],
			'Objeto': ['martelo', 'parafuso', 'marreta', 'chave', 'canivete', 'prego', 'caneta', 'copo'],
			'Filme': ['o pequenino', 'transformers', 'it: a coisa', 'os mercenarios', 'motoqueiro fantasma', 'harry potter', 'missao impossivel'],
			'Meio de Transporte': ['onibus', 'trem', 'aviao', 'barco', 'lancha', 'jet sky', 'carro', 'moto', 'skate', 'metro'],
			'Eletronico': ['celular', 'video game', 'computador', 'camera digital', 'gps', 'notebook', 'tablet'],
			'Pais': ['reino unido', 'portugal', 'argentina', 'brasil', 'estados unidos', 'australia', 'russia', 'mexico', 'canada', 'suecia'],
			'Profissao': ['medico', 'carteiro', 'economista', 'programador', 'professor', 'veterinario'],
			'Cor': ['laranja', 'azul celeste', 'violeta', 'roxo', 'branco', 'verde agua', 'amarelo ocre'],
			'Roupa': ['blusa', 'camiseta', 'casaco', 'chapeu', 'gravata', 'chinelo', 'meia', 'terno', 'vestido']
}

letras = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

acentos =  {'a': ['à', 'á', 'ã', 'ê'],
			'e': ['è', 'é', 'ẽ', 'ê'],
			'i': ['ì', 'í', 'ĩ', 'î'],
			'o': ['ò', 'ó', 'õ', 'ô'],
			'u': ['ù', 'ú', 'ũ', 'û']
}

# Evitar repeticao de palavras
escolhidos = list()

class Forca(object):
	def __init__(self):
		self.dica, self.palavra = self.getPalavra()
		self.erros = list()
		self.acertos = list()
		self.repetido = False
		self.p_oculta = self.ocultaPalavra()
		self.ganhou = False
		self.perdeu = False

	def getPalavra(self):
		palavra = ''
		while(palavra not in escolhidos):
			dica = random.choice(palavras.keys())
			for d, p in palavras.items():
				if dica == d:
					palavra = random.choice(p)
					escolhidos.append(palavra)
		return dica, palavra

	def ocultaPalavra(self):
		palavra_oculta = list()
		for i in self.palavra:
			if i == '-' or i == ' ' or i == ':':
				palavra_oculta.append(i)
			else:
				palavra_oculta.append('_ ')
		return palavra_oculta

	def mostraLetra(self, letra):
		n = 0		
		for letras in self.palavra:
			if letras == str(letra):
				self.p_oculta[n] = str(letra)
			n += 1

	def checaLetra(self, letra):
		if letra in letras:
			if not letra in self.acertos and not letra in self.erros:
				self.repetido = False

				if str(letra) in self.palavra:
					self.acertos.append(letra)
					self.mostraLetra(letra)
				
				else:
					self.erros.append(letra)
			else:
				self.repetido = True

	def checaGameover(self):
		oculta = ''
		for letra in self.p_oculta:
			oculta += str(letra)
		if oculta == self.palavra:
			self.ganhou = True