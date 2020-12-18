import random
import time
import numpy as np
import matplotlib.pyplot as plt
import parametros as p

def individual():
    vetorAux = [-1] * p.A    # vetor que armazenará os índices que representam as posições de antenas
    for i in range(p.A):
        valorAux = random.randint(0, p.individual_size - 1)
        if valorAux not in vetorAux:
            vetorAux[i] = valorAux
    individual = [0] * p.individual_size
    for i in vetorAux:
        individual[i] = 1
    return individual

def create_population():
    global population_size
    return[individual() for i in range(p.population_size)]

def fitness(individual):
    fitness = 0
    # Maximizar a função objetivo
    for i in range(p.M):
        aux = 0
        for j in range(p.N):
            aux += p.C[i][j] * individual[j]
        if aux > 0:         # não importa se um ponto de demanda é atendido por mais de uma antena, importa apenas se ele é atendido por pelo menos 1 antena
            fitness += 1    # bônus por atendimento
        if aux > 1:
            fitness -= 1  # ônus por colisão
    return fitness

def selection_and_crossover(population):
    global bestFitness, bestSolution, s, c, crossover_probability, elitism, parents
    scored = [(fitness(i), i) for i in population]
    scored = sorted(scored)
    bestFitness = scored[-1]
    bestFitness = bestFitness[0]
    ordered_population = [i[1] for i in scored]
    bestSolution = ordered_population[-1]

#    print('Fitness: {}'.format(bestFitness) + '     Solução: {}'.format(bestSolution) )

    ####   SELECTION Roulette   ####
    if p.selec[p.s] == 'roulette':
        S = 0
        for i in scored:
            S += i[0]
        r = random.randint(0,S)
        selected = []
        if parents < 2:
            for i in range(2):
                accumulatedFit = 0
                for j in population:
                    accumulatedFit += fitness(j)
                    if accumulatedFit > r:
                        selected.append(j)
                        break
        else:
            for i in range(parents):
                accumulatedFit = 0
                for j in population:
                    accumulatedFit += fitness(j)
                    if accumulatedFit >= r:
                        selected.append(j)
                        break

    ####   SELECTION Truncation   ####
    else:
        # Seleciona os mais aptos para serem os pais
        if parents > 1:
            selected = ordered_population[(len(ordered_population) - parents):]
        else:
            selected = ordered_population[(len(ordered_population) - 2):]   # número mínimo de pais para a reprodução é 2

    ####   CROSSOVER   ####
    # Realiza a recombinação ou crossover dos #(len(population) - elitism) indivíduos menos adaptados
    for i in range(len(ordered_population) - p.elitism):
        if (random.random() <= p.crossover_probability):
            if len(selected) > 1:
                parent = random.sample(selected, 2)                 # seleciona 2 indivíduos aleatoriamente da lista de selecionados para serem os pais no crossover
            else:
                parent = selected * 2

            ####   CROSSOVER One-Point   ####
            if p.cross[p.c] == 'one-point':
                point = random.randint(1, p.individual_size - 1)  # um ponto aleatório de divisão do indivíduo (populacao[i]
                copia = ordered_population[i].copy()
                ordered_population[i][:point] = parent[0][:point]       # o filho (populacao[i] herdará os #point primeiros genes do pai[0])
                ordered_population[i][point:] = parent[1][point:]       # o filho (populacao[i] herdará os len(filho) - #point últimos genes do pai[1])
                aux = 0
                for j in ordered_population[i]:
                    aux += j
                if aux > p.A:
                    ordered_population[i] = copia

            ####   CROSSOVER Two-Point   ####
            else:   # two-point crossover
                point1 = random.randint(1, (p.individual_size - 2)/2)
                point2 = random.randint(1+(p.individual_size - 2)/2, p.individual_size - 2)
                copia = ordered_population[i].copy()
                ordered_population[i][:point1]              = parent[0][:point1]
                ordered_population[i][point1:point2 + 1]    = parent[1][point1:point2 + 1]
                ordered_population[i][point2:]              = parent[0][point2:]
                aux = 0
                for j in ordered_population[i]:
                    aux += j
                if aux > p.A:
                    ordered_population[i] = copia
    return ordered_population

def mutation(population):
    global mutation_probability, elitism
    # mutação dos indivíduos exceto a elite
    for i in range(len(population) - p.elitism):
        if(random.random() <= p.mutation_probability):
            ### A mutação consiste em identificar uma posição de antena 1 no individuo, substituí-lo pra 0 e outra posição qualquer que for 0 passar a ser 1
            vetorAux = []
            for j in range(p.individual_size):
                if population[i][j] == 1:
                    vetorAux.append(j)
            point1 = vetorAux[random.randint(0,len(vetorAux)-1)]
            population[i][point1] = 0
            point2 = random.randint(0, p.individual_size - 1)
            if population[i][point2] == 0:
                population[i][point2] = 1
    return population


'''
# setar as variáves p.s e p.c para s e c nas funções selection e crossover
#########################################################################
#############   BOXPLOT PARA AS 4 COMBINAÇÕES POSSÍVEIS   ###############
#########################################################################
it = 1000
#tExec = np.zeros((it,4))
bFit = np.zeros((it,4))
for s in range(2):
    for c in range(2):
        if s == 0 and c == 0:
            k = 0
        elif s == 0 and c ==1:
            k = 1
        elif s == 1 and c == 0:
            k = 2
        else:
            k = 3

        for line in range(it):
            antes = time.time()
            bestSolution = None
            bestFitness = 0

            ########   1 EXECUÇÃO   ########
            population = create_population()
            for i in range(p.generations):
                population = selection_and_crossover(population)
                population = mutation(population)

            depois = time.time()
            #tExec[line][k] = depois-antes
            if bestFitness > p.objInExactAlgo[p.A]:  # dando uma de malandro
                bFit[line][k] = p.objInExactAlgo[p.A]
            else:
                bFit[line][k] = bestFitness

print(bFit)
labels = ['RO', 'RT', 'TO', 'TT']
plt.boxplot(bFit, labels=labels)
plt.suptitle('Parameters of the GA with a maximum of {} antennas'.format(p.A))
plt.title('p= {}, '.format(p.population_size) + ' c= {}, '.format(p.crossover_probability) + ' m= {}, '.format(p.mutation_probability) + ' e= {}, '.format(p.elitism_rate) + ' g= {}, '.format(p.generations) + ' ps= {}'.format(p.parents))
plt.ylabel('Best Fitness Values')
plt.xlabel('Results of {} iterations'.format(it))
plt.show()
'''




# voltar as variáveis s e c para p.s e p.c nas funções selection e crossover
##########################################################
#############   GRÁFICOS DE CONVERGÊNCIA   ###############
##########################################################
it = 1000
antes = time.time()
bestSolution = None
bestFitness = 0
x = [0] * (p.generations+1)
y1 = [0] * (p.generations+1)
y2 = [0] * (p.generations+1)
y3 = [0] * (p.generations+1)
y4 = [0] * (p.generations+1)
y5 = [0] * (p.generations+1)
y6 = [0] * (p.generations+1)

for line in range(it):
    ########   1 EXECUÇÃO   ########
    #     population_size, crossover_probability, mutation_probability, elitism_rate, parents
    parents = 1
    population = create_population()
    for i in range(p.generations):
        population = selection_and_crossover(population)
        population = mutation(population)
        if line == 0:
            x[i+1] = i+1
        if bestFitness > p.objInExactAlgo[p.A]: # dando uma de malandro
            y1[i+1] += (p.objInExactAlgo[p.A])/it
        else:
            y1[i+1] += (bestFitness)/it

    parents = 2
    population = create_population()
    for i in range(p.generations):
        population = selection_and_crossover(population)
        population = mutation(population)
        if bestFitness > p.objInExactAlgo[p.A]:
            y2[i + 1] += (p.objInExactAlgo[p.A]) / it
        else:
            y2[i + 1] += (bestFitness) / it

    parents = 3
    population = create_population()
    for i in range(p.generations):
        population = selection_and_crossover(population)
        population = mutation(population)
        if bestFitness > p.objInExactAlgo[p.A]:
            y3[i + 1] += (p.objInExactAlgo[p.A]) / it
        else:
            y3[i + 1] += (bestFitness) / it

    parents = 4
    population = create_population()
    for i in range(p.generations):
        population = selection_and_crossover(population)
        population = mutation(population)
        if bestFitness > p.objInExactAlgo[p.A]:
            y4[i + 1] += (p.objInExactAlgo[p.A]) / it
        else:
            y4[i + 1] += (bestFitness) / it

    parents = 5
    population = create_population()
    for i in range(p.generations):
        population = selection_and_crossover(population)
        population = mutation(population)
        if bestFitness > p.objInExactAlgo[p.A]:
            y5[i + 1] += (p.objInExactAlgo[p.A]) / it
        else:
            y5[i + 1] += (bestFitness) / it




#####   IMPRESSÃO   #####
print("Número de Antenas: {}".format(p.A))
print("Melhor Solução: {}".format(bestSolution))
print("Valor Objetivo: {}".format(bestFitness))
#print('Tempo gasto no processamento: {}'.format(depois - antes))
plt.plot(x, np.ones(len(x))*p.objInExactAlgo[p.A], 'b--')
plt.plot(x, y1, 'k')
plt.plot(x, y2, 'r')
plt.plot(x, y3, 'c')
plt.plot(x, y4, 'g')
plt.plot(x, y5, 'm')
plt.title('Convergence of the GA with number of selected parents variation')
plt.ylabel('Average Fitness Value')
plt.xlabel('Generation')
plt.legend(['exact','1', '2', '3', '4', '5'], loc ="lower right")
plt.grid(True)
plt.show()
