import numpy as np
import sys


class Task:
    def __init__(self, i, p, r, d, w):
        self.i = i
        self.p = p
        self.r = r
        self.d = d
        self.w = w


class Machine:
    def __init__(self, i, b, tasks=None):
        self.i = i
        self.b = b
        self.time = 0
        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

    def get_crit_val(self):
        crit_val = 0
        time = 0
        for task in self.tasks:
            time = max(time, task.r) + (task.p / self.b)
            if time > task.d:
                crit_val += task.w
        return crit_val

    def get_start_duration(self):
        time = 0
        result = []
        for task in self.tasks:
            result.append((max(time, task.r), task.p / self.b))
            time = max(time, task.r) + (task.p / self.b)
        return result


def get_tasks_and_machines(in_fname):
    f = open(in_fname)
    n = int(f.readline())
    machines = [Machine(i, float(b)) for i, b in enumerate(f.readline().split())]
    tasks = []
    for i in range(n):
        p, r, d, w = [int(val) for val in f.readline().split()]
        tasks.append(Task(i, p, r, d, w))

    f.close()
    return machines, tasks


def alg1(machines, tasks):
    machines.sort(key=lambda machine: machine.b, reverse=True)
    while len(tasks) >= 1:
        tasks.sort(key=lambda task: task.d)
        task_found = False
        for task in tasks:
            for machine in machines:  # always 4 so O(1)
                if max(machine.time, task.r) + task.p / machine.b < task.d:
                    machine.tasks.append(task)
                    machine.time = max(machine.time, task.r) + task.p / machine.b
                    tasks.remove(task)
                    task_found = True
                    break
            if task_found:
                break
        if not task_found:
            machines[0].tasks.append(tasks[0])
            tasks.remove(tasks[0])

    return machines

def alg2(machines, tasks):
    while len(tasks) >= 1:
        tasks.sort(key=lambda task: task.d)
        machines.sort(key=lambda machine: machine.time)
        #print([(machine.time, machine.b) for machine in machines])
        task_found = False
        min_r = min([task.r for task in tasks])
        for task in tasks:
            for machine in machines:  # always 4 so O(1)
                if max(machine.time, task.r) + task.p / machine.b <= task.d and task.r <= max(machine.time, min_r) + 5*task.w:
                    machine.tasks.append(task)
                    machine.time = max(machine.time, task.r) + task.p / machine.b
                    #print(task.r, task.p, task.d)
                    tasks.remove(task)
                    task_found = True
                    break
            if task_found:
                break
        if not task_found:
            machines[0].tasks.append(tasks[0])
            tasks.remove(tasks[0])

    return machines

def alg3(machines, tasks):
    n = len(tasks)
    while len(tasks) >= 1:
        tasks.sort(key=lambda task: task.d)
        best_10 = tasks[:len(tasks)//10]
        best_10.sort(key=lambda task: task.w, reverse=True)
        tasks[:len(tasks)//10] = best_10


        machines.sort(key=lambda machine: machine.time)
        task_found = False
        min_r = min([task.r for task in tasks])
        for task in tasks:
            for machine in machines:  # always 4 so O(1)
                if max(machine.time, task.r) + task.p / machine.b <= task.d and task.r <= max(machine.time, min_r) + task.w:
                    machine.tasks.append(task)
                    machine.time = max(machine.time, task.r) + task.p / machine.b
                    tasks.remove(task)
                    task_found = True
                    break
            if task_found:
                break
        if not task_found:
            machines[0].tasks.append(tasks[0])
            machines[0].time = max(machines[0].time, tasks[0].r) + tasks[0].p / machines[0].b
            tasks.remove(tasks[0])

    return machines


def run(in_fname, out_fname):
    out_f = open(out_fname, 'w')

    machines, tasks = get_tasks_and_machines(in_fname)

    machines = alg3(machines, tasks)
    machines.sort(key=lambda machine: machine.i)

    crit_val = 0
    for machine in machines:
        crit_val += machine.get_crit_val()

    out_f.write(f'{crit_val}\n')
    for machine in machines:
        out_f.write(f'{" ".join([str(c.i) for c in machine.tasks])}\n')

    out_f.close()


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
