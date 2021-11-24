from itertools import permutations
import sys
from random import randint

K = 4
assert(K % 2 == 0)


# main functions 
def make_matrix(matrix):
    result = []
    for line in matrix:
        result.append([int(e) for e in line.split()])
    return result
    


def get_input(filename = 'input.txt'): # O(n^2)
    with open(filename, 'r') as file_obj:
        text = file_obj.read()
        lines = text.split('\n')
        n = int(lines[0])
        segments = make_matrix(lines[1:n+1])
        s_matrix = make_matrix(lines[n+1:])
    
        return {
            'n': n,
            'segments': segments,
            's_matrix': s_matrix
        }


def sort_by_r(segments): # O(nlogn)
    segments = [(e[1], (*e, i)) for i, e in enumerate(segments)]
    segments = sorted(segments)
    segments = [e for help_attr, e in segments]
    return segments


def get_grade(segments, s_matrix):
    if segments == []: return 0
    max_l, curpos = 0, segments[0][1]
    for i, (duration, beg, en, index) in enumerate(segments):
        curpos = max(curpos, beg)
        curpos += duration
        max_l = max(max_l, curpos - en)

        if i == len(segments) - 1: continue
        n_duration, n_beg, n_en, n_index = segments[i + 1]
        curpos += s_matrix[index][n_index]

    return max_l


def merge(prefix, sufix, s_matrix):
    main_prefix, part_prefix = prefix[:-K//2], prefix[-K//2:]
    part_sufix, main_sufix = sufix[:K//2], sufix[K//2:]

    # main_prefix + best_perm(part_prefix + part_sufix) + main_sufix
    to_perm = part_prefix + part_sufix
    result = (10**10, None)
    for perm in permutations(to_perm):
        candidate = main_prefix + perm + main_sufix
        result = min(
            result,
            (get_grade(candidate, s_matrix), candidate)
        )
    return result[1]


def divide_and_conquer(segments, s_matrix):
    if len(segments) <= K:
        result = (10**10, None)
        for perm in permutations(segments):
            result = min(
                result,
                (get_grade(perm, s_matrix), perm)
            )
        return result[1]
    
    mid = len(segments) // 2
    prefix = segments[:mid]
    sufix = segments[mid:]

    prefix = divide_and_conquer(prefix, s_matrix)
    sufix = divide_and_conquer(sufix, s_matrix)
    return merge(prefix, sufix, s_matrix)


def save_result(segments, filename, s_matrix):
    with open(filename, 'w') as file_obj:
        file_obj.write('{}\n{}'.format(
            get_grade(segments, s_matrix),
            ' '.join([str(index) for _, _, _, index in segments])
        ))


def solve(data, output):
    n = data['n']
    segments = sort_by_r(data['segments']) # (trwanie, poczatek, koniec, indeks)
    s_matrix = data['s_matrix']

    segments = divide_and_conquer(segments, s_matrix)
    return (get_grade(segments, s_matrix), segments)
    
    

if __name__ == '__main__':
    input = sys.argv[1]
    output = sys.argv[2]

    data = get_input(input)
    best = solve(data, output)
    
    save_result(best[1], output, data['s_matrix'])
    # O(n^2 + nlogn * K!)