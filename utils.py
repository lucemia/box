# -*- coding: utf-8 -*-
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv


def plotFitness(*fitnesses):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for fitness, c in zip(fitnesses, ('r', 'g', 'b')):
        xs = [k for k in range(len(fitness))]
        ys1 = [f[0] for f in fitness]
        # ys2 = [f[1] for f in fitness]

        ax.scatter(xs, ys1, c=c, marker='o')
        # ax.scatter(xs, ys2, c='b', marker='o')

    ax.set_xlabel('X=f1 Label')
    ax.set_ylabel('y=f2 Label')

    plt.grid(True)
    plt.show()


def plot2D(popu):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    #for p in popu:
    xs = [k.fitness[0] for k in popu]
    ys = [k.fitness[1] for k in popu]

    ax.scatter( xs, ys, c='r', marker='o')

    ax.set_xlabel('X=f1 Label')
    ax.set_ylabel('Y=f2 Label')

    plt.grid(True)
    plt.show()


def plot3D(popu):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    #for p in popu:
    xs = [k.fitness[0] for k in popu]
    ys = [k.fitness[1] for k in popu]
    zs = [k.fitness[2] for k in popu]
    ax.scatter( ys, xs, zs, c='r', marker='o')
    # fitness(*k.candidate)[0] = fitness(k.candidate[0])
    # fitness(*k.candidate)[1] = fitness(k.candidate[1])
    # fitness(*k.candidate)[2] = fitness(k.candidate[2])
    ax.set_xlabel('X=f1 Label')
    ax.set_ylabel('Y=f2 Label')
    ax.set_zlabel('Z=f3 Label')

    plt.show()

    # # output fitness of pareto set to csv file
    # with open('ParetoSet.csv', 'w') as f:
    #     w = csv.writer(f)
    #     for row in zip(xs, ys, zs):
    #         w.writerow(row)

def export(popu, fitness_func):
    with open('ParetoSet.csv', 'w') as f:
        f = csv.writer(f)
        for p in popu:
            var = list(p.candidate)
            fitness = list(p.fitness)
            result = list(fitness_func(*var))

            f.writerow(var + fitness + result)


