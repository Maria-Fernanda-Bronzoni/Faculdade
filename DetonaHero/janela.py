import pygame
import config as C

class Janela:
    def __init__(self, pos):
        self.quebrada = False  # Estado da janela (quebrada ou não)
        self.imagem_quebrada = pygame.image.load(C.CAMINHO_JANELA_QUEBRADA).convert_alpha()  # Imagem da janela quebrada
        
        # Retângulo para desenhar a imagem na posição correta na tela
        self.draw_rect = self.imagem_quebrada.get_rect(topleft=pos)
        
        # Retângulo de colisão, inflado para ser menor que o draw_rect para precisão na detecção
        self.rect = self.draw_rect.copy()
        self.rect.inflate_ip(C.JANELA_COLISAO_INFLATE)

        self.progresso_conserto = 0.0  # Quanto foi consertado da janela (0 a limite)
        self.limite_conserto = C.PROGRESSO_MAXIMO_CONSERTO  # Valor necessário para consertar completamente

    def quebrar(self):
        """ Marca a janela como quebrada e zera o progresso de conserto. """
        self.quebrada = True
        self.progresso_conserto = 0.0

    def consertar(self):
        """ Marca a janela como consertada (não quebrada) e reseta o progresso. """
        self.quebrada = False
        self.progresso_conserto = 0.0

    def aumentar_progresso(self, valor):
        """ Incrementa o progresso de conserto e conserta a janela se atingir o limite. """
        if self.quebrada:
            self.progresso_conserto += valor
            if self.progresso_conserto >= self.limite_conserto:
                self.consertar()

    def desenhar(self, tela):
        """ Desenha a imagem da janela quebrada na tela se estiver quebrada. """
        if self.quebrada:
            tela.blit(self.imagem_quebrada, self.draw_rect.topleft)
