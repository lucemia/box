# -*- coding: utf-8 -*-
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
import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel("ERROR")

#-----------------------------------------------------------------------
#                               nm-pso
#-----------------------------------------------------------------------

def _op(candidate_a, candidate_b, var):
    return map(lambda a, b: a + var * (a - b), candidate_a, candidate_b)

def _ind(candidate, maximize, fitness):
    ind = ec.Individual(candidate, maximize=maximize)
    ind.fitness = fitness
    return ind

class NMPSO(inspyred.swarm.PSO):
    # def __init__(self, rand):

    #     super(inspyred.swarm.PSO, self).__init__(rand)
    #     self._swarm_variator = self.variator
    #     self.variator = self._nm_swarm_variator

    def _swarm_variator(self, random, candidates, args):
        popu_size = len(candidates)
        n = int(( popu_size - 1 ) / 3)

        # import pdb; pdb.set_trace()
        offspring = super(NMPSO, self)._swarm_variator(random, candidates, args)
        temp = [(self._previous_population[k], k) for k in range(popu_size)]

        temp.sort(reverse=True)
        rank = [k[1] for k in temp]

        # print rank
        # the n previous parents will remain not change
        for index in rank[:n]:
            offspring[index] = self._previous_population[index].candidate

        # the n + 1 use nm

        self._t = 10
        offspring[n+1] = self.nm([self._previous_population[index] for index in rank[:n+1]], args).candidate
        offspring[n+1] = self.bounder(offspring[n+1], args)
        # the remain use pso
        return offspring

    def nm(self, population, args):
        alpha = args.setdefault('alpha', 1)
        gamma = args.setdefault('gamma', 2)
        sigma = args.setdefault('sigma', 0.5)
        rho = args.setdefault('rho', -0.5)
        # theta = args.setdefault('theta', 0.1)

        fitness = lambda ind: self.evaluator([ind], args)[0]

        # http://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method

        popu_size = len(population)
        # 1. Order according to the values at the vertices
        population.sort(reverse=True)

        # print population
        # x = raw_input()
        # Stopping Criterion
        self._t -= 1
        if not self._t > 0:
            logger.info("DONE")
            return population[0]

        # 2. Calculate X0, the center of gravity of all points except Xn+1
        # import pdb; pdb.set_trace()

        X_0 = [sum(k) / (popu_size-1) for k in zip(*(p.candidate for p in population[:-1]))]

        # the Xn+1
        X_N_1 = population[-1].candidate
        # 3. Reflection
        # Compute the reflected point
        X_R = _op(X_0, X_N_1, alpha)
        X_1 = population[0].candidate
        X_N = population[-2].candidate
        # fit_reflection = evaluate(X_R)

        ind_N_1 = _ind(X_N_1, self.maximize, fitness(X_N_1))
        ind_R = _ind(X_R, self.maximize, fitness(X_R))
        ind_1 = _ind(X_1, self.maximize, fitness(X_1))
        ind_N = _ind(X_N, self.maximize, fitness(X_N))
        ind_0 = _ind(X_0, self.maximize, fitness(X_0))

        # import pdb; pdb.set_trace()


        # if the reflected point is better than the second worst, but not better than the best
        # then obtain a new simplex by replacing the worst point Xn+1 with the reflected point Xr
        # and go to step 1
        # print fitness(X_0), fitness(X_R), fitness(X_N)
        # raw_input()
        if ind_1 >= ind_R > ind_N:
            population[-1] = ind_R
            logger.info("reflection")
            # print "reflection"
            return self.nm(population, args)

        # 4. Expansion
        # if the reflected point is the best point so far
        elif ind_R > ind_1:
            # x = raw_input()

            # then compute the expanded point
            X_E = _op(X_0, X_N_1, gamma)
            ind_E = _ind(X_E, self.maximize, fitness(X_E))
            logger.info("expansion")
            # print "expansion"

            # if the expanded point is better than the reflected point
            if ind_E > ind_R:
                # then obtain a new simplex by replacing the
                # worst point Xn+1 with the expanded point Xe, and go to step 1.
                population[-1] = ind_E
                return self.nm(population, args)
            else:
                # else obtain a new simplex by replacing the worst point Xn+1
                # with the reflected point Xr and go to step 1.
                population[-1] = ind_R
                return self.nm(population, args)
        # 5. Contraction
        # Here, it is certain that
        elif ind_R <= ind_N:
            logger.info("contraction")
            # print "contraction"
            # Compute contracted point
            X_C = _op(X_0, X_N_1, rho)
            ind_C = _ind(X_C, self.maximize, fitness(X_C))

            # if the contracted point is better than the worst point
            if ind_C > ind_N_1:
                # then obtain a new simplex by replacing the worst point
                # Xn+1 with the contracted point Xc and go to step 1.
                population[-1] = ind_C
                return self.nm(population, args)

            # else go to step 6.
            # 6. Reduction / Shrink
            else:
                logger.info("reduction")
                # print "reduction"
                # for all but the best point
                # replace the point with
                new_population = []
                new_population.append(population[0])

                for popu in population[1:]:
                    X_I = _op(X_1, popu.candidate, sigma)
                    new_population.append(_ind(X_I, self.maximize, fitness(X_I)))

                # goto step 1.
                return self.nm(new_population, args)


