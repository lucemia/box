import inspyred
from inspyred import ec
import random

# http://fonnesbeck.github.io/ScipySuperpack/
# http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html
# Nelder-Mead

#ruten random float
#random.uniform(k[0], k[1])
prng = random.Random()

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
    return ec.emo.Pareto([f1, f2 *2, 1/f3 * 100])
    #return ec.emo.Pareto([f1, f2, f3], [True, True, False])
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


class NMPSO(inspyred.swarm.PSO):
    def nm(self, population):
        from scipy.optimize import minimize
        p = minimize(nm_fitness, population[-1].candidate, method='nelder-mead')
        #[-1] with n+1
        O2_CH4, GV, T = p.x[0], p.x[1], p.x[2]

        ind = inspyred.ec.Individual([O2_CH4, GV, T], maximize=self.maximize)
        # import pdb; pdb.set_trace()
        #maximize=find max )

        ind.candidate = bound(ind.candidate, self._kwargs)
        ind.fitness = my_evaluator([ind.candidate], self._kwargs)[0]
        #print (ind.fitness)
        return ind


    def _swarm_replacer(self, random, population, parents, offspring, args):
        n = int(( len(population) - 1 ) / 3)
        # print [(k.candidate, k.fitness) for k in population]

        # import pdb; pdb.set_trace()
        # the offspring is produced by PSO
        population_offspring = list(zip(population, offspring))
        import pdb; pdb.set_trace()
        population_offspring.sort(key=lambda i:i[0], reverse=True)
        #define by individual ,i[0]=pop,offspring

        # the n elite
        population_new = [k[0] for k in population_offspring[:n]]

        # the nm is generate by n+1 population
        population_new.append(self.nm([k[0] for k in population_offspring[:n+1]]))
        population_new.extend([k[1] for k in population_offspring[n+1:]])

        self._previous_population = [k[0] for k in population_offspring]

        return population_new


def run_nm_pso():
    ea = NMPSO(prng)
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    ea.topology = inspyred.swarm.topologies.ring_topology

    final_pop = ea.evolve(
        generator=generator,
        evaluator=my_evaluator,
        pop_size=7,
        bounder=bound,
        maximize=True,
        max_evaluations=100,
        neighborhood_size=5
    )

    #print final_pop

    best = max(final_pop)
    # print('Best Solution: \n{0}'.format(str(best)))

    return final_pop

"""
def run_ga():
     ea = inspyred.ec.GA(prng)
     ea.terminator = inspyred.ec.terminators.evaluation_termination
     final_pop = ea.evolve(
         generator=generator,
         evaluator=my_evaluator,
         pop_size=6,
         maximize=True,
         bounder=bound,
         max_evaluations=100,
         num_elites=1)
     print (final_pop)

     best = max(final_pop)
     print('Best Solution: \n{0}'.format(str(best)))

     return final_pop
"""
def run_pso():
    ea = inspyred.swarm.PSO(prng)
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    ea.topology = inspyred.swarm.topologies.ring_topology

    final_pop = ea.evolve(
        generator=generator,
        evaluator=my_evaluator,
        pop_size=6,
        bounder=bound,
        maximize=True,
        max_evaluations=100,
        neighborhood_size=5
    )

    #print final_pop

    best = max(final_pop)
    # print('Best Solution: \n{0}'.format(str(best)))

    return final_pop

popu = run_nm_pso()
#p =
for p in popu:
    print ("Particle=")
    print (p,fitness(*p.candidate))
    #print (p,fitness(*p.candidate))

#print (max(popu))
best = max(popu)

print (best, fitness(*best.candidate))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = fitness(*best.candidate)[0]
    ys = fitness(*best.candidate)[1]
    zs = fitness(*best.candidate)[2]
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('X=f1 Label')
ax.set_ylabel('Y=f2 Label')
ax.set_zlabel('Z=f3 Label')

plt.show()

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
