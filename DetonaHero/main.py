from game import Game
from menu import Menu
import score

if __name__ == "__main__":
    while True:
        # Cria e executa o menu inicial, aguarda escolha do usuário
        menu = Menu()
        escolha = menu.executar()

        if escolha == 'iniciar':
            while True:
                jogo = Game()  # Cria nova instância do jogo
                resultado = jogo.executar()  # Executa o jogo e espera resultado

                if resultado == 'rejogar':
                    continue  # Reinicia o jogo imediatamente

                elif resultado == 'menu':
                    break  # Volta para o menu principal

                elif resultado == 'sair':
                    exit()  # Encerra o programa

        elif escolha == 'ranking':
            ranking = score.ler_ranking()  # Lê ranking salvo
            jogo = Game()  # Cria instância só para mostrar ranking (pode ser refatorado)
            jogo.mostrar_ranking(ranking)  # Exibe ranking na tela

        elif escolha == 'sair':
            exit()  # Encerra o programa
