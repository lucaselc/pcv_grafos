import numpy as np
import random
import networkx as nx

def inicializarFormigas(num_vertices, num_formigas):
    formigas = []
    for _ in range(num_formigas):
        formiga = list(range(num_vertices))
        random.shuffle(formiga)
        formigas.append(formiga)
    return formigas

def calcularCustoRota(matriz_adjacencia, rota):
    custo = 0
    for i in range(len(rota) - 1):
        custo += matriz_adjacencia[rota[i]][rota[i+1]]
    custo += matriz_adjacencia[rota[-1]][rota[0]]  # Custos de retorno à cidade inicial
    return custo

def atualizarFeromonios(feromonios, formigas, taxa_evaporacao, Q):
    for i in range(len(feromonios)):
        for j in range(i+1, len(feromonios)):
            feromonios[i][j] *= (1.0 - taxa_evaporacao)
            feromonios[j][i] = feromonios[i][j]

    for formiga in formigas:
        contribuicao_formiga = Q / calcularCustoRota(matriz_adjacencia, formiga)
        for i in range(len(formiga) - 1):
            feromonios[formiga[i]][formiga[i+1]] += contribuicao_formiga
            feromonios[formiga[i+1]][formiga[i]] = feromonios[formiga[i]][formiga[i+1]]

    return feromonios

def formigasColoniais(matriz_adjacencia, num_formigas, num_iteracoes, taxa_evaporacao, Q):
    num_vertices = len(matriz_adjacencia)
    feromonios = np.ones((num_vertices, num_vertices))

    melhor_rota = None
    melhor_custo = float('inf')

    for _ in range(num_iteracoes):
        formigas = inicializarFormigas(num_vertices, num_formigas)
        
        for formiga in formigas:
            custo_formiga = calcularCustoRota(matriz_adjacencia, formiga)
            if custo_formiga < melhor_custo:
                melhor_custo = custo_formiga
                melhor_rota = formiga

        feromonios = atualizarFeromonios(feromonios, formigas, taxa_evaporacao, Q)

    return melhor_rota, melhor_custo

if __name__ == "__main__":
    matriz_adjacencia = [
        [0, 4, 8, 15, 2],
        [4, 0, 3, 5, 7],
        [8, 3, 0, 10, 12],
        [15, 5, 10, 0, 18],
        [2, 7, 12, 18, 0]
    ]

    num_formigas = 100
    num_iteracoes = 100
    taxa_evaporacao = 0.5
    Q = 1.0

    melhor_rota, melhor_custo = formigasColoniais(matriz_adjacencia, num_formigas, num_iteracoes, taxa_evaporacao, Q)

    print(f"Rota : {melhor_rota}")
    print(f"Custo da rota: {melhor_custo}")
