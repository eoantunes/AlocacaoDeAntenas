import pygad
import numpy
import parametros as p
import random
import matplotlib.pyplot as plt

"""This script try to reproduce the old implemantion of the GA.py file.
   The python package used was the PyGAD(https://pygad.readthedocs.io/en/latest/index.html ).
   All the information about the execution is in the PyGad documentation.
"""

def individual():
    """Create an individual as a vector of size 'individual_size' and alocate randomly
       the positions(index) of the 'numb_antennas' antennas, represented as 1 in the vector.

       Returns:
            A vector of 'individual_size' composed by zeros and 'numb_antennas' 1s. 
    """
    vetorAux = [-1] * p.A
    for i in range(p.A):
        valorAux = random.randint(0, p.individual_size - 1)
        if valorAux not in vetorAux:
            vetorAux[i] = valorAux
    individual = [0] * p.individual_size
    for i in vetorAux:
        individual[i] = 1

    return individual

def fitness(solution, solution_idx):
    """Responsible for generate the fitness value from the solution(individual).

       Args:
            solution: The input solution(indivdual).
            solution_idx: The index inside de population.

       Returns:
            The interger values of the fitness value.
    """
    fitness = 0
    for i in range(p.M):
        aux = 0
        for j in range(p.N):
            aux += p.C[i][j] * solution[j]
        if aux > 0:        
            fitness += 1    
        if aux > 1:
            fitness -= 1
    return fitness

def create_population():
    """Create the population of individuals.

       Returns:
            A vector of vectors where each line represents a individual.
    """
    return[individual() for i in range(p.population_size)]

last_fitness = 0
i_global = 0
y = numpy.zeros((5, p.generations))
x = numpy.arange(p.generations)
def callback_generation(ga_instance):
    """CallBack to access the information during the optmization
    """
    global last_fitness
    print("--------------------------------------------------------------")
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution()[1] - last_fitness))
    print("--------------------------------------------------------------")
    last_fitness = ga_instance.best_solution()[1]

    best_fitness = ga_instance.best_solution()[1]
    if best_fitness > p.objInExactAlgo[p.A]:
        y[i_global-1][ga_instance.generations_completed-1] += (p.objInExactAlgo[p.A])/p.generations
    else:
        y[i_global-1][ga_instance.generations_completed-1] += (best_fitness)/p.generations

# Creating an instance of the GA class inside the ga module. Some parameters are initialized within the constructor.
# To see all the parameters check PyGAD GA module on (https://pygad.readthedocs.io/en/latest/README_pygad_ReadTheDocs.html#pygad-ga-class)

# Running the GA to optimize the parameters of the function.
for i in range(1, len(['k', 'r', 'c', 'g', 'm'])+1):
    i_global = i
    ga_instance = pygad.GA(num_generations=p.generations,
                           num_parents_mating=p.parents,
                           fitness_func=fitness,
                           initial_population=create_population(),
                           num_genes=p.N,
                           parent_selection_type=p.parent_selection_type,
                           keep_parents=i,
                           crossover_type=p.crossover_type,
                           mutation_type=p.mutation_type,
                           mutation_percent_genes=p.mutation_probability,
                           on_generation=callback_generation)
    
    ga_instance.run()

#####    IMPRESSÃO    #####
#print('Tempo gasto no processamento: {}'.format(depois - antes))
plt.plot(x, numpy.ones(len(x))*p.objInExactAlgo[p.A], 'b--')
plt.plot(x, y[0]*100, 'k')
plt.plot(x, y[1]*100, 'r')
plt.plot(x, y[2]*100, 'c')
plt.plot(x, y[3]*100, 'g')
plt.plot(x, y[4]*100, 'm')
plt.title('Convergence of the GA with number of selected parents variation')
plt.ylabel('Average Fitness Value')
plt.xlabel('Generation')
plt.legend(['exact','1', '2', '3', '4', '5'], loc ="lower right")
plt.grid(True)
plt.show()


# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))
