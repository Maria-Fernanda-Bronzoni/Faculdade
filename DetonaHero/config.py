# --- CONFIGURAÇÕES GERAIS DA TELA ---
LARGURA_TELA = 1280                      # Largura da janela do jogo em pixels
ALTURA_TELA = 720                       # Altura da janela do jogo em pixels
CAPTION = "Detona Hero"                 # Título da janela do jogo
FPS = 60                               # Frames por segundo para controlar a taxa de atualização

# --- CORES ---
# Definições RGB das cores usadas no jogo para facilitar o uso e manutenção
COR_BRANCA = (255, 255, 255)
COR_PRETA = (0, 0, 0)
COR_AMARELA = (255, 255, 0)
COR_VERDE = (0, 255, 0)
COR_VERMELHA = (255, 0, 0)

# Cores específicas para elementos do menu, permitindo fácil ajuste visual
COR_FUNDO_MENU = (10, 20, 40)
COR_TITULO_MENU = (255, 255, 0)
COR_BOTAO_MENU = (0, 100, 0)
COR_BOTAO_HOVER_MENU = (0, 180, 0)
COR_BOTAO_SAIR_MENU = (100, 0, 0)
COR_BOTAO_SAIR_HOVER_MENU = (180, 0, 0)
COR_TEXTO_MENU = (255, 255, 255)

# Cores para a HUD, especialmente barra de progresso (fundo e frente)
COR_BARRA_PROGresso_FUNDO = (50, 50, 50)
COR_BARRA_PROgresso_FRENTE = (0, 200, 0)

# --- FONTES ---
FONTE_PADRAO = None                    # Usar fonte padrão do sistema (pygame font default)

# --- CAMINHOS DE ARQUIVOS ---
# Strings com os caminhos dos arquivos de imagem para carregar assets facilmente
CAMINHO_FUNDO = "assets/fundo.png"
CAMINHO_LUA = "assets/lua.png"
CAMINHO_ARVORES = "assets/arvores.png"
CAMINHO_PREDIO = "assets/predio.png"
CAMINHO_JANELA_QUEBRADA = "assets/janelaquebrada.png"

# Assets do herói para diferentes animações (idle, walk, reparando)
CAMINHO_HEROI_IDLE = "assets/heroi/Idle.png"
CAMINHO_HEROI_WALK = "assets/heroi/Walk.png"
CAMINHO_HEROI_REPARANDO = "assets/heroi/Attack_4.png" 

# Assets do vilão para animações diferentes (idle, ataques variados)
CAMINHO_VILAO_IDLE = "assets/vilao/Idle1.png"
CAMINHO_VILAO_ATTACK1 = "assets/vilao/Attack1.png"
CAMINHO_VILAO_ATTACK2 = "assets/vilao/Attack2.png"
CAMINHO_VILAO_ATTACK3 = "assets/vilao/Attack3.png"
CAMINHO_VILAO_ATTACK4 = "assets/vilao/Attack4.png"

# --- CONFIGURAÇÕES DA GAMEPLAY ---
TEMPO_LIMITE_SEGUNDOS = 120            # Tempo máximo para o jogador terminar o jogo
POS_PREDIO = (440, 60)                # Posição do prédio na tela (x, y)

# --- CONFIGURAÇÕES DO HERÓI ---
VELOCIDADE_HEROI = 5                  # Pixels por frame que o herói anda
VELOCIDADE_ANIMACAO_HEROI = 150      # Milissegundos entre frames da animação do herói
TAMANHO_FRAME_HEROI = (128, 128)     # Tamanho de cada frame da sprite do herói
NUM_FRAMES_HEROI_IDLE = 4             # Quantidade de frames na animação idle
NUM_FRAMES_HEROI_WALK = 8             # Frames para animação de caminhada
NUM_FRAMES_HEROI_REPARANDO = 10       # Frames para animação de reparo

# --- CONFIGURAÇÕES DO VILÃO ---
VELOCIDADE_VILAO = 8                 # Pixels por frame que o vilão anda
POSICAO_INICIAL_VILAO = (-200, 100) # Posição inicial fora da tela, vindo da esquerda
POSICAO_SAIDA_VILAO = (-200, 100)   # Posição para onde o vilão sai (mesma da inicial)
VELOCIDADE_ANIMACAO_VILAO = 80      # Intervalo em ms entre frames da animação do vilão

# --- CONFIGURAÇÕES DAS JANELAS ---
PROGRESSO_MAXIMO_CONSERTO = 100      # Valor máximo para o progresso do conserto da janela
INCREMENTO_CONSERTO_POR_SEGUNDO = 50 # Quantidade que o conserto avança por segundo
JANELA_COLISAO_INFLATE = (-30, -30) # Ajusta o retângulo de colisão para ser menor que a janela

# --- POSIÇÕES DAS JANELAS QUEBRADAS ---
# Posições relativas para desenhar as janelas quebradas sobre o prédio
POSICOES_JANELAS_QUEBRADAS_RELATIVAS = [
    (14, 525), (309, 525),             # 1º andar
    (14, 395), (163, 395), (309, 395),# 2º andar
    (14, 265), (163, 265), (309, 265),# 3º andar
    (14, 150), (163, 150), (309, 150),# 4º andar
    (14, 15), (163, 15), (309, 15),   # 5º andar
]

CAMINHO_RANKING = 'ranking.txt'      # Arquivo para salvar o ranking do jogo
MAX_ITENS_RANKING = 10               # Número máximo de entradas no ranking
