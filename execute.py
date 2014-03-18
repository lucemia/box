from utils import *
from problem import *
import inspyred
from random import *
from time import *

prng = Random()
prng.seed(time())

def execute(model, p, **kwargs):
    ea = model(prng)

    ea.terminator = kwargs.get('terminator')
    ea.archiver = kwargs.get('archiver')
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
    inspyred.swarm.PSO,
    #Poloni(),
    inspyred.benchmarks.DTLZ2,
    pop_size=100,
    max_generations=300,
    neighborhood_size=5,
    archiver=inspyred.ec.archivers.best_archiver,
    terminator=inspyred.ec.terminators.generation_termination,
    topology=inspyred.swarm.topologies.ring_topology
)

for p in ea.archive:
    print p

plot2D(ea.archive)
