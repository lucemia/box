# -*- coding: utf-8 -*-
from utils import *
from problem import *
from nm_pso import *
import inspyred
from random import *
from time import *

prng = Random()
prng.seed(time())

def execute(model, p, **kwargs):
    ea = model(prng)

    ea.terminator = kwargs.get('terminator')
    # ea.archiver = kwargs.get('archiver')
    ea.topology = kwargs.get('topology')

    final_pop = ea.evolve(
        generator=p.generator,
        evaluator=p.evaluator,
        bounder=p.bounder,
        maximize=p.maximize,
        **kwargs
    )

    return ea, final_pop

ea, final_pop = execute(
    NMPSO,
    # inspyred.swarm.PSO,
    Gas(),
    # Poloni(),
    #SCH(),
    #Viennet(),
    #inspyred.benchmarks.Kursawe(),
    #inspyred.benchmarks.DTLZ6(),
    pop_size=50,
    max_generations=10,
    neighborhood_size=5,
    # archiver=inspyred.ec.archivers.best_archiver,
    terminator=inspyred.ec.terminators.generation_termination,
    topology=inspyred.swarm.topologies.ring_topology
    #import pdb; pdb.set_trace()
)
print len(final_pop)

# export(ea.archive, gas_func)



#plot2D(ea.archive)
plot3D(ea.archive)

