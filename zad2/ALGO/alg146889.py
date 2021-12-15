#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import random

class Instance:
    def create(self, size):
        instance = self(size)
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
        

    def _random_p(self, total_processing_time, cut_count=None, cuts=[]):
        if cut_count is None:
            cut_count = self.n - 1
        total_processing_time_cuts = [0] + cuts
        for _ in range(cut_count):
            total_processing_time_cuts.append(random.randint(0, total_processing_time))
        total_processing_time_cuts.sort()
        total_processing_time_cuts.append(total_processing_time)
        p = [total_processing_time_cuts[i + 1] - total_processing_time_cuts[i] for i in self._task_range]
        try:
            p.index(0) # should not have any 0 time tasks
        except ValueError:
            return p, total_processing_time_cuts
        return self._random_p(total_processing_time)

    def _set_n(self, n):
        self.n = n
        self._task_range = range(n)
        self.p = [0 for _ in self._task_range]
        self.r = [0 for _ in self._task_range]
        self.d = [0 for _ in self._task_range]
        self.s = [[0 for _ in self._task_range] for _ in self._task_range]



Instance.create = classmethod(Instance.create)

class Q4rwuInstance(Instance):
    def _set_n(self, n):
        self.n = n
        self._task_range = range(n)
        self.b = [1.0 for _ in range(4)]
        self.p = [0 for _ in self._task_range]
        self.r = [0 for _ in self._task_range]
        self.d = [0 for _ in self._task_range]
        self.w = [0 for _ in self._task_range]

    def save(self, path):
        f = open(path, 'w')
        f.write(str(self.n) + '\n')
        f.write(' '.join(map(lambda b: str(b), self.b)) + '\n')
        f.write('\n'.join(map(lambda j: str(self.p[j]) + ' ' + str(self.r[j]) + ' ' + str(self.d[j]) + ' ' + str(self.w[j]), self._task_range)) + '\n')
        f.close()

    def load(self, path):
        f = open(path, 'r')
        self._set_n(int(f.readline().strip()))
        self.b = [b for b in map(lambda b: float(b), f.readline().strip().split(' '))]
        prdws = [f.readline().strip().split(' ') for _ in self._task_range]
        for i, prdw in enumerate(prdws):
            self.p[i] = int(prdw[0])
            self.r[i] = int(prdw[1])
            self.d[i] = int(prdw[2])
            self.w[i] = int(prdw[3])
        return self

    def _randomize(self, total_processing_time=None, min_window=0, max_window=0, min_ready_time_sub_rate=1.0, max_ready_time_sub_rate=1.0, weight_multiplier=random.randint(2, 10)):
        self.b = [1] + [1 + abs(random.normalvariate(0, 1)) for _ in range(3)]
        total_b =  sum(self.b)
        if total_processing_time is None:
            total_processing_time = random.randint(self.n ** 2, self.n ** 3)
        if max_ready_time_sub_rate is None:
            max_ready_time_sub_rate = min_ready_time_sub_rate + random.random() * ((int(math.sqrt(self.n) / total_b)) - min_ready_time_sub_rate)
        if max_window is None:
            max_window = random.randint(0, int(total_processing_time / self.n))
        if min_window is None:
            min_window = random.randint(0, max_window)
        machine_cuts = []
        cut_total = 0
        for i in range(3):
            cut_total += int(round(total_processing_time * self.b[i] / total_b))
            machine_cuts.append(cut_total)
        print(machine_cuts, total_processing_time)
        self.p, cuts = self._random_p(total_processing_time, cut_count=self.n - 4, cuts=machine_cuts)
        machine_cut_index = 0
        task_delay_change = 0
        machine_ids = []
        print([cuts.index(machine_cuts[i]) for i in range(3)])
        for i, cut in enumerate(cuts[1:]):
            if (machine_cut_index < 3) and (cut > machine_cuts[machine_cut_index]):
                task_delay_change = machine_cuts[machine_cut_index]
                machine_cut_index += 1
            cuts[i] -= task_delay_change
            machine_ids.append(machine_cut_index)
        #print(cuts)
        ready_time_sub_rate_min_to_max = max_ready_time_sub_rate - min_ready_time_sub_rate
        self.r = [max(0, round(cuts[i] / self.b[machine_ids[i]] - random.random() * ready_time_sub_rate_min_to_max)) for i, p in enumerate(self.p)]
        self.d = [self.r[i] + self.p[i] + random.randint(min_window, max_window) for i in self._task_range]
        self.w = [weight_multiplier ** math.floor(abs(random.normalvariate(0, 1))) for _ in self._task_range]
        print(machine_ids.count(0), machine_ids.count(0) + machine_ids.count(1), machine_ids.count(0) + machine_ids.count(1) + machine_ids.count(2), machine_ids.count(0) + machine_ids.count(1) + machine_ids.count(2) + machine_ids.count(3))
        shuffled_ids = [i for i in self._task_range]
        random.shuffle(shuffled_ids)
        self.p = [self.p[i] for i in shuffled_ids]
        self.r = [self.r[i] for i in shuffled_ids]
        self.d = [self.d[i] for i in shuffled_ids]
        self.w = [self.w[i] for i in shuffled_ids]
        

class SolverBase:
    def solve(self, input_filename, output_filename=None, klass=Instance):
        instance = klass().load(input_filename)
        task_order = self.task_order(instance)
        criterion_value = self.criterion_value(instance, task_order)
        if output_filename is None:
            student_id_index = input_filename.find("in_") + 3
            student_id = input_filename[student_id_index:(student_id_index + 6)]
            output_filename = 'out_' + student_id + '_146889_' + str(instance.n) + '.txt'
        self._save(output_filename, task_order, criterion_value)
        return criterion_value

    def _save(self, output_filename, task_order, criterion_value):
        f = open(output_filename, 'w')
        f.write(str(criterion_value) + '\n')
        self.write(f, task_order)
        f.close()

    def write(self, f, task_order):
        raise NotImplementedError('Not yet implemented!')

    def task_order(self, instance):
        raise NotImplementedError('Not yet implemented!')

    def criterion_value(self, instance, task_order):
        raise NotImplementedError('Not yet implemented!')

class Solver(SolverBase):
    def write(self, f, task_order):
        f.write('\n'.join(map(lambda b: ' '.join(map(lambda bj: str(task_order[b][bj]), range(len(task_order[b])))), range(len(task_order)))) + '\n')

class ProperSolver(Solver):
    def criterion_value(self, instance, task_order):
        late_weights = 0
        late_tasks = []
        for m, b in enumerate(task_order):
            time = 0
            for i in b:
                time = self.end_time(instance,  time, i, m)
                l = time - instance.d[i]
                if l > 0:
                    late_weights += instance.w[i]
                    late_tasks.append(i)
        return late_weights

    def end_time(self, instance, time, next_task, machine_id):
        wait_time = max(0, instance.r[next_task] - time)
        return time + wait_time + instance.p[next_task] / instance.b[machine_id]

class StaticInsertionDLLPTHWSM(ProperSolver):
    # I'm Static Insertion Dead Lined Least Processing Time Highest Weight Slowest Machine. I insert tasks in my own way.
    def task_order(self, instance):
        task_preinsertion_order = [i for i in range(instance.n)]
        task_preinsertion_order.sort(key=lambda i: instance.p[i] * instance.w[i] - instance.d[i] + instance.r[i], reverse=True)
        machine_insertion_order = [i for i in range(4)]
        machine_insertion_order.sort(key=lambda i: instance.b[i])
        task_start_times = [None for i in range(instance.n)]
        task_order = [[], [], [], []]
        late_tasks = []
        for i in range(instance.n):
            task = task_preinsertion_order[i]
            inserted = False
            for j, _ in enumerate(task_order):
                conflict = False
                machine_id = machine_insertion_order[j]
                speed = instance.b[machine_id]
                base_start_time = instance.d[task] - instance.p[task] / speed
                for _, l in enumerate(task_order[machine_id]):
                    l_end_time = task_start_times[l] + instance.p[l] / speed
                    task_end_time = base_start_time + instance.p[task] / speed
                    l_overlaps_task = ((task_end_time >= task_start_times[l]) and (task_start_times[l] >= base_start_time))
                    if l_overlaps_task or ((task_start_times[l] <= base_start_time) and (base_start_time <= l_end_time)):
                        base_start_time = task_start_times[l] - instance.p[task] / speed
                        if base_start_time < instance.r[task]:
                            conflict = True
                            break
                if conflict == False:
                    inserted = True
                    task_order[machine_id].append(task)
                    #print(str(task) + ' at ' + str(machine_id) + ' from ' + str(base_start_time) + ' to ' + str(base_start_time + instance.p[task] / speed))
                    task_start_times[task] = base_start_time
                    task_order[machine_id].sort(key=lambda i: -task_start_times[i])
                    #if self.criterion_value(instance, task_order) != self.expected_value(instance, late_tasks):
                    #    raise RuntimeError('Invalid is ' + str(self.expected_value(instance, late_tasks)) + ' should be ' + str(self.criterion_value(instance, task_order)))
                    break
            if inserted == False:
                late_tasks.append(task)
        for ordering in task_order:
            ordering.sort(key=lambda i: task_start_times[i])
        task_order[0] += late_tasks
        return task_order

    def expected_value(self, instance, late_tasks):
        return sum(map(lambda i: instance.w[i], late_tasks))

solver = StaticInsertionDLLPTHWSM()
if len(sys.argv) > 2:
    instance_path = sys.argv[1]
    output_filename = sys.argv[2]
    solver.solve(instance_path, output_filename=output_filename, klass=Q4rwuInstance)
elif len(sys.argv) > 1:
    instance_path = sys.argv[1]
    solver.solve(instance_path, klass=Q4rwuInstance)
