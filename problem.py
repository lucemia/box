# -*- coding: utf-8 -*-
from inspyred.benchmarks import *
import copy
import inspyred
from inspyred import ec
from inspyred.ec import emo
from inspyred.ec import selectors
from inspyred import swarm
import itertools
import math
import random

def gas_func(O2_CH4, GV, T):
    f1 = (86.74 + 14.6*O2_CH4 - 3.06*GV + 18.82*T + 3.14*O2_CH4*GV - 6.91*O2_CH4**2 - 13.31*T**2)*(-8.87*10**-6)
    f2 = (39.46+5.98*O2_CH4 - 2.4*GV + 13.06*T + 2.5*O2_CH4*GV + 1.64*GV*T-3.9*O2_CH4**2-10.15*T**2-3.69*GV**2*O2_CH4) * (-2.152*10**-9)+45.7
    f3 = (1.29-0.45*T-0.112*O2_CH4*GV-0.142*T*GV+0.109*O2_CH4**2+0.405*T**2+0.167*T**2*GV)*4.425*10**-10+0.18

    d = (100-f1)**2 + (50-f2)**2 + (1-f3)**2

    return f1, f2, f3, d ** .5

def Poloni_func(x, y):
    A1 = 0.5*math.sin(1)-2*math.cos(1)+math.sin(2)-1.5*math.cos(2)
    A2 = 1.5*math.sin(1)-math.cos(1)+2*math.sin(2)-0.5*math.cos(2)
    B1 = 0.5*math.sin(x)-2*math.cos(x)+math.sin(y)-1.5*math.cos(y)
    B2 = 1.5*math.sin(x)-math.cos(x)+2*math.sin(y)-0.5*math.cos(y)

    f1 = (1+(A1-B1)**2+(A2-B2)**2)
    f2 = ((x+3)**2+(y+1)**2)

    return f1, f2

def SCH_func(x):
    f1 = (x)**2
    f2 = (x-2)**2
    
    return f1, f2

def Viennet_func(x,y):
    f1 = 0.5*(x**2 + y**2) + math.sin(x**2 + y**2)
    f2 = ((3*x-2*y+4)**2)/8 + ((x-y+1)**2)/27 + 15
    f3 = 1/((x**2+y**2+1)) - 1.1*math.exp(-(x**2+y**2))
    
    return f1, f2, f3

class Gas(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, dimensions=3, objectives=3)
        self.bounder = ec.Bounder([0.25, 10000, 600], [0.55, 20000, 1100])
        self.maximize = True

    def generator(self, random, args):
        return [random.uniform(k[0], k[1]) for k in zip([0.25, 10000, 600], [0.55, 20000, 1100])]

    def evaluator(self, candidates, args):
        fitness = []
        for c in candidates:
            f1, f2, f3, d = gas_func(*c)
            fitness.append(emo.Pareto((f1, f2, 1/f3)))

        return fitness

class Poloni(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, dimensions=2, objectives=2)
        self.bounder = ec.Bounder([-math.pi, -math.pi], [math.pi, math.pi])
        self.maximize = False

    def generator(self, random, args):
        return [random.uniform(-math.pi, math.pi) for _ in range(self.dimensions)]

    def evaluator(self, candidates, args):
        fitness = []
        for c in candidates:
            f1, f2 = Poloni_func(*c)
            fitness.append(emo.Pareto((f1, f2)))
        return fitness

class SCH(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, dimensions=1, objectives=2)
        self.bounder = ec.Bounder([-1000], [1000])
        self.maximize = False

    def generator(self, random, args):
        return [random.uniform(k[0], k[1]) for k in zip([-1000], [1000])]

    def global_optimum(self):
        x = [random.uniform(0, 2) for _ in range(self.objectives - 1)]
        x.extend([0 for _ in range(self.dimensions - self.objectives + 1)])
        return x

    def evaluator(self, candidates, args):
        fitness = []
        for c in candidates:
            f1, f2 = SCH_func(*c)
            fitness.append(emo.Pareto((f1, f2)))

        return fitness

class Viennet(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, dimensions=2, objectives=3)
        self.bounder = ec.Bounder([-3,3], [-3,3])
        self.maximize = False

    def generator(self, random, args):
        return [random.uniform(k[0], k[1]) for k in zip([-3,3], [-3,3])]

    def evaluator(self, candidates, args):
        fitness = []
        for c in candidates:
            f1, f2, f3 = Viennet_func(*c)
            fitness.append(emo.Pareto((f1, f2, f3)))

        return fitness