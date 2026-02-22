import random
import numpy as np

class ga:
    """
    Adaptação realizada em cima do pseudocódigo e do código do tsp_populacional
    pseudocódigo:
        function GENETIC-ALGORITHM(population, fitness) returns an individual
            repeat
                weights ← WEIGHTED-BY(population, fitness)
                population2 ← empty list
                for i = 1 to SIZE(population) do
                    parent1, parent2 ← WEIGHTED-RANDOM-CHOICES(population, weights, 2)
                    child ← REPRODUCE(parent1, parent2)
                    if (small random probability) then child ← MUTATE(child)
                    add child to population2
                population ← population2
            until some individual is fit enough, or enough time has elapsed
            return the best individual in population, according to fitness
            
        function REPRODUCE(parent1,parent2) returns an individual
            n->LENGTH(parent1)
            c->random number from 1 to n
            return APPEND(SUBSTRING(parent1,1,c), SUBSTRING(parent2,c+1,n))
    """

    def __init__(self, matriz_distancias, tam_pop=100, prob_mutacao=0.01, num_geracoes=100, elite_size=2):
        """
            matriz_distancias: matriz de distâncias
            tam_pop: tamanho da população
            prob_mutacao: probabilidade de mutação
            num_geracoes: número de gerações
        """
        self.matriz_distancias = matriz_distancias
        self.num_cidades = matriz_distancias.shape[0]
        self.tam_pop = tam_pop
        self.prob_mutacao = prob_mutacao
        self.num_geracoes = num_geracoes
        self.elite_size = elite_size

    def _fitness(self, ind):
        # calcula o fitness (dist total), quanto menor melhor
        # cria uma lista de idx para pegar a distância entre as cidades i e i+1
        idx_origem = ind
        idx_destino = np.roll(ind, -1) # volta à primeira cidade
        return np.sum(self.matriz_distancias[idx_origem, idx_destino])

    def weighted_by(self, population):
        # Fitness Proportionate Selection
        # invertemos o fitness pois menor distância é melhor
        fit_val = [self._fitness(ind) for ind in population]
        # menor distância -> maior peso
        weights = [1.0 / (f + 1e-10) for f in fit_val]   # o 1e-10 faz com q evita divisão por zero
        return weights, fit_val

    def reproduce(self, parent1, parent2):
        """
        Cruzamento com Ordem Preservada (OX1 - Order Crossover)
        Parte do primeiro pai é copiada, e o resto é preenchido com genes do segundo pai
		mantendo a ordem, omitindo genes já presentes
        """
        n = len(parent1)
        c = random.randint(1, n - 1)   # ponto de corte entre 1 e n-1

        # SUBSTRING(parent1, 1, c)
        filho = parent1[:c]
        
        # SUBSTRING(parent2, c, n) + início, filtrando duplicatas
        # garante que o filho tenha todos os genes sem repetir os de parent1[:c]
        set_filho = set(filho)
        for cidade in parent2:
            if cidade not in set_filho:
                filho.append(cidade)
        
        return filho

    def mutate(self, filho):
        """
        Operador de mutação por inversão de segmento
        """
        if random.random() < self.prob_mutacao:
            # seleciona dois pontos e inverte o trecho entre eles
            i, j = sorted(random.sample(range(len(filho)), 2))
            # inverte o segmento
            filho[i:j+1] = filho[i:j+1][::-1]
        return filho

    def run(self, pop_inicial=None):

        if pop_inicial is None:
            pop = [random.sample(range(self.num_cidades), self.num_cidades)
                          for _ in range(self.tam_pop)]
        else:
            pop = pop_inicial
            self.tam_pop = len(pop)

        melhor_geral = None
        melhor_fit_geral = float('inf')
        historico = []

        for generation in range(self.num_geracoes):
            # calcula pesos
            weights, fit_vals = self.weighted_by(pop)

            # encontra o melhor da geração atual
            min_idx = np.argmin(fit_vals)
            if fit_vals[min_idx] < melhor_fit_geral:
                melhor_fit_geral = fit_vals[min_idx]
                melhor_geral = list(pop[min_idx])
            
            historico.append(melhor_fit_geral)

            # ordena a população pelo fitness (qnt menor melhor)
            pop_ordenada = [x for _, x in sorted(zip(fit_vals, pop), key=lambda pair: pair[0])]
            pop2 = pop_ordenada[:self.elite_size]

            # reprod
            while len(pop2) < self.tam_pop:
                parent1, parent2 = random.choices(pop, weights=weights, k=2)
                filho = self.reproduce(parent1, parent2)
                filho = self.mutate(filho)
                pop2.append(filho)

            pop = pop2

        return melhor_geral, melhor_fit_geral, historico