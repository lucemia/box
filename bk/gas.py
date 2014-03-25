import inspyred
from inspyred import ec
import unittest
import random
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import csv

# http://fonnesbeck.github.io/ScipySuperpack/
# http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html
# Nelder-Mead

#ruten random float
#random.uniform(k[0], k[1])
prng = random.Random()


def plot(popu):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    #for p in popu:
    xs = [fitness(*k.candidate)[0] for k in popu]
    ys = [fitness(*k.candidate)[1] for k in popu]
    zs = [fitness(*k.candidate)[2] for k in popu]
    ax.scatter( ys, xs, zs, c='r', marker='o')
    # fitness(*k.candidate)[0] = fitness(k.candidate[0])
    # fitness(*k.candidate)[1] = fitness(k.candidate[1])
    # fitness(*k.candidate)[2] = fitness(k.candidate[2])
    ax.set_xlabel('X=f1 Label')
    ax.set_ylabel('Y=f2 Label')
    ax.set_zlabel('Z=f3 Label')

    plt.show()

    with open('fitnessPoint.csv', 'w') as f:
        w = csv.writer(f)
        for row in zip(xs, ys, zs):
            w.writerow(row)


def fitness(O2_CH4, GV, T):
    f1 = (86.74 + 14.6*O2_CH4 - 3.06*GV + 18.82*T + 3.14*O2_CH4*GV - 6.91*O2_CH4**2 - 13.31*T**2)*(-8.87*10**-6)
    f2 = (39.46+5.98*O2_CH4 - 2.4*GV + 13.06*T + 2.5*O2_CH4*GV + 1.64*GV*T-3.9*O2_CH4**2-10.15*T**2-3.69*GV**2*O2_CH4) * (-2.152*10**-9)+45.7
    f3 = (1.29-0.45*T-0.112*O2_CH4*GV-0.142*T*GV+0.109*O2_CH4**2+0.405*T**2+0.167*T**2*GV)*4.425*10**-10+0.18

    d = (100-f1)**2 + (50-f2)**2 + (1-f3)**2

    return f1, f2, f3, d ** .5

#do evaluate fitness function
@inspyred.ec.evaluators.evaluator
def my_evaluator(candidate, args):
    O2_CH4, GV, T = candidate
    f1, f2, f3, d = fitness(O2_CH4, GV, T)

    # return -d
    return ec.emo.Pareto([f1, f2, 1/f3])
    # return -d
    # return ec.emo.Pareto([f1, f2, f3], [True, True, False])
    # without normalize [f1, f2, f3] , normalize [f1, f2*2, f3*100]

lower_bound = [0.25, 10000, 600]
upper_bound = [0.55, 20000, 1100]

def generator(random, args):
    #  random, args
    return [random.uniform(k[0], k[1]) for k in zip(lower_bound, upper_bound)]

bound = ec.Bounder(lower_bound, upper_bound)

def nm_fitness(ind):
    # import pdb; pdb.set_trace()
    return fitness(ind[0], ind[1], ind[2])[-1]

def cmp(i, j):
    if i > j:return 1
    elif j > i: return -1
    return 0


class NMPSO(inspyred.swarm.PSO):
    def nm(self, population):
        print (population[-1])
        from scipy.optimize import minimize
        p = minimize(nm_fitness, population[-1].candidate, method='nelder-mead')
        # import pdb; pdb.set_trace()
        # population[-1].candidate = use last population candidate as default value
        ind = inspyred.ec.Individual([float(k) for k in p.x], maximize=self.maximize)
        # import pdb; pdb.set_trace()
        #maximize=find max )

        ind.candidate = bound(ind.candidate, self._kwargs)
        ind.fitness = my_evaluator([ind.candidate], self._kwargs)[0]

        #print (ind.fitness)
        return ind


    def _swarm_replacer(self, random, population, parents, offspring, args):
        # import pdb; pdb.set_trace()

        n = int(( len(population) - 1 ) / 3)
        # print [(k.candidate, k.fitness) for k in population]

        # population.sort(reverse=True)
        # import pdb; pdb.set_trace()
        # the offspring is produced by PSO
        # print(population)
        # print(offspring)
        population_offspring = list(zip(population, offspring))
        # import pdb; pdb.set_trace()
        #print
        # TODO:
        print ([k[0] for k in population_offspring])
        population_offspring.sort(reverse=True)
        #define by individual ,i[0]=pop,offspring
        print ([k[0] for k in population_offspring])
        # the n elite
        population_new = [k[0] for k in population_offspring[:n]]

        # the nm is generate by n+1 population
        population_new.append(self.nm([k[0] for k in population_offspring[:n+1]]))
        population_new.extend([k[1] for k in population_offspring[n+1:]])

        self._previous_population = [k[0] for k in population_offspring]

        return population_new


def run_pso(model, pop_size=10, generation=500):
    ea = model(prng)
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    ea.topology = inspyred.swarm.topologies.ring_topology

    final_pop = ea.evolve(
        generator=generator,
        evaluator=my_evaluator,
        pop_size=pop_size,
        bounder=bound,
        maximize=True,
        max_evaluations=pop_size *generation,
        neighborhood_size=5
    )

    return final_pop

PSO = inspyred.swarm.PSO

# popu = run_pso(PSO, 7, 30)
# popu = run_pso(NMPSO, 100, 300)

total_popu = []
for i in range(1):
    popu = run_pso(NMPSO, 3, 4)
    total_popu.extend(popu)
    # add popu plot point in total_popu

plot(total_popu)




# for p in popu:
#     print ("Particle=")
#     print (p,fitness(*p.candidate))
#     print (p,fitness(*p.candidate))

# print (max(popu))
# best = max(popu)

# print (best, fitness(*best.candidate))



# popu = run_pso()
# best = max(popu)
# print best, fitness(best.candidate[0], best.candidate[1], best.candidate[2])


# import pdb; pdb.set_trace()

# print fitness(0.55, 20000.0, 1099.8115398083803)

# fitness(0.5371872730661065, 19825.600047903703, 915.8655694070546)
# print fitness(0.413131, 18776, 894.659)
# print fitness(0.420981, 18978, 883.274)
# print fitness(0.294829, 10054.5, 916.267), [99.131, 45.9225, 0.803374,4.1737]
# print fitness(0.269169, 10028.6, 837.061), [82.7591, 44.4307, 0.698872, 18.1232]
# print fitness(0.253618, 10014.8, 706.612), [59.0164, 44.4179, 0.549171, 41.3701]
# print fitness(0.439771, 18269.1, 900.941), [95.9281, 45.3552, 1.27496, 6.1807]
# print fitness(0.422193, 18900.2, 885.426), [92.678, 45.3857, 1.27409, 8.6573]
# print fitness(0.412634, 19011.5, 872.664), [90.0384, 45.3724, 1.24901, 10.9885]

# print fitness(0.5446067301314228, 19043.41815339666, 922.2253699200469)
