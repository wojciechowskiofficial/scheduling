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
    # sample ps from uniform(a, b) distribution
    p_a = 100
    p_b = 1000
    p_transposed = np.random.randint(p_a, p_b, n)
    # sample rs from chi-square distribution shifted by constant 
    r_b = np.sum(p_transposed) * .75
    chi2_scale = r_b / 16
    r_transposed = chi2.rvs(df=5, scale=chi2_scale, size=n)
    # upper-boudnd right tail
    r_transposed = np.where(r_transposed > 16 * chi2_scale, np.random.randint(1, 16 * chi2_scale), r_transposed)
    r_transposed = np.rint(r_transposed)
    r_transposed = r_transposed.astype(np.int64)
    # sample ds from uniform(p + r, (p + r) + p_b - p_a)
    r_plus_p_transposed = r_transposed + p_transposed
    d_transposed = r_plus_p_transposed
    for i in range(d_transposed.shape[0]):
        d_transposed[i] = np.random.randint(d_transposed[i] + p_a, d_transposed[i] + p_b)
    prd_matrix = np.array([p_transposed, r_transposed, d_transposed], dtype=np.int64)
    prd_matrix = np.transpose(prd_matrix)
    s_matrix = np.random.randint(np.min(p_transposed), np.round(np.max(p_transposed) / 2), size=(n, n))
    prd_matrix[0][1] = 0
    with open('in_136376_' + str(n) + '.txt', 'w') as f:
        f.write(str(n))
        f.write('\n')
        for i in range(n):
            for j in range(3):
                f.write(str(prd_matrix[i][j]) + ' ')
            f.write('\n')
        for i in range(n):
            for j in range(n):
                f.write(str(s_matrix[i][j]) + ' ')
            f.write('\n')



if __name__ == '__main__':
    Main()
