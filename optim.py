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

    print "set random seed", seed

    prng.seed(seed)
    return prng


def generate(random, args):
    """
    初始化 Gene
    references:
        http://inspyred.github.io/tutorial.html#the-generator
        http://inspyred.github.io/tutorial.html#id5
    """



    return


def evaluate(candidates, args):
    """
        Multiobjective,
        Try to max the volume and min the distance
    """
    # TODO:
    return


def optim_ga(settings):
    """
    根據設定, 執行 GA
    """
    ea = inspyred.ec.GA(prng())
    ea.terminator = inspyred.ec.terminators.evaluation_termination

    final_pop = ea.evolve(
        generator=generate,
        evaluator=generate,
        pop_size=100,
        maximize=True,
        # bounder=problem.bounder, TODO
        max_evaluations=30000,
        num_elites=1
    )

    best = max(final_pop)

    return best


def optim_es(settings):
    # TODO use inspyred
    pass
