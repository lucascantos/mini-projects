from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import warnings
from matplotlib import style
from collections import Counter
style.use('fivethirtyeight')

dataset = { 'k': [[1,2],[2,3],[3,1]], 'r': [[6,5],[7,7],[8,6]]}

new_feastrues = [5,7]


def k_nearest_neighbors(data, predict, k=3):
    if len(data) >= k:
        warnings.warn('k is set to a value less than total voting groups!')
    distances = []
    for group in data:
        for features in data[group]:
            euclidean_distance = np.linalg.norm(np.array(features) - np.array(predict))
            distances.append([euclidean_distance, group])
    votes = [i[1] for i in sorted(distances)[:k]]
    print( Counter(votes).most_common((1)))
    vote_result = Counter(votes).most_common(1)[0][0]
    return vote_result

results = k_nearest_neighbors(dataset,new_feastrues,k=3)
print(results)


for i in dataset:
    for ii in dataset[i]:
        plt.scatter(ii[0], ii[1], s=100, color=i)

        plt.scatter(new_feastrues[0], new_feastrues[1], color=results)
plt.show()