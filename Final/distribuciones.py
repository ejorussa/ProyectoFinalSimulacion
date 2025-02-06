import math
import random


def normal(rnd1, rnd2, media, de, formula):
    if formula == 1:
        rnd1 = random.random()
        rnd2 = random.random()
        n1 = (pow(-2 * math.log(rnd1), 1 / 2) * math.cos(2 * math.pi * rnd2)) * de + media
        return rnd1, rnd2, n1, 2
    elif formula == 2:
        n2 = (pow(-2 * math.log(rnd1), 1 / 2) * math.sin(2 * math.pi * rnd2)) * de + media
        return rnd1, rnd2, n2, 1
