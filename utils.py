import numpy as np
from tqdm import tqdm


def map_label_to_index(label):
    if label == 'h':
        return 0
    elif label == 'w':
        return 1
    elif label == 'R':
        return 2
    elif label == 'E':
        return 3

def single_array_to_matrix(x):
    output = np.empty(shape=(4,4))
    for i in tqdm(range(x.shape[0])):
        for j in range(x.shape[1]-1):
            previous = map_label_to_index(x[i,j])
            after = map_label_to_index(x[i,j+1])
            output[previous, after] += 1
    output = output / output.sum(axis = 1)

    return output

def data_to_transition_matrix(x):
    output = np.empty(shape=(3,4,4))

    pm10_am8 = x[:,np.concatenate([np.arange(45,48),np.arange(0,16)])]
    am8_5pm = x[:,np.arange(16,34)]
    pm5_pm10 = x[:,np.arange(34,45)]

    output[0] = single_array_to_matrix(pm10_am8)
    output[1] = single_array_to_matrix(am8_5pm)
    output[2] = single_array_to_matrix(pm5_pm10)
    
    return output