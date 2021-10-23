import argparse
import numpy as np

class Task:
    pass

def Main():
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_name', type=str)
    parser.add_argument('--out_name', type=str)
    args = parser.parse_args()
    # load
    with open(args.in_name, 'r') as f:
        one_string_in = f.read().split()
    gen_one_string_in = iter(one_string_in)
    n = int(next(gen_one_string_in))
    prd_matrix = np.empty((n, 3), np.int64)
    for i in range(n):
        for j in range(3): 
            prd_matrix[i][j] = next(gen_one_string_in)
    s_matrix = np.empty((n, n), np.int64)
    for i in range(n):
        for j in range(n):
            s_matrix[i][j] = next(gen_one_string_in)
    # start scheduling
    # init stuff
    curr_t = np.zeros(n)
    scheduling = list()
    p_transposed = prd_matrix[:, 0].transpose()
    r_transposed = prd_matrix[:, 1].transpose()
    d_transposed = prd_matrix[:, 2].transpose()
    ids = np.arange(n)
    # pick the first task
    lateness = r_transposed + p_transposed - d_transposed
    next_task = np.argmin(r_transposed)
    l_max = lateness[next_task]
    scheduling.append(ids[next_task])
    curr_t = np.full(shape=r_transposed.shape, fill_value=(r_transposed[next_task] + p_transposed[next_task]))
    # curr_t -> befor any s_matrix addition
    for i in range(1, n, 1):
        # next_task is still from previous iteration
        # curr_t is after processing the previous task and before adding s times
        # add s_matrix to curr_t
        curr_t += s_matrix[next_task][:]
        # delete previous task
        p_transposed = np.delete(p_transposed, next_task)
        r_transposed = np.delete(r_transposed, next_task)
        d_transposed = np.delete(d_transposed, next_task)
        ids = np.delete(ids, next_task)
        s_matrix = np.delete(s_matrix, next_task, 0)
        s_matrix = np.delete(s_matrix, next_task, 1)
        lateness = np.delete(lateness, next_task)
        curr_t = np.delete(curr_t, next_task)
        # merge curr_t with r times onto tmp_r_transposed
        tmp_r_transposed = np.where(r_transposed < curr_t, curr_t, r_transposed)
        # calculate lateness vector
        lateness = tmp_r_transposed + p_transposed - d_transposed
        # choose new next task
        next_task = np.argmax(lateness)
        # update l_max if needed
        if l_max < lateness[next_task]:
            l_max = lateness[next_task]
        # add new next task to scheduling list
        scheduling.append(ids[next_task])
        # populate chosen curr_t onto the whole vector
        curr_t = np.full(shape=curr_t.shape, 
                         fill_value=tmp_r_transposed[next_task] + p_transposed[next_task])
    # write to file
    with open(args.out_name, 'w') as f:
        f.write(str(l_max))
        f.write('\n')
        for task in scheduling:
            f.write(str(task) + ' ')


if __name__ == '__main__':
    Main()
