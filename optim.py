# -*- encoding=utf8 -*-

import inspyred
from random import Random
from time import time





def prng(seed=None):
    """
    設定 Random Number, 如果要 debug, 可以將 Seed 設定成固定數字
    """
    prng = Random()
    if not seed:
        seed = time()

    print("set random seed:", seed)

    prng.seed(seed)
    return prng


def generate(random, args):
    """
    初始化 Gene
    references:
        http://inspyred.github.io/tutorial.html#the-generator
        http://inspyred.github.io/tutorial.html#id5
    """

    size = args.get('num_boxes', 10)    

    return random.shuffle(range(size))


def evaluate(candidates, args):
    """
        Multiobjective,
        Try to max the volume and min the distance
    """
    fitness = []
    for cs in candidates:
        # TODO:
        # 1. based on gene, generate box position
        # 2. use physical.py to check the box is stable
        # 3. calcualte the value of these box

        fit = 10
        fitness.append(fit)
    return fitness

from inspyred.ec.variators import crossover, n_point_crossover

@crossover
def order_crossover(random, mom, dad, args):
    # TODO:
    # write custom crossover function
    # implemented a 2-cut order crossover
    # http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/Order1CrossoverOperator.aspx

    offspring = n_point_crossover(random, mom, dad, args)
    # TODO: fix offspring to fit order    
    return offspring

def optim_ga(settings):
    """
    根據設定, 執行 GA, 回傳最佳的結果
    """
    ea = inspyred.ec.GA(prng(settings.get("seed")))
    ea.terminator = inspyred.ec.terminators.evaluation_termination

    final_pop = ea.evolve(
        generator=generate,
        evaluator=evaluate,
        pop_size=settings.get("pop_size", 100),
        maximize=settings.get("maximize", True),
        # bounder=problem.bounder, TODO
        max_evaluations=settings.get("max_evaluatiosn", 30000),
        num_elites=settings.get("num_elites", 1)
    )

    best = max(final_pop)

    return best


def optim_es(settings):
    # TODO use inspyred
    pass


if __name__ == "__main__":
    optim_ga({})