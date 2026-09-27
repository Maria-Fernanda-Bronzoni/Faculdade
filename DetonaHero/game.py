import pygame
import sys
import config as C
from janela import Janela
from vilao import Vilao
from heroi import Heroi
import score


class Game:
    """ Classe principal que gerencia o jogo: inicialização, loop, estados e desenho na tela. """

    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((C.LARGURA_TELA, C.ALTURA_TELA))  # cria janela
        pygame.display.set_caption(C.CAPTION)  # título da janela
        self.clock = pygame.time.Clock()       # relógio para controlar FPS
        self.rodando = True                    # flag para o loop do jogo

        # Inicializa recursos visuais e configura estado inicial do jogo
        self._carregar_recursos()
        self._configurar_jogo()

    def _carregar_recursos(self):
        """ Carrega imagens e fontes usadas durante o jogo para evitar repetição. """
        self.fonte_hud = pygame.font.Font(C.FONTE_PADRAO, 50)
        self.fonte_mensagem = pygame.font.Font(C.FONTE_PADRAO, 80)
        self.fundo = pygame.transform.scale(pygame.image.load(C.CAMINHO_FUNDO).convert(), (C.LARGURA_TELA, C.ALTURA_TELA))
        self.lua = pygame.image.load(C.CAMINHO_LUA).convert_alpha()
        self.fundo_arvores = pygame.transform.scale(pygame.image.load(C.CAMINHO_ARVORES).convert_alpha(), (C.LARGURA_TELA, C.ALTURA_TELA))
        self.predio_img = pygame.image.load(C.CAMINHO_PREDIO).convert_alpha()

    def _configurar_jogo(self):
        """ Define o estado inicial do jogo, cria janelas, herói e vilão, prepara variáveis. """
        self.estado_jogo = "INTRO_VILAO"      # estado inicial, vilão começa a aparecer
        self.tempo_restante = C.TEMPO_LIMITE_SEGUNDOS
        self.inicio_timer_jogo = 0

        # Cria instâncias das janelas com posições relativas ao prédio
        posicoes_janelas = [(C.POS_PREDIO[0] + x, C.POS_PREDIO[1] + y) for x, y in C.POSICOES_JANELAS_QUEBRADAS_RELATIVAS]
        self.janelas = [Janela(pos) for pos in posicoes_janelas]
        self.total_janelas = len(self.janelas)
        self.janelas_consertadas_contador = self.total_janelas  # contador de janelas não quebradas

        # Posiciona o herói fora da tela, para que ele entre no momento certo
        pos_inicial_heroi = (C.LARGURA_TELA + 150, C.ALTURA_TELA - 250)
        self.heroi = Heroi(posicao_inicial=pos_inicial_heroi)

        # Configura o vilão e seus alvos (janelas)
        self.vilao = Vilao()
        self.alvos_vilao = self.janelas[:]
        self.indice_alvo_vilao = 0
        if self.alvos_vilao:
            self.vilao.definir_alvo(self.alvos_vilao[self.indice_alvo_vilao].rect.center)

    def executar(self):
        """ Loop principal do jogo, executa enquanto self.rodando for True. """
        while self.rodando:
            self.tratar_eventos()    # capta inputs e eventos
            self.atualizar()         # atualiza lógica do jogo conforme estado
            self.desenhar()          # desenha tudo na tela
            pygame.display.flip()    # atualiza a tela
            self.clock.tick(C.FPS)   # controla FPS

            # Exibe tela final por 2 segundos e encerra loop se jogo terminou
            if self.estado_jogo in ["FIM", "VITORIA"]:
                self._desenhar_cenario()
                self._desenhar_personagens_e_objetos()
                self._desenhar_hud()
                self._desenhar_mensagens_finais()
                pygame.display.flip()
                pygame.time.delay(2000)
                self.rodando = False

        # Se ganhou, pede nome, salva tempo e mostra ranking
        if self.estado_jogo == "VITORIA":
            nome = self.pedir_nome_jogador()
            tempo = C.TEMPO_LIMITE_SEGUNDOS - self.tempo_restante
            score.salvar_tempo(tempo, nome)
            ranking_atual = score.ler_ranking()
            self.mostrar_ranking(ranking_atual)

        # Mensagem e cor para tela final de acordo com resultado
        mensagem = "VITÓRIA!" if self.estado_jogo == "VITORIA" else "TEMPO ESGOTADO!"
        cor = C.COR_VERDE if self.estado_jogo == "VITORIA" else C.COR_VERMELHA

        # Tela final com botões para escolher próxima ação
        escolha = self.tela_fim(mensagem, cor)

        if escolha == 'rejogar':
            return 'rejogar'
        elif escolha == 'menu':
            return 'menu'
        else:
            return 'sair'

    def tela_fim(self, mensagem_texto, cor_texto):
        """ Tela final com botões: Jogar Novamente, Menu e Sair. """
        fonte_botao = pygame.font.Font(C.FONTE_PADRAO, 50)

        # Define botões retangulares na tela
        botao_rejogar = pygame.Rect(C.LARGURA_TELA/2 - 175, 350, 350, 80)
        botao_menu = pygame.Rect(C.LARGURA_TELA/2 - 175, 450, 350, 80)
        botao_sair = pygame.Rect(C.LARGURA_TELA/2 - 175, 550, 350, 80)

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'sair'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Retorna opção escolhida ao clicar nos botões
                    if botao_rejogar.collidepoint(mouse_pos):
                        return 'rejogar'
                    elif botao_menu.collidepoint(mouse_pos):
                        return 'menu'
                    elif botao_sair.collidepoint(mouse_pos):
                        return 'sair'

            # Muda cursor para mão ao passar em cima dos botões
            if botao_rejogar.collidepoint(mouse_pos) or botao_menu.collidepoint(mouse_pos) or botao_sair.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # Desenha fundo e elementos do menu final
            if self.fundo:
                self.tela.blit(self.fundo, (0, 0))
            else:
                self.tela.fill(C.COR_FUNDO_MENU)

            mensagem = self.fonte_mensagem.render(mensagem_texto, True, cor_texto)
            self.tela.blit(mensagem, mensagem.get_rect(center=(C.LARGURA_TELA/2, 200)))

            self._desenhar_botao_fim(botao_rejogar, "Jogar Novamente", C.COR_BOTAO_MENU, C.COR_BOTAO_HOVER_MENU)
            self._desenhar_botao_fim(botao_menu, "Voltar ao Menu", C.COR_BOTAO_MENU, C.COR_BOTAO_HOVER_MENU)
            self._desenhar_botao_fim(botao_sair, "Sair", C.COR_BOTAO_SAIR_MENU, C.COR_BOTAO_SAIR_HOVER_MENU)

            pygame.display.flip()
            self.clock.tick(C.FPS)

    def tratar_eventos(self):
        """ Verifica eventos do pygame, principalmente fechar a janela ou ESC para sair. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.rodando = False

    def atualizar(self):
        """ Atualiza lógica do jogo de acordo com o estado atual. """
        if self.estado_jogo == "INTRO_VILAO":
            self._atualizar_intro_vilao()
        elif self.estado_jogo == "INTRO_HEROI":
            self._atualizar_intro_heroi()
        elif self.estado_jogo == "JOGANDO":
            self._atualizar_jogando()

    def _atualizar_intro_vilao(self):
        """ Controle do vilão no estado inicial, andando e quebrando janelas. """
        self.vilao.atualizar()

        if self.vilao.ataque_concluido:
            self.vilao.ataque_concluido = False
            if self.indice_alvo_vilao < len(self.alvos_vilao):
                self.alvos_vilao[self.indice_alvo_vilao].quebrar()  # janela é quebrada
                self.indice_alvo_vilao += 1
                # Define próximo alvo ou saída do vilão
                if self.indice_alvo_vilao < len(self.alvos_vilao):
                    self.vilao.definir_alvo(self.alvos_vilao[self.indice_alvo_vilao].rect.center)
                else:
                    self.vilao.definir_alvo(C.POSICAO_SAIDA_VILAO)

        elif self.vilao.chegou_no_alvo() and self.vilao.estado != 'atacando':
            self.vilao.atacar()

        elif self.vilao.chegou_no_alvo() and self.indice_alvo_vilao >= len(self.alvos_vilao):
            self.estado_jogo = "INTRO_HEROI"
            ponto_encontro_heroi = (C.POS_PREDIO[0] + self.predio_img.get_width() / 2, C.ALTURA_TELA - 250)
            self.heroi.definir_alvo_automatico(ponto_encontro_heroi)

    def _atualizar_intro_heroi(self):
        """ Controla a entrada do herói após o vilão terminar suas ações. """
        self.heroi.atualizar()
        if self.heroi.chegou_no_alvo():
            self.heroi.parar_movimento_automatico()
            self.estado_jogo = "JOGANDO"
            self.inicio_timer_jogo = pygame.time.get_ticks()

    def _atualizar_jogando(self):
        """ Estado principal do jogo: movimentação do herói, reparo das janelas e controle do tempo. """
        self.heroi.atualizar()
        keys = pygame.key.get_pressed()

        # Verifica se o herói está em uma janela quebrada e tecla espaço está pressionada
        janela_alvo = next((j for j in self.janelas if j.quebrada and j.rect.collidepoint(self.heroi.rect.center)), None)

        if janela_alvo and keys[pygame.K_SPACE]:
            self.heroi.mudar_estado('reparando')
            delta_time = self.clock.get_time() / 1000.0  # tempo em segundos desde último frame
            janela_alvo.aumentar_progresso(C.INCREMENTO_CONSERTO_POR_SEGUNDO * delta_time)
        else:
            if self.heroi.estado_animacao == 'reparando':
                self.heroi.mudar_estado('idle')

        # Atualiza contador de janelas consertadas
        self.janelas_consertadas_contador = len([j for j in self.janelas if not j.quebrada])
        if self.janelas_consertadas_contador == self.total_janelas:
            self.estado_jogo = "VITORIA"
            return

        # Atualiza tempo restante e verifica se acabou
        tempo_decorrido = (pygame.time.get_ticks() - self.inicio_timer_jogo) / 1000
        self.tempo_restante = max(0, C.TEMPO_LIMITE_SEGUNDOS - tempo_decorrido)
        if self.tempo_restante <= 0:
            self.estado_jogo = "FIM"

    def desenhar(self):
        """ Função que desenha o cenário, personagens, HUD e mensagens finais. """
        self._desenhar_cenario()
        self._desenhar_personagens_e_objetos()
        self._desenhar_hud()
        self._desenhar_mensagens_finais()

    def _desenhar_cenario(self):
        """ Desenha o fundo, árvores, prédio e lua na tela. """
        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self.fundo_arvores, (0, 0))
        self.tela.blit(self.predio_img, C.POS_PREDIO)
        self.tela.blit(self.lua, (-100, -30))

    def _desenhar_personagens_e_objetos(self):
        """ Desenha todas as janelas, vilão e herói na tela. """
        for janela in self.janelas:
            janela.desenhar(self.tela)
        self.vilao.desenhar(self.tela)
        self.heroi.desenhar(self.tela)

    def _desenhar_hud(self):
        """ Desenha o contador de janelas e o tempo restante na tela. """
        texto_contador = self.fonte_hud.render(f"Janelas: {self.janelas_consertadas_contador} / {self.total_janelas}", True, C.COR_AMARELA)
        self.tela.blit(texto_contador, (C.LARGURA_TELA - 300, 20))

        cor_tempo = C.COR_VERDE if self.tempo_restante > 10 else C.COR_VERMELHA
        texto_tempo = self.fonte_hud.render(f"Tempo: {int(self.tempo_restante)}s", True, cor_tempo)
        self.tela.blit(texto_tempo, (20, 20))

        # Barra de progresso para reparo da janela se herói estiver nela
        janela_alvo = next((j for j in self.janelas if j.quebrada and j.rect.collidepoint(self.heroi.rect.center)), None)
        if janela_alvo:
            largura_total = 300
            altura_total = 25
            pos_x = C.LARGURA_TELA / 2 - largura_total / 2
            pos_y = C.ALTURA_TELA - 60

            fundo_rect = pygame.Rect(pos_x, pos_y, largura_total, altura_total)
            pygame.draw.rect(self.tela, C.COR_BARRA_PROGresso_FUNDO, fundo_rect, border_radius=5)

            progresso = janela_alvo.progresso_conserto / janela_alvo.limite_conserto
            largura_progresso = largura_total * progresso
            progresso_rect = pygame.Rect(pos_x, pos_y, largura_progresso, altura_total)
            pygame.draw.rect(self.tela, C.COR_BARRA_PROgresso_FRENTE, progresso_rect, border_radius=5)
            pygame.draw.rect(self.tela, C.COR_BRANCA, fundo_rect, 2, border_radius=5)

    def _desenhar_mensagens_finais(self):
        """ Exibe mensagem de vitória ou fim de tempo com fundo transparente. """
        mensagem_texto = None
        cor_texto = C.COR_BRANCA

        if self.estado_jogo == "FIM":
            mensagem_texto = "TEMPO ESGOTADO!"
            cor_texto = C.COR_VERMELHA
        elif self.estado_jogo == "VITORIA":
            mensagem_texto = "VITÓRIA!"
            cor_texto = C.COR_VERDE

        if mensagem_texto:
            fundo_transparente = pygame.Surface((C.LARGURA_TELA, C.ALTURA_TELA), pygame.SRCALPHA)
            fundo_transparente.fill((0, 0, 0, 150))  # preto semitransparente
            self.tela.blit(fundo_transparente, (0, 0))

            mensagem = self.fonte_mensagem.render(mensagem_texto, True, cor_texto)
            mensagem_rect = mensagem.get_rect(center=(C.LARGURA_TELA / 2, C.ALTURA_TELA / 2))
            self.tela.blit(mensagem, mensagem_rect)

    def _desenhar_botao_fim(self, rect, texto, cor_normal, cor_hover):
        """ Desenha botão com texto e muda cor quando o mouse está sobre ele. """
        mouse_pos = pygame.mouse.get_pos()
        cor = cor_hover if rect.collidepoint(mouse_pos) else cor_normal
        pygame.draw.rect(self.tela, cor, rect, border_radius=15)

        fonte = pygame.font.Font(C.FONTE_PADRAO, 50)
        texto_surf = fonte.render(texto, True, C.COR_TEXTO_MENU)
        texto_rect = texto_surf.get_rect(center=rect.center)
        self.tela.blit(texto_surf, texto_rect)

    def pedir_nome_jogador(self):
        """ Exibe tela para digitar nome do jogador para ranking e retorna o nome. """
        nome = ""
        fonte_input = pygame.font.Font(C.FONTE_PADRAO, 50)
        fonte_instrucao = pygame.font.Font(C.FONTE_PADRAO, 30)

        ativo = True
        while ativo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        ativo = False
                    elif event.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        if len(nome) < 15 and event.unicode.isprintable():
                            nome += event.unicode

            self.tela.fill(C.COR_FUNDO_MENU)

            instrucao = fonte_instrucao.render("Digite seu nome e pressione Enter:", True, C.COR_BRANCA)
            self.tela.blit(instrucao, instrucao.get_rect(center=(C.LARGURA_TELA / 2, 150)))

            texto_nome = fonte_input.render(nome, True, C.COR_AMARELA)
            ret_texto = texto_nome.get_rect(center=(C.LARGURA_TELA / 2, 250))
            pygame.draw.rect(self.tela, C.COR_PRETA, ret_texto.inflate(20, 20))
            self.tela.blit(texto_nome, ret_texto)

            pygame.display.flip()
            self.clock.tick(C.FPS)

        return nome.strip()

    def mostrar_ranking(self, ranking):
        """ Exibe tela com os melhores tempos do ranking. """
        fonte_titulo = pygame.font.Font(C.FONTE_PADRAO, 60)
        fonte_lista = pygame.font.Font(C.FONTE_PADRAO, 40)

        mostrando = True
        while mostrando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        mostrando = False

            self.tela.fill(C.COR_FUNDO_MENU)
            titulo = fonte_titulo.render("Ranking - Melhores Tempos", True, C.COR_AMARELA)
            self.tela.blit(titulo, titulo.get_rect(center=(C.LARGURA_TELA / 2, 80)))

            y_inicio = 150
            for i, item in enumerate(ranking[:10]):
                texto = f"{i+1}. {item['nome']} - {item['tempo']:.2f} s - {item['data']}"
                linha = fonte_lista.render(texto, True, C.COR_BRANCA)
                self.tela.blit(linha, (C.LARGURA_TELA / 2 - linha.get_width() / 2, y_inicio + i * 50))

            instrucao = fonte_lista.render("Pressione ENTER ou ESC para continuar", True, C.COR_AMARELA)
            self.tela.blit(instrucao, instrucao.get_rect(center=(C.LARGURA_TELA / 2, C.ALTURA_TELA - 50)))

            pygame.display.flip()
            self.clock.tick(C.FPS)
