from math import *


def c(x):
    return (x - sin(x))/(sin(x) - x*cos(x))


def s(x):
    return x*((sin(x) - x*cos(x))/(2-2*cos(x)-x*sin(x)))


def sb(x):
    return s(x)(1+c(x))


def ss(x):
    return 2*s(x)*(1+c(x))
