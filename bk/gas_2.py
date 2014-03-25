import inspyred
from inspyred import ec
import random
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import problem

# http://fonnesbeck.github.io/ScipySuperpack/
# http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html
# Nelder-Mead

#ruten random float
#random.uniform(k[0], k[1])
prng = random.Random()

def plot2D(popu):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    #for p in popu:
    xs = [k.fitness[0] for k in popu]
    ys = [k.fitness[1] for k in popu]

    ax.scatter( ys, xs, c='r', marker='o')

    ax.set_xlabel('X=f1 Label')
    ax.set_ylabel('Y=f2 Label')


    plt.show()


def run_pso(pop_size=100, generation=300):
    p = problem.Poloni()

    # ea = inspyred.swarm.PSO(prng)
    ea = inspyred.ec.emo.PAES(prng)

    ea.terminator = inspyred.ec.terminators.evaluation_termination
    ea.topology = inspyred.swarm.topologies.ring_topology

    final_pop = ea.evolve(
        generator=p.generator,
        evaluator=p.evaluator,
        pop_size=pop_size,
        bounder=p.bounder,
        maximize=p.maximize,
        archiver=p.archiver,
        max_evaluations=pop_size*generation,
        neighborhood_size=5,
        max_archive_size=100,
    )

    #print final_pop

    best = min(final_pop)
    # print('Best Solution: \n{0}'.format(str(best)))
    return final_pop

#popu = run_nm_pso()
popu = run_pso()
#p =
for p in popu:
    print ("Particle=")


plot2D(popu)

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
