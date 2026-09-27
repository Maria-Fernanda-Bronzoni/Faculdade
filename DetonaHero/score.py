import json
import os
from datetime import datetime

ARQUIVO_RANKING = "ranking.json"  # Arquivo local para salvar o ranking dos melhores tempos
MAX_ITENS = 10  # Limite de registros mantidos no ranking

def salvar_tempo(tempo, nome_jogador="Desconhecido"):
    """ 
    Adiciona o tempo do jogador no ranking, ordena e salva no arquivo JSON.
    nome_jogador é opcional e default é "Desconhecido".
    """
    nome_jogador = nome_jogador.strip() or "Desconhecido"
    registro = {
        "nome": nome_jogador,
        "tempo": tempo,
        "data": datetime.now().strftime("%d/%m/%Y")  # Data do registro
    }

    ranking = ler_ranking()  # Lê ranking atual

    ranking.append(registro)  # Adiciona novo registro
    ranking.sort(key=lambda x: x["tempo"])  # Ordena por tempo (menor é melhor)
    ranking = ranking[:MAX_ITENS]  # Mantém só os top 10

    # Salva ranking atualizado no arquivo JSON com formatação legível
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=4)

def ler_ranking():
    """ Lê o arquivo JSON do ranking e retorna uma lista ordenada por tempo.
        Se o arquivo não existir ou der erro, retorna lista vazia.
    """
    if not os.path.isfile(ARQUIVO_RANKING):
        return []
    try:
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            ranking = json.load(f)
            ranking.sort(key=lambda x: x["tempo"])  # Ordena por tempo só pra garantir
            return ranking
    except Exception:
        return []
