import inspyred


class NMPSO(inspyred.swarm.PSO):
    nm_fitness = None

    def nm(self, population):
        print (population[-1])
        from scipy.optimize import minimize
        p = minimize(self.nm_fitness, population[-1].candidate, method='nelder-mead')
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

