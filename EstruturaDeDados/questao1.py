class Nodo:

    def __init__(self, numero, cor):
        self.numero = numero
        self.cor = cor
        self.proximo = None

class ListaEncadeada:

    def __init__(self):
        self.head = None
        self.contadorVerde = 0
        self.contadorAmarelo = 200

    def inserirSemPrioridade(self, nodo):

        atual = self.head

        while atual.proximo is not None:
            atual = atual.proximo

        atual.proximo = nodo

    def inserirComPrioridade(self, nodo):

        if self.head.cor == "V":
            nodo.proximo = self.head
            self.head = nodo
            return

        atual = self.head

        while atual.proximo is not None and atual.proximo.cor == "A":
            atual = atual.proximo

        nodo.proximo = atual.proximo
        atual.proximo = nodo

    def inserir(self):

        cor = input("Digite a cor do cartão (A ou V): ").upper()

        while cor != "A" and cor != "V":
            print("Cor inválida.")
            cor = input("Digite a cor do cartão (A ou V): ").upper()

        if cor == "V":
            self.contadorVerde += 1
            numero = self.contadorVerde
        else:
            self.contadorAmarelo += 1
            numero = self.contadorAmarelo

        nodo = Nodo(numero, cor)

        if self.head is None:
            self.head = nodo
        elif cor == "V":
            self.inserirSemPrioridade(nodo)
        else:
            self.inserirComPrioridade(nodo)

    def imprimirListaEspera(self):

        if self.head is None:
            print("A fila está vazia.")
            return

        atual = self.head

        while atual is not None:
            print(f"Cartão: {atual.cor}{atual.numero}")
            atual = atual.proximo

    def atenderPaciente(self):

        if self.head is None:
            print("Não há pacientes na fila.")
            return

        paciente = self.head
        self.head = self.head.proximo

        print(f"Paciente {paciente.cor}{paciente.numero} chamado.")

def iniciarSistema():

    fila = ListaEncadeada()

    while True:

        print("1 - Adicionar paciente")
        print("2 - Mostrar pacientes na fila")
        print("3 - Chamar paciente")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            fila.inserir()

        elif opcao == "2":
            fila.imprimirListaEspera()

        elif opcao == "3":
            fila.atenderPaciente()

        elif opcao == "4":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida.")

iniciarSistema()