import pygame
import config as C

class Vilao:
    """ Controla o personagem do vilão, sua movimentação e animações. """
    def __init__(self):
        # Carrega as animações para os estados 'movendo' e 'atacando'
        self.animacoes = self._carregar_animacoes()
        
        # Estado inicial do vilão (pode ser 'movendo' ou 'atacando')
        self.estado = 'movendo'
        
        # Controla o frame atual da animação
        self.frame_atual = 0
        
        # Imagem inicial baseada no primeiro frame da animação 'movendo'
        self.imagem = self.animacoes['movendo'][self.frame_atual]
        
        # Retângulo de colisão e posição do vilão, posicionando na coordenada inicial
        self.rect = self.imagem.get_rect(topleft=C.POSICAO_INICIAL_VILAO)
        
        # Controle do tempo para animação, armazena o último update
        self.ultimo_update = pygame.time.get_ticks()
        
        # Velocidade entre frames para troca da animação
        self.velocidade_animacao = C.VELOCIDADE_ANIMACAO_VILAO
        
        # Flag para indicar que a animação de ataque terminou (uma vez só)
        self.ataque_concluido = False

        # Posição alvo para onde o vilão deve se mover
        self.alvo = None
        
        # Velocidade de movimento do vilão
        self.velocidade = C.VELOCIDADE_VILAO
        
        # Posição atual armazenada como lista para movimentação com floats
        self.posicao = list(self.rect.topleft)

    def _carregar_animacoes(self):
        # Carrega imagens para os estados 'movendo' e 'atacando'
        animacoes = {'movendo': [], 'atacando': []}
        
        # Carrega a imagem estática para o estado 'movendo' (idle)
        animacoes['movendo'].append(pygame.image.load(C.CAMINHO_VILAO_IDLE).convert_alpha())

        # Carrega os frames da animação de ataque (sequência de 4 imagens)
        try:
            frames_ataque = []
            caminhos_ataque = [
                C.CAMINHO_VILAO_ATTACK1, C.CAMINHO_VILAO_ATTACK2,
                C.CAMINHO_VILAO_ATTACK3, C.CAMINHO_VILAO_ATTACK4
            ]
            for caminho in caminhos_ataque:
                frames_ataque.append(pygame.image.load(caminho).convert_alpha())
            animacoes['atacando'] = frames_ataque
        except (pygame.error, FileNotFoundError) as e:
            print(f"Erro ao carregar animação de ataque do vilão: {e}")
            # Caso dê erro, usa a animação de 'movendo' como fallback
            animacoes['atacando'] = animacoes['movendo']
        return animacoes

    def _animar(self):
        # Atualiza o frame da animação conforme o tempo
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.velocidade_animacao:
            self.ultimo_update = agora
            lista_frames_atual = self.animacoes[self.estado]
            self.frame_atual += 1
            
            # Se chegou no fim da animação
            if self.frame_atual >= len(lista_frames_atual):
                # Se estava atacando, avisa que terminou e volta para movendo
                if self.estado == 'atacando':
                    self.ataque_concluido = True
                    self.estado = 'movendo'
                    self.frame_atual = 0
                else:
                    # Para estados em loop, reinicia a animação
                    self.frame_atual = 0
            
            # Atualiza a imagem para o frame atual
            self.imagem = self.animacoes[self.estado][self.frame_atual]

    def atacar(self):
        # Começa a animação de ataque se não estiver atacando
        if self.estado != 'atacando':
            self.estado = 'atacando'
            self.frame_atual = 0
            self.ataque_concluido = False

    def _mover(self):
        # Move o vilão em direção ao alvo, se definido
        if self.alvo:
            dx = self.alvo[0] - self.rect.centerx
            dy = self.alvo[1] - self.rect.centery
            dist = (dx**2 + dy**2)**0.5

            if dist > self.velocidade:
                # Move proporcionalmente à velocidade, mantendo direção
                self.posicao[0] += (dx / dist) * self.velocidade
                self.posicao[1] += (dy / dist) * self.velocidade
                self.rect.topleft = self.posicao
            else:
                # Caso esteja perto do alvo, posiciona exatamente nele
                self.rect.center = self.alvo
                self.posicao = list(self.rect.topleft)

    def atualizar(self):
        # Atualiza o vilão a cada frame
        # Só se move se não estiver atacando
        if self.estado != 'atacando':
            self._mover()
        # Atualiza animação
        self._animar()

    def definir_alvo(self, pos_alvo):
        # Define um novo alvo para o vilão se mover até lá
        self.alvo = pos_alvo

    def chegou_no_alvo(self):
        # Verifica se o vilão chegou perto o suficiente do alvo no eixo X
        if not self.alvo:
            return False
        dist_x = abs(self.rect.centerx - self.alvo[0])
        dist_y = abs(self.rect.centery - self.alvo[1])
        return dist_x < self.velocidade  # Pode ajustar para considerar dist_y também

    def desenhar(self, tela):
        # Desenha a imagem atual do vilão na tela
        tela.blit(self.imagem, self.rect.topleft)
