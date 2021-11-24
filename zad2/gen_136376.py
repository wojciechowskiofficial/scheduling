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
    # sample bs from uniform continuous(2, 5) distribution
    b_transposed = np.random.uniform(2, 5, 4)
    b_transposed[np.random.randint(0, 4)] = 1.
    # sample ps from uniform(a, b) distribution
    p_a = 100
    p_b = 1000
    p_transposed = np.random.randint(p_a, p_b, n)
    # sample rs from uniform continuous(0, sum(p_transposed) * 0.5)
    r_transposed = np.random.randint(0, np.sum(p_transposed) * .25, n)
    # sample ds from uniform(p + r, (p + r) + p_b - p_a)
    r_plus_p_transposed = r_transposed + p_transposed
    d_transposed = r_plus_p_transposed
    for i in range(d_transposed.shape[0]):
        d_transposed[i] = np.random.randint(d_transposed[i] + 1, d_transposed[i] + .25 * p_b)
    # sample ws from uniform(1, 5)
    w_transposed = np.random.randint(1, 5, n)
    prdw_matrix = np.array([p_transposed, r_transposed, d_transposed, w_transposed], dtype=np.int64)
    prdw_matrix = np.transpose(prdw_matrix)
    s_matrix = np.random.randint(np.min(p_transposed), np.round(np.max(p_transposed) / 2), size=(n, n))
    prdw_matrix[0][1] = 0
    with open('in_136376_' + str(n) + '.txt', 'w') as f:
        f.write(str(n))
        f.write('\n')
        for i in range(4):
            f.write(str(b_transposed[i]) + ' ')
        f.write('\n')
        for i in range(n):
            for j in range(4):
                f.write(str(prdw_matrix[i][j]) + ' ')
            f.write('\n')
        for i in range(n):
            for j in range(n):
                f.write(str(s_matrix[i][j]) + ' ')
            f.write('\n')



if __name__ == '__main__':
    Main()
