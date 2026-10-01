class Nodo:
    def __init__(self, sigla, nome):
        self.sigla = sigla
        self.nome = nome
        self.proximo = None

class TabelaHash:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho

    def funcao_hash(self, sigla):
        if sigla == "DF":
            return 7

        primeira = ord(sigla[0])
        segunda = ord(sigla[1])

        return (primeira + segunda) % self.tamanho

    def inserir(self, sigla, nome, posicao):
        novo = Nodo(sigla, nome)

        if self.tabela[posicao] is None:
            self.tabela[posicao] = novo
        else:
            novo.proximo = self.tabela[posicao]
            self.tabela[posicao] = novo

    def imprimir(self):
        for i in range(self.tamanho):
            atual = self.tabela[i]

            if atual is None:
                print(f"Posição {i}: None")
                continue

            resultado = []

            while atual is not None:
                resultado.append(atual.sigla)
                atual = atual.proximo

            print(f"Posição {i}: {' -> '.join(resultado)}")

estados = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins")
]

tabela = TabelaHash(10)

print("Tabela antes das inserções:")
tabela.imprimir()

for sigla, nome in estados:
    posicao = tabela.funcao_hash(sigla)
    tabela.inserir(sigla, nome, posicao)

print("\nTabela depois das inserções:")
tabela.imprimir()

sigla = "MF"
nome = "Maria Fernanda"

posicao = tabela.funcao_hash(sigla)
tabela.inserir(sigla, nome, posicao)

print("\nTabela depois do estado fictício:")
tabela.imprimir()