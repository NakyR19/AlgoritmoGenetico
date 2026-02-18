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

    def __init__(self, matriz_distancias, tam_pop=100, prob_mutacao=0.01, num_geracoes=100):
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

    def _fitness(self, pop):
        # calcula o fitness (dist total), quanto menor melhor
        dist = 0
        for i in range(self.num_cidades - 1):
            dist += self.matriz_distancias[pop[i], pop[i+1]]
        dist += self.matriz_distancias[pop[-1], pop[0]]   # volta p/ cidade inicial
        return dist

    def weighted_by(self, population):
        # Fitness Proportionate Selection
        # invertemos o fitness pois menor distância é melhor
        fit_val = [self._fitness(ind) for ind in population]
        # menor distância -> maior peso
        weights = [1.0 / (f + 1e-10) for f in fit_val]   # o 1e-10 faz com q evita divisão por zero
        return weights

    def reproduce(self, parent1, parent2):
        """
        Cruzamento com Ordem Preservada (OX1 - Order Crossover)
        Parte do primeiro pai é copiada, e o resto é preenchido com genes do segundo pai
		mantendo a ordem, omitindo genes já presentes
        """
        n = len(parent1)
        c = random.randint(1, n - 1)   # ponto de corte entre 1 e n-1

        # prefixo de parent1 ate c + sufixo de parent2 de c+1 em diante
        aux_filho = parent1[:c] + parent2[c:]

        # tira duplicatas e insere cidades faltantes, crossover de um ponto n preserva permutações
        faltante = set(parent1) - set(aux_filho)
        check = set()
        filho = []
        for cidade in aux_filho:
            if cidade not in check:
                check.add(cidade)
                filho.append(cidade)
            else:
                # caso de cidade repetida, substitui pela primeira cidade faltante
                cidade = faltante.pop()
                check.add(cidade)
                filho.append(cidade)
        # se faltar cidades, inseriinserendo no final
        if faltante:
            filho.extend(faltante)
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
            weights = self.weighted_by(pop)

            # cria nova pop vazia
            pop2 = []

            # gera cada filho individualmente
            for i in range(self.tam_pop):
                # seleciona dois pais com base nos pesos
                parent1, parent2 = random.choices(pop, weights=weights, k=2)

                # crossover
                filho = self.reproduce(parent1, parent2)

                # mutacao
                filho = self.mutate(filho)

                # add filho a nova pop
                pop2.append(filho)

            # substitui população antiga pela nova
            pop = pop2

            # armazena o melhor indivíduo da geração
            melhor_na_geracao = min(pop, key=lambda ind: self._fitness(ind))
            melhor_fit = self._fitness(melhor_na_geracao)
            historico.append(melhor_fit)
            if melhor_fit < melhor_fit_geral:
                melhor_fit_geral = melhor_fit
                melhor_geral = melhor_na_geracao.copy()

        return melhor_geral, melhor_fit_geral, historico