#-*- coding: utf-8 -*-

# Version 1.2 #

import random
import string

# Dicas: [Palavras]
palavras = {'Animal': ['formiga', 'peixe-boi', 'esquilo', u'jacaré', 'jabuti', 'elefante', 'tigre', u'escorpião', 'macaco', 'crocodilo', 'lesma', 'rinoceronte', 'zebra', 'gato'],
			'Cidade': ['tokyo', 'nova york', 'roma', 'las vegas', 'viena', 'moscou', 'viena', 'lisboa', 'punta del leste', 'buenos aires', 'paris', u'são paulo', u'amsterdã'],
			'Objeto': ['martelo', 'parafuso', 'marreta', 'chave', 'canivete', 'prego', 'caneta', 'copo', u'lâmpada', 'cadeira', u'relógio'],
			'Filme': ['o pequenino', 'transformers', 'it: a coisa', u'os mercenários', 'motoqueiro fantasma', 'harry potter', 'missao impossivel', 'o hobbit', u'senhor dos anéis'],
			'Meio de Transporte': [u'ônibus', u'trêm', u'avião', 'barco', 'lancha', 'jet sky', 'carro', 'moto', 'skate', u'metrô'],
			'Eletronico': ['celular', 'video game', 'computador', 'camera digital', 'gps', 'notebook', 'tablet', u'robô', 'smartphone'],
			u'País': ['reino unido', 'portugal', 'argentina', 'brasil', 'estados unidos', 'australia', 'russia', u'méxico', 'canada', 'suecia', u'nova zelândia', u'crôacia', 'holanda'],
			'Profissao': [u'médico', 'carteiro', 'economista', 'programador', 'professor', u'veterinário', 'bombeiro', 'jornalista', 'advogado', 'cobrador', 'ator'],
			'Cor': ['laranja', 'azul celeste', 'violeta', 'roxo', 'branco', u'verde água', 'amarelo ocre', 'magenta'],
			'Roupa': ['blusa', 'camiseta', 'casaco', u'chapéu', 'gravata', 'chinelo', 'meia', 'terno', 'vestido', u'tênis', 'cachecol']
}

letras = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

acentos =  {'a': [u'à', u'á', u'ã', u'â'],
			'e': [u'è', u'é', u'ẽ', u'ê'],
			'i': [u'ì', u'í', u'ĩ', u'î'],
			'o': [u'ò', u'ó', u'õ', u'ô'],
			'u': [u'ù', u'ú', u'ũ', u'û']
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
		if letra in acentos.keys():
			for l in self.palavra:
				for k, v in acentos.items():
					if letra == k:
						if l == k:
							if self.dica == u'País' or self.dica == 'Cidade':
								if n == 0 or self.p_oculta[n-1] == ' ':
									self.p_oculta[n] = string.upper(str(letra))
								else:
									self.p_oculta[n] = str(letra)
							else:
								self.p_oculta[n] = str(letra)
						else:
							for a in v:
								if a == l:
									if self.dica == u'País' or self.dica == 'Cidade':
										if n == 0 or self.p_oculta[n-1] == ' ':
											self.p_oculta[n] = string.upper(a)
										else:
											self.p_oculta[n] = a
									else:
										self.p_oculta[n] = a
				n += 1
		else:
			for letras in self.palavra:
				if letras == str(letra):
					if self.dica == u'País' or self.dica == 'Cidade':
						if n == 0 or self.p_oculta[n-1] == ' ':
							self.p_oculta[n] = string.upper(str(letra))
						else:
							self.p_oculta[n] = str(letra)
					else:
						self.p_oculta[n] = str(letra)
				n += 1

	def checaLetra(self, letra):
		if letra in letras:
			if not letra in self.acertos and not letra in self.erros:
				self.repetido = False
				n = 0
				if letra in acentos.keys():
					for l in self.palavra:
						for k, v in acentos.items():
							if letra == k:
								if l == k:
									if n == 0:
										self.acertos.append(letra)
										self.mostraLetra(letra)
										n += 1
								else:
									for a in v:
										if a == l:
											if n == 0:
												self.acertos.append(letra)
												self.mostraLetra(letra)
												n += 1
					if n == 0:
						self.erros.append(letra)
				else:
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
			oculta += string.lower(letra)
		if oculta == self.palavra:
			self.ganhou = True
