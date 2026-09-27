import pygame
import config as C
from spritesheet import Spritesheet

class Heroi:
    """ Controla o personagem do jogador, suas animações e movimentos. """

    def __init__(self, posicao_inicial):
        self.velocidade = C.VELOCIDADE_HEROI
        self.animacoes = self._carregar_animacoes()  # Carrega frames das animações do herói
        self.estado_animacao = 'idle'  # Estado atual da animação ('idle', 'walk', 'reparando')
        self.direcao = 'left'  # Direção para espelhar imagem

        self.frame_atual = 0
        self.imagem = self.animacoes[self.estado_animacao][self.frame_atual]  # Frame inicial
        self.rect = self.imagem.get_rect(center=posicao_inicial)  # Posição e tamanho do herói na tela

        self.ultimo_update = pygame.time.get_ticks()  # Controle do tempo para troca de frames
        self.velocidade_animacao = C.VELOCIDADE_ANIMACAO_HEROI

        self.estado_movimento = 'automatico'  # Movimento pode ser 'automatico' ou 'manual' (teclado)
        self.alvo_automatico = None  # Ponto para onde o herói deve se mover automaticamente

    def _carregar_animacoes(self):
        """ Carrega frames das animações a partir dos spritesheets. """
        animacoes = {'idle': [], 'walk': [], 'reparando': []}
        w, h = C.TAMANHO_FRAME_HEROI
        try:
            idle_sheet = Spritesheet(C.CAMINHO_HEROI_IDLE)
            animacoes['idle'] = idle_sheet.get_animation_frames(w, h, C.NUM_FRAMES_HEROI_IDLE)
            walk_sheet = Spritesheet(C.CAMINHO_HEROI_WALK)
            animacoes['walk'] = walk_sheet.get_animation_frames(w, h, C.NUM_FRAMES_HEROI_WALK)
            reparando_sheet = Spritesheet(C.CAMINHO_HEROI_REPARANDO)
            animacoes['reparando'] = reparando_sheet.get_animation_frames(w, h, C.NUM_FRAMES_HEROI_REPARANDO)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Erro ao carregar animação do herói: {e}")
        return animacoes

    def _animar(self):
        """ Atualiza o frame da animação conforme o tempo para criar movimento fluido. """
        agora = pygame.time.get_ticks()
        frames = self.animacoes.get(self.estado_animacao, self.animacoes['idle'])

        if agora - self.ultimo_update > self.velocidade_animacao:
            self.ultimo_update = agora
            self.frame_atual = (self.frame_atual + 1) % len(frames)  # Loop da animação
            imagem_base = frames[self.frame_atual]
            # Espelha imagem se direção for esquerda
            self.imagem = pygame.transform.flip(imagem_base, True, False) if self.direcao == 'left' else imagem_base

    def mudar_estado(self, novo_estado):
        """ Muda o estado de animação reiniciando o frame atual. """
        if self.estado_animacao != novo_estado:
            self.estado_animacao = novo_estado
            self.frame_atual = 0

    def atualizar(self):
        """ Atualiza a lógica do movimento e animação a cada frame do jogo. """
        if self.estado_movimento == 'automatico' and self.alvo_automatico:
            self._mover_automaticamente()
        elif self.estado_movimento == 'manual' and self.estado_animacao != 'reparando':
            self._mover_manualmente()

        self._animar()

    def _mover_automaticamente(self):
        """ Move o herói em direção ao alvo automático, atualizando direção e estado. """
        dx = self.alvo_automatico[0] - self.rect.centerx
        dy = self.alvo_automatico[1] - self.rect.centery
        if dx != 0:
            self.rect.x += self.velocidade if dx > 0 else -self.velocidade
            self.direcao = 'right' if dx > 0 else 'left'
            self.mudar_estado('walk')
        if dy != 0:
            self.rect.y += self.velocidade if dy > 0 else -self.velocidade

    def _mover_manualmente(self):
        """ Controla movimento via teclado (WASD) quando em modo manual. """
        keys = pygame.key.get_pressed()
        movendo = False
        if keys[pygame.K_a]:
            self.rect.x -= self.velocidade
            self.direcao = 'left'
            movendo = True
        if keys[pygame.K_d]:
            self.rect.x += self.velocidade
            self.direcao = 'right'
            movendo = True
        if keys[pygame.K_w]:
            self.rect.y -= self.velocidade
            movendo = True
        if keys[pygame.K_s]:
            self.rect.y += self.velocidade
            movendo = True

        self.mudar_estado('walk' if movendo else 'idle')

        # Limita movimento para dentro da tela
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(C.LARGURA_TELA, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(C.ALTURA_TELA, self.rect.bottom)

    def definir_alvo_automatico(self, pos_alvo):
        """ Define o ponto para movimento automático e altera estado para 'walk'. """
        self.alvo_automatico = pos_alvo
        self.estado_movimento = 'automatico'
        self.mudar_estado('walk')

    def chegou_no_alvo(self):
        """ Verifica se o herói está suficientemente próximo do alvo automático. """
        if not self.alvo_automatico:
            return False
        dist_x = abs(self.rect.centerx - self.alvo_automatico[0])
        dist_y = abs(self.rect.centery - self.alvo_automatico[1])
        return dist_x < self.velocidade and dist_y < self.velocidade

    def parar_movimento_automatico(self):
        """ Para o movimento automático, libera o controle para o jogador (manual). """
        self.alvo_automatico = None
        self.estado_movimento = 'manual'
        self.mudar_estado('idle')

    def desenhar(self, tela):
        """ Desenha o sprite do herói na tela na posição atual. """
        tela.blit(self.imagem, self.rect.topleft)
