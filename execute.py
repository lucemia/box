# -*- coding: utf-8 -*-
from utils import *
from problem import *
from nm_pso import *
import inspyred
from random import *
from time import *

prng = Random()
prng.seed(time())


archive = []
def best_observer(population, num_generations, num_evaluations, args):
    # print len(archive)
    global archive
    # import pdb; pdb.set_trace()
    new_archive = archive
    for ind in population:
        if len(new_archive) == 0:
            new_archive = population[:]
        else:
            should_remove = []
            should_add = True
            for a in new_archive:
                if ind.candidate == a.candidate:
                    should_add = False
                    break
                elif ind < a:
                    should_add = False
                elif ind > a:
                    should_remove.append(a)
            for r in should_remove:
                new_archive.remove(r)
            if should_add:
                new_archive.append(ind)

    archive = new_archive


def execute(model, p, **kwargs):
    ea = model(prng)

    ea.terminator = kwargs.get('terminator')
    ea.topology = kwargs.get('topology')
    ea.observer = kwargs.get('observer')

    final_pop = ea.evolve(
        generator=p.generator,
        evaluator=p.evaluator,
        bounder=p.bounder,
        maximize=p.maximize,
        **kwargs
    )

    return ea, final_pop

ea, final_pop = execute(
    # NMPSO,
    inspyred.swarm.PSO,
    # Gas(),
    # Poloni(),
    # SCH(),
    Viennet(),
    #inspyred.benchmarks.Kursawe(),
    #inspyred.benchmarks.DTLZ6(),
    pop_size=50,
    max_generations=100,
    neighborhood_size=5,
    observer=[best_observer],
    # archiver=best_archiver,
    terminator=inspyred.ec.terminators.generation_termination,
    topology=inspyred.swarm.topologies.ring_topology
)
# print len(final_pop)
print (len(archive))
# export(archive, gas_func)

# plot2D(archive)
plot3D(archive)

