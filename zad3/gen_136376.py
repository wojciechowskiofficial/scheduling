import argparse
import numpy as np
from scipy.stats import chi2

def Main():
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int)
    args = parser.parse_args()
    # generate
    n = args.n
    data = np.full(shape=(n, 7), fill_value=0)
    for i in range(n):
        data[i,0] = np.random.randint(15, 180)
        data[i,1] = np.random.randint(30, 40)
        data[i,2] = np.random.randint(30, 300)
        data[i,3] = np.random.randint(15, 30)
    sum_p_axis = np.sum(data, axis=1)
    sum_p = np.sum(data)
    for i in range(n):
        data[i,4] = np.random.randint(sum_p_axis[i], sum_p)
        data[i,5] = np.random.randint(1, 5)
        data[i,6] = np.random.randint(1, 5)
    with open('in_136376_' + str(n) + '.txt', 'w') as f:
        f.write(str(n))
        f.write('\n')
        for i in range(n):
            for j in range(7):
                f.write(str(data[i,j]) + ' ')
            f.write('\n')

if __name__ == '__main__':
    Main()
