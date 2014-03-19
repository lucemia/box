import collections
import copy
import inspyred
import math
import random
from inspyred import ec
import unittest
from random import *
from time import *
from problem import *

#-----------------------------------------------------------------------
#                               nm-pso
#-----------------------------------------------------------------------

def nm_fitness(ind):
    # import pdb; pdb.set_trace()
    return fitness(ind[0], ind[1], ind[2])[-1]

class NMPSO(inspyred.swarm.PSO):

    def nm(self, population):
        #return population[-1]
        from scipy.optimize import minimize
        p = minimize(nm_fitness, population[-1].candidate, method='nelder-mead')
        # population[-1].candidate = use last population candidate as 初始值
        #import pdb; pdb.set_trace()
        O2_CH4, GV, T = p.x[0], p.x[1], p.x[2]
        ind = inspyred.ec.Individual([O2_CH4, GV, T], maximize=self.maximize)
        # import pdb; pdb.set_trace()
        # maximize = find max for ind
        # redefine a new bound for nm , do not use old bound
        ind.candidate = bound(ind.candidate, self._kwargs)
        ind.fitness = my_evaluator([ind.candidate], self._kwargs)[0]
        #print (ind) 
        return ind


    def _swarm_replacer(self, random, population, parents, offspring, args):
        n = int(( len(population) - 1 ) / 3)
        # print [(k.candidate, k.fitness) for k in population]
        # import pdb; pdb.set_trace()
        # the offspring is produced by PSO , it is use to replace
        population_offspring = list(zip(population, offspring))
        population_offspring.sort(key=lambda i:i[0], reverse=True)
        # define by individual , i[0] = pop,offspring

        # the n elite
        population_new = [k[0] for k in population_offspring[:n]]
        #print (population_new[0])
        # the nm is generate by n+1 population
        population_new.append(self.nm([k[0] for k in population_offspring[:n+1]]))
        population_new.extend([k[1] for k in population_offspring[n+1:]])

        self._previous_population = [k[0] for k in population_offspring]

        return population_new
