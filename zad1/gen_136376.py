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
    magnitude = np.random.randint(100, 1000)
    p_transposed = np.random.randint(round(magnitude / 2), round(magnitude * 3 / 2), n)
    r_transposed = np.random.chisquare(df=5, size=n)
    r_transposed = np.where(r_transposed > 16, np.random.randint(1, 16), r_transposed)
    r_transposed = np.rint(r_transposed)
    sum_of_p = np.sum(p_transposed)
    max_of_r = np.max(r_transposed)
    scaler = round(sum_of_p / max_of_r)
    r_transposed *= np.random.randint(1, scaler, n)
    r_transposed = r_transposed.astype(np.int64)
    r_plus_p_transposed = r_transposed + p_transposed
    d_transposed = r_plus_p_transposed
    for i in range(d_transposed.shape[0]):
        d_transposed[i] = np.random.randint(d_transposed[i], d_transposed[i] + magnitude)
    prd_matrix = np.array([p_transposed, r_transposed, d_transposed], dtype=np.int64)
    prd_matrix = np.transpose(prd_matrix)
    s_matrix = np.random.randint(round(np.min(p_transposed) * .1), np.min(p_transposed), size=(n, n))
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
