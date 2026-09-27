import pygame
import config as C

class Menu:
    """ Tela de menu inicial com opções para iniciar o jogo, ver ranking ou sair. """
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((C.LARGURA_TELA, C.ALTURA_TELA))
        pygame.display.set_caption(f"{C.CAPTION} - Menu")
        
        # Fonte para o texto do autor e créditos
        self.fonte_autor = pygame.font.Font(C.FONTE_PADRAO, 40)
        self.texto_autor = self.fonte_autor.render(
            "Desenvolvido por: Maria Fernanda Bronzoni", True, C.COR_TEXTO_MENU
        )

        # Fontes para título e botões do menu
        self.fonte_titulo = pygame.font.Font(C.FONTE_PADRAO, 90)
        self.fonte_botao = pygame.font.Font(C.FONTE_PADRAO, 60)

        # Renderiza título do jogo
        self.titulo = self.fonte_titulo.render(C.CAPTION, True, C.COR_TITULO_MENU)

        # Define os retângulos (áreas) dos botões para detectar cliques
        self.botao_iniciar_rect = pygame.Rect(C.LARGURA_TELA/2 - 175, C.ALTURA_TELA/2, 350, 80)
        self.botao_sair_rect = pygame.Rect(C.LARGURA_TELA/2 - 175, C.ALTURA_TELA/2 + 100, 350, 80)
        self.botao_ranking_rect = pygame.Rect(C.LARGURA_TELA/2 - 175, C.ALTURA_TELA/2 + 200, 350, 80)
        
        # Tenta carregar imagem de fundo, caso contrário usa cor sólida
        try:
            self.fundo = pygame.transform.scale(
                pygame.image.load(C.CAMINHO_FUNDO).convert(), (C.LARGURA_TELA, C.ALTURA_TELA)
            )
        except pygame.error:
            self.fundo = None

    def desenhar_botao(self, rect, texto, cor_normal, cor_hover):
        """ Desenha botão com efeito hover baseado na posição do mouse. """
        mouse_pos = pygame.mouse.get_pos()
        cor = cor_hover if rect.collidepoint(mouse_pos) else cor_normal
        pygame.draw.rect(self.tela, cor, rect, border_radius=15)
        
        texto_surf = self.fonte_botao.render(texto, True, C.COR_TEXTO_MENU)
        texto_rect = texto_surf.get_rect(center=rect.center)
        self.tela.blit(texto_surf, texto_rect)

    def executar(self):
        """ Loop principal do menu, aguarda interação do jogador e retorna a escolha. """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'sair'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.botao_iniciar_rect.collidepoint(event.pos):
                        return 'iniciar'
                    if self.botao_sair_rect.collidepoint(event.pos):
                        return 'sair'
                    if self.botao_ranking_rect.collidepoint(event.pos):
                        return 'ranking'

            # Muda o cursor para "mão" se estiver em cima de algum botão, caso contrário seta o padrão
            mouse_pos = pygame.mouse.get_pos()
            if (self.botao_iniciar_rect.collidepoint(mouse_pos) or
                self.botao_sair_rect.collidepoint(mouse_pos) or
                self.botao_ranking_rect.collidepoint(mouse_pos)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
            # Desenha o fundo (imagem ou cor sólida)
            if self.fundo:
                self.tela.blit(self.fundo, (0, 0))
            else:
                self.tela.fill(C.COR_FUNDO_MENU)

            # Desenha créditos, título e botões
            self.tela.blit(
                self.texto_autor,
                (C.LARGURA_TELA/2 - self.texto_autor.get_width()/2, C.ALTURA_TELA/2 - 80)
            )
            self.tela.blit(
                self.titulo,
                (C.LARGURA_TELA/2 - self.titulo.get_width()/2, C.ALTURA_TELA/4)
            )
            self.desenhar_botao(self.botao_iniciar_rect, "Iniciar Jogo", C.COR_BOTAO_MENU, C.COR_BOTAO_HOVER_MENU)
            self.desenhar_botao(self.botao_sair_rect, "Sair", C.COR_BOTAO_SAIR_MENU, C.COR_BOTAO_SAIR_HOVER_MENU)
            self.desenhar_botao(self.botao_ranking_rect, "Ver Ranking", C.COR_BOTAO_MENU, C.COR_BOTAO_HOVER_MENU)

            pygame.display.flip()
