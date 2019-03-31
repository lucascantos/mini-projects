from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import warnings
from matplotlib import style
from collections import Counter
style.use('fivethirtyeight')

dataset = { 'k': [[1,2],[2,3],[3,1]], 'r': [[6,5],[7,7],[8,6]]}

new_feastrues = [5,7]

for i in dataset:
    for ii in dataset[i]:
        plt.scatter(ii[0], ii[1], s=100, color=i)

        plt.scatter(new_feastrues[0], new_feastrues[1])
plt.show()

def k_nearest_neighbors(data, predict, k=3):
    if len(data) >= k:
        warnings.warn('k is set to a value less than total voting groups!')

    knnalgos
    return vote_result