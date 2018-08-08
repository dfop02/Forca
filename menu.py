#-*- coding: utf-8 -*-

import pygame, sys, time, string, forca
from forca import Forca
from pygame.locals import *

pygame.init()

tela_width = 800
tela_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)

FPS = 60

class Menu(object):
	def __init__(self):
		self.gameTela = pygame.display.set_mode((tela_width ,tela_height))
		pygame.display.set_caption('Jogo da Forca')
		self.clock = pygame.time.Clock()
		self.jogo = None

	def desenha_forca(self, erros):
		if erros >= 1:
			pygame.draw.circle(self.gameTela, blue, (360, 200), 20, 5)
			if erros >= 2:
				pygame.draw.rect(self.gameTela, blue, (350, 220, 20, 100), 5)
				if erros >= 3:
					pygame.draw.line(self.gameTela, blue, (350, 230), (320, 280), 5)
					if erros >= 4:
						pygame.draw.line(self.gameTela, blue, (370, 230), (400, 280), 5)
						if erros >= 5:
							pygame.draw.line(self.gameTela, blue, (350, 320), (320, 370), 5)
							if erros >= 6:
								pygame.draw.line(self.gameTela, blue, (370, 320), (400, 370), 5)
								self.jogo.perdeu = True

	def desenha_jogo(self):
		pygame.draw.rect(self.gameTela, black, (100, 100, 40, 400), 5)
		pygame.draw.rect(self.gameTela, black, (140, 100, 240, 40), 5)
		pygame.draw.rect(self.gameTela, black, (340, 140, 40, 40), 5)

		simpleText = pygame.font.Font('freesansbold.ttf', 30)
		n = 0
		
		# Verifica se a palavra é grande, se for quebra em duas linhas
		if len(self.jogo.p_oculta) < 13:
			for i in self.jogo.p_oculta:
				letra = simpleText.render(i, True, black)
				if i != '_ ':			
					self.gameTela.blit(letra, (170+n, 470))
				else:
					pygame.draw.rect(self.gameTela, black, (160+n, 500, 40, 0), 5)
				n += 50
		else:
			for i in self.jogo.p_oculta:
				letra = simpleText.render(i, True, black)
				if i != '_ ':			
					self.gameTela.blit(letra, (170+n, 440))
					if n > 600:
						self.gameTela.blit(letra, (170+n-650, 470))
				else:
					pygame.draw.rect(self.gameTela, black, (160+n, 470, 40, 0), 5)
					if n > 600:
						pygame.draw.rect(self.gameTela, black, (160+n-650, 500, 40, 0), 5)
				n += 50

		letra = simpleText.render('Dica: ', True, black)
		self.gameTela.blit(letra, (40, 60))
		letra = simpleText.render(self.jogo.dica, True, black)
		self.gameTela.blit(letra, (130, 60))

		letra = simpleText.render('Acertos: ', True, black)
		self.gameTela.blit(letra, (70, 520))
		n = 0
		for i in self.jogo.acertos:
			letra = simpleText.render(i, True, black)
			self.gameTela.blit(letra, (195+n, 520))
			n += 20

		letra = simpleText.render('Erros: ', True, black)
		self.gameTela.blit(letra, (70, 560))
		n = 0
		for i in self.jogo.erros:
			letra = simpleText.render(i, True, black)
			self.gameTela.blit(letra, (165+n, 560))
			n += 20

		self.desenha_forca(len(self.jogo.erros))

		if self.jogo.repetido:
			letra = simpleText.render('Essa letra ja foi escolhida', True, black)
			self.gameTela.blit(letra, (200, 20))

		if self.jogo.perdeu:
			pygame.display.update()
			time.sleep(0.5)
			self.gameTela.fill(white)
			letra = simpleText.render('Voce perdeu! Mais sorte na proxima!', True, black)
			resp = simpleText.render('A palavra era: ' + str(self.jogo.palavra), True, black)
			self.gameTela.blit(letra, (180, 200))
			self.gameTela.blit(resp, (180, 240))
		elif self.jogo.ganhou:
			pygame.display.update()
			self.gameTela.fill(white)
			letra = simpleText.render('Parabens!! Voce venceu!', True, black)
			self.gameTela.blit(letra, (200, 200))
		else:
			self.btn_sair()

	def text_objects(self, text, font):
		textSurface = font.render(text, True, black)
		return textSurface, textSurface.get_rect()

	def game_intro(self):
		largeText = pygame.font.Font('freesansbold.ttf', 60)
		TextSurf, TextRect = self.text_objects("Jogo da Forca", largeText)
		TextRect.center = ((tela_width/2),(tela_height/4))
		self.gameTela.blit(TextSurf, TextRect)

		options = ['Jogar', 'Sair']
		x, y = tela_width/2.6, tela_height/2
		n = 0
		for i in range(len(options)):
			option = largeText.render(options[i], True, black)
			self.gameTela.blit(option, (x, y+n))
			n += 100
		pygame.draw.rect(self.gameTela, black, (x-10, y, 190, 70), 5)
		pygame.draw.rect(self.gameTela, black, (x-10, y+100, 140, 70), 5)

	def btn_sair(self):
		x, y = tela_width/2.6, tela_height/2
		largeText = pygame.font.Font('freesansbold.ttf', 40)
		btn = largeText.render('Voltar', True, black)
		self.gameTela.blit(btn, (x+340, y+240))
		pygame.draw.rect(self.gameTela, black, (x+330, y+235, 140, 50), 5)

	def credit(self):
		largeText = pygame.font.Font('freesansbold.ttf', 20)
		btn = largeText.render('by: dfop02', True, black)
		self.gameTela.blit(btn, (680, 560))

	def jogo_loop(self):
		menu = True
		x, y = tela_width/2.6, tela_height/2
		self.jogo = Forca()
		while menu:
			self.gameTela.fill(white)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				elif event.type == pygame.KEYDOWN:
					self.jogo.checaLetra(string.lower(event.unicode))
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						if pygame.Rect(x+330, y+235, 140, 50).collidepoint(event.pos):
							menu = False
			self.jogo.checaGameover()
			if self.jogo.perdeu:
				self.desenha_jogo()
				time.sleep(1)
				pygame.display.update()
				time.sleep(3)
				menu = False	
			elif self.jogo.ganhou:
				self.desenha_jogo()
				time.sleep(1)
				pygame.display.update()
				time.sleep(3)
				menu = False
			else:
				self.desenha_jogo()
			pygame.display.update()
			self.clock.tick(FPS)

	def menu_loop(self):
		menu = True
		x, y = tela_width/2.6, tela_height/2
		while menu:
			self.gameTela.fill(white)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						if pygame.Rect(x-10, y, 190, 70).collidepoint(event.pos):
							self.jogo_loop()
						elif pygame.Rect(x-10, y+100, 140, 70).collidepoint(event.pos):
							pygame.quit()
							quit()
			self.game_intro()
			self.credit()
			pygame.display.update()
			self.clock.tick(FPS)

menu = Menu()
menu.menu_loop()
pygame.quit()
quit()
