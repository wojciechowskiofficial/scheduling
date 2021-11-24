#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

## deps

import math
import random

class Instance:
    def create(self, size):
        instance = Instance(size)
        instance._randomize()
        return instance

    def __init__(self, n=None):
        self.n = n
        if n is not None:
            self._set_n(n)
        

    def save(self, path):
        f = open(path, 'w')
        f.write(str(self.n) + '\n')
        f.write('\n'.join(map(lambda j: str(self.p[j]) + ' ' + str(self.r[j]) + ' ' + str(self.d[j]), self._task_range)) + '\n')
        f.write('\n'.join(map(lambda s_i: ' '.join(map(lambda s_i_j: str(s_i_j), s_i)), self.s)) + '\n')
        f.close()

    def load(self, path):
        f = open(path, 'r')
        self._set_n(int(f.readline().strip()))
        prds = [f.readline().strip().split(' ') for _ in self._task_range]
        for i, prd in enumerate(prds):
            self.p[i] = int(prd[0])
            self.r[i] = int(prd[1])
            self.d[i] = int(prd[2])
        self.s = [[s_i_j for s_i_j in map(lambda s_i_j: int(s_i_j), f.readline().strip().split(' '))] for _ in self._task_range]
        return self

    def _randomize(self, total_processing_time=None, total_base_ready_time=None, min_window=None, max_window=None, min_ready_time_sub_rate=1.0, max_ready_time_sub_rate=None, min_s=None, max_s=None):
        if total_processing_time is None:
            total_processing_time = random.randint(self.n ** 2, self.n ** 3)
        if total_base_ready_time is None:
            total_base_ready_time = total_processing_time
        if max_ready_time_sub_rate is None:
            max_ready_time_sub_rate = random.randint(min_ready_time_sub_rate, int(math.sqrt(self.n)))
        if min_window is None:
            min_window = random.randint(0, int(math.sqrt(total_processing_time)))
        if max_window is None:
            max_window = random.randint(min_window, total_processing_time)
        if min_s is None:
            min_s = random.randint(0, int(math.sqrt(min_window)))
        if max_s is None:
            max_s = random.randint(min_s, min_window)
        self.p = self._random_p(total_processing_time)
        ready_time_sub_rate_min_to_max = max_ready_time_sub_rate - min_ready_time_sub_rate
        self.r = [max(0, int(random.randint(0, total_base_ready_time) - self.p[i] * min_ready_time_sub_rate + random.random() * ready_time_sub_rate_min_to_max)) for i in self._task_range]
        self.d = [self.r[i] + self.p[i] + random.randint(min_window, max_window) for i in self._task_range]
        self.s = [[random.randint(min_s, max_s) for _ in self._task_range] for _ in self._task_range]
        for i in self._task_range:
            self.s[i][i] = 0
        

    def _random_p(self, total_processing_time):
        total_processing_time_cuts = [0]
        for _ in range(self.n - 1):
            total_processing_time_cuts.append(random.randint(0, total_processing_time))
        total_processing_time_cuts.sort()
        total_processing_time_cuts.append(total_processing_time)
        p = [total_processing_time_cuts[i + 1] - total_processing_time_cuts[i] for i in self._task_range]
        try:
            p.index(0) # should not have any 0 time tasks
        except ValueError:
            return p
        return self._random_p(total_processing_time)

    def _set_n(self, n):
        self.n = n
        self._task_range = range(n)
        self.p = [0 for _ in self._task_range]
        self.r = [0 for _ in self._task_range]
        self.d = [0 for _ in self._task_range]
        self.s = [[0 for _ in self._task_range] for _ in self._task_range]



Instance.create = classmethod(Instance.create)

#from generator.instance import Instance

class Solver:
    def solve(self, input_filename, output_filename=None):
        instance = Instance().load(input_filename)
        task_order = self.task_order(instance)
        l_max = self.l_max(instance, task_order)
        if output_filename is None:
            student_id_index = input_filename.find("in_") + 3
            student_id = input_filename[student_id_index:(student_id_index + 6)]
            output_filename = 'out_' + student_id + '_146889_' + str(instance.n) + '.txt'
        self._save(output_filename, task_order, l_max)
        return l_max

    def _save(self, output_filename, task_order, l_max):
        f = open(output_filename, 'w')
        f.write(str(l_max) + '\n')
        f.write(' '.join(map(lambda j: str(task_order[j]), range(len(task_order)))) + '\n')
        f.close()

    def task_order(self, instance):
        raise NotImplementedError('Not yet implemented!')

    def l_max(self, instance, task_order):
        raise NotImplementedError('Not yet implemented!')
		
#from solver.Solver import Solver

class ProperSolver(Solver):
    def l_max(self, instance, task_order):
        l_max = None
        worst_task = None
        time = 0
        current_task = None
        for i in task_order:
            time = self.end_time(instance,  time, current_task, i)
            l = time - instance.d[i]
            if (l_max is None) or (l > l_max):
                l_max = l
                worst_task = i
            current_task = i
        return l_max#, worst_task

    def end_time(self, instance, time, current_task, next_task):
        wait_time = max(0, instance.r[next_task] - time)
        active_switch_time = 0
        if current_task is not None:
            active_switch_time = max(0, instance.s[current_task][next_task] - wait_time)
        return time + wait_time + active_switch_time + instance.p[next_task]

    def lower_bound(self, instance):
        return min([instance.r[i] + instance.p[i] - instance.d[i] for i in range(instance.n)])

class InsertionSolver(ProperSolver):
    # I'm insertion. I insert tasks in my own way.
    def task_order(self, instance):
        task_preinsertion_order = [i for i in range(instance.n)]
        task_preinsertion_order.sort(key=lambda i: instance.d[i] + instance.r[i] - instance.p[i])
        task_start_times = [None for i in range(instance.n)]
        task_order = []
        self._l_max = None
        for i in range(instance.n):
            task = task_preinsertion_order[i]
            base_start_time = instance.r[task]
            for k, j in enumerate(task_order):
                j_end_time_before_task = task_start_times[j] + instance.p[j] + instance.s[j][task]
                task_end_time_before_j = base_start_time + instance.p[task] + instance.s[task][j]
                task_end_time_before_next = 0
                next_start_time = 0
                if len(task_order) > (k + 1):
                    task_end_time_before_next = base_start_time + instance.p[task] + instance.s[task][task_order[k + 1]]
                    next_start_time = task_start_times[task_order[k + 1]]
                j_overlaps_task = ((task_start_times[j] >= base_start_time) and (task_end_time_before_j > task_start_times[j]))
                if j_overlaps_task or ((task_start_times[j] <= base_start_time) and (j_end_time_before_task > base_start_time)):
                    l_j_from_moving_task_forward = task_start_times[j] + instance.p[j] - instance.d[j]
                    l_task_from_moving_task_forward = j_end_time_before_task + instance.p[task] - instance.d[task]
                    l_max_from_moving_task_forward = max(l_task_from_moving_task_forward, l_j_from_moving_task_forward)
                    if (next_start_time < task_end_time_before_next):
                            base_start_time = j_end_time_before_task
                            if (self._l_max is None) or (l_max_from_moving_task_forward > self._l_max):
                                self._l_max = l_max_from_moving_task_forward
                            continue
                    l_j_from_moving_j_forward = task_end_time_before_j + instance.p[j] - instance.d[j]
                    l_task_from_moving_j_forward = base_start_time + instance.p[task] - instance.d[task]
                    l_max_from_moving_j_forward = max(l_task_from_moving_j_forward, l_j_from_moving_j_forward)
                    if l_max_from_moving_j_forward < l_max_from_moving_task_forward:
                        task_start_times[task] = base_start_time
                        task = j
                        base_start_time = task_end_time_before_j
                        if (self._l_max is None) or (l_max_from_moving_j_forward > self._l_max):
                            self._l_max = l_max_from_moving_j_forward
                    else:
                        base_start_time = j_end_time_before_task
                        if (self._l_max is None) or (l_max_from_moving_task_forward > self._l_max):
                            self._l_max = l_max_from_moving_task_forward
                        
            task_start_times[task] = base_start_time
            l = base_start_time + instance.p[task] - instance.d[task]
            if (self._l_max is None) or (l > self._l_max):
                self._l_max = l
            task_order.append(task_preinsertion_order[i])
            task_order.sort(key=lambda i: task_start_times[i])
        return task_order

## end deps

# from solver.InsertionSolver import InsertionSolver

solver = InsertionSolver()
if len(sys.argv) > 2:
    instance_path = sys.argv[1]
    output_filename = sys.argv[2]
    solver.solve(instance_path, output_filename=output_filename)
elif len(sys.argv) > 1:
    instance_path = sys.argv[1]
    solver.solve(instance_path)
