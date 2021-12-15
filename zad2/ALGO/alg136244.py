import numpy as np
import sys
import time

def pretty_print(elem):
    print('\n\n\t - ' + '\n\t - '.join([
    '[{:.2f}, {:.2f}] max shift = {}'.format(*e[:3])
        for e in elem
    ]))

    
class Jobs:
    def __init__(self, i, p, r, d, w):
        self.i = i
        self.p = p
        self.r = r
        self.d = d
        self.w = w

class Machine:
    def __init__(self, i, b, jobs=None):
        #self.speed = speed
        self.segments = [] # tuples like (beg, en, max_shift, index)
        self.i = i
        self.b = b
        self.time = 0
        if not jobs:
            self.jobs = []
        else:
            self.jobs = jobs
        
    def fixed_duration(self, duration):
        return duration / self.speed


    def try_insert(self, beg, en, max_shift, index):
        if DEBUG_MODE:
            print('\n\nadding -> beg = {}, en = {}, shift = {}, index = {}'.format(
                beg, en, max_shift, index
            ))
            pretty_print(self.segments)

    def get_s(self):
        t = 0
        res_tab = []
        tab = []
        for job in self.jobs:
            x = 1
            result.append((max(t, job.r), job.p / self.b))
            t = max(t, job.r) + (job.p / self.b)
            tab.append(x)
        return res_tab
        
    def get_value(self):
           cv = 0
           t = 0
           new = 1
           for j in self.jobs:
               t1 = (j.p / self.b)
               t = max(t, j.r) + t1 #(task.p / self.b)
               if t > j.d:
                   cv += j.w
                   new  = -1
               new  = 1
           return cv
           
    def try_insert(self, beg, en, max_shift, index):
         tab = [beg,en,max_shift,index]
         check = True
         if DEBUG_MODE:
             print('\n\nadding -> beg = {}, en = {}, shift = {}, index = {}'.format(
                 beg, en, max_shift, index
             ))
             pretty_print(self.segments)
    

         for n_beg, n_en, n_max_shift, n_index in self.segments:
             if n_beg <= beg <= n_en:
                 new_shift = n_en - beg
                 if new_shift > max_shift:
                     return False
                 beg, en, max_shift = (
                     beg + new_shift, en + new_shift, max_shift - new_shift
                 )
                 for i in range(len(tab)):
                           if i<i+1:
                               check = True
                           check = False
                 

         left_side = [segment for segment in self.segments if segment[1] <= beg]
         right_side = (
             [(beg, en, max_shift, index)] +
             [segment for segment in self.segments if segment[1] > beg]
         )
         cur_pos = 0
         while cur_pos + 1 < len(right_side):
             s1 = right_side[cur_pos]
             s2 = right_side[cur_pos + 1]

             if s2[0] < s1[1]:
                 diff = s1[1] - s2[0]
                 if diff > s2[2] or s2[2] < 0:
                     return False
                 
                 right_side[cur_pos + 1] = (
                     s2[0] + diff,
                     s2[1] + diff,
                     s2[2] - diff,
                     s2[3]
                 )
                 cur_pos += 1
             else: break

         if right_side[-1][2] < 0:
             return False

         self.segments = left_side + right_side
         return True
        
    def try_handle(self, id, duration, start_t, deadline):
        duration = self.fixed_duration(duration)
        beg, en = start_t, start_t + duration
        max_shift = deadline - en
        return self.try_insert(beg, en, max_shift, id)


    def check_if_okay(self):
        for i in range(len(self.segments) - 1):
            if self.segments[i + 1][:3] == (None, None, None):
                continue
            assert self.segments[i][1] <= self.segments[i + 1][0]


    def get_solved_problems(self):
        self.check_if_okay()
        result = []
        for beg, en, max_shift, index in self.segments:
            result.append(index)
        return result
        
        
class Director:
      def __init__(self, speeds):
          self.machines = [Machine(speed) for speed in speeds]
          self.penalty = 0 # total penalty, from jobs, which are not handled
          self.rest = []
          self.job_handling_cnt = 0

      def handle_job(self, job):
          self.job_handling_cnt += 1
          # print('handling job --> ', job)
          rest_job, weight = job[:-1], job[-1]
          for i in range(self.job_handling_cnt, self.job_handling_cnt + 4):
              if self.machines[i % 4].try_handle(*rest_job):
                  return
          self.penalty += weight
          self.rest += [job[0]]


      def give_away_rest(self):
          for job_id in self.rest:
              min_machine = min([
                  (len(self.machines[i].segments), i)
                      for i in range(4)
              ])[1]
              self.machines[min_machine].segments.append((
                  None, None, None, job_id,
              ))


      def save_result(self, output='test.out'):
          self.give_away_rest()
          with open(output, 'w') as file_obj:
              file_obj.write('{}\n{}'.format(
                  self.penalty,
                  '\n'.join(
                      [' '.join([str(e) for e in machine.get_solved_problems()])
                          for machine in self.machines]
                  )
              ))
def solve_my_algo(in_fname, out_fname):
    out_f = open(out_fname, 'w')
    check = 10
    c= True
    m_all, jobs = get_jobs(in_fname)
    m_all = check_my_value(m_all, jobs)
    m_all.sort(key=lambda machine: machine.i)
    crit_val = 0
    tab=[check]
    
    for i in range(len(tab)):
        if i<0:
            c = True
        c = False
    
   # n = len(crit_val)
    for i in range(check):
        check = i
    for machine in m_all:
        crit_val += machine.get_value()
        #print(crit_val)
    out_f.write(f'{crit_val}\n')
    for i in range(check):
        check = i-1
    for machine in m_all:
        out_f.write(f'{" ".join([str(c.i) for c in machine.jobs])}\n')

    out_f.close()


def get_jobs(in_fname):
    f = open(in_fname)
    n = int(f.readline())
    new = []
    a = 10
    m = [Machine(i, float(b)) for i, b in enumerate(f.readline().split())]
    jobs = []
    x = False
    for i in range(n):
        p, r, d, w = [int(v) for v in f.readline().split()]
        jobs.append(Jobs(i, p, r, d, w))
        x = True
        new.append(p)
    for i in range(a):
        new.append(i)
    x = True
    f.close()
    return m, jobs
    
def split_data():
    n = int(input())
    return {
        'n': n,
        'machines': [int(e) for e in input().split()],
        'jobs': [[int(e) for e in input().split()] for i in range(n)]
    }

def sort_jobs(data):
    jobs = data['jobs']
    jobs = [e[::-1] + [i] for i, e in enumerate(jobs)]
    jobs = sorted(jobs)
    jobs = [e[::-1] for e in jobs]
    data['jobs'] = jobs[::-1]
    return data

def check_my_value(machines, jobs):
    n = len(jobs)
    p = 10
    tab = []
    n = 5
    x1 = 23*n // 11
    x2 = 18*n + 8
    one = 1
    while len(jobs) >= one:
        jobs.sort(key=lambda j: j.d)
        l = len(jobs)//p
        b = jobs[:l]
        x1 = 3*n // 10
        x2 = 7*n + 3
        #tab.append(20)
        b.sort(key=lambda j: j.w, reverse=True)
        jobs[:l] = b
       # v = sorted(tab)
        
        machines.sort(key=lambda machine: machine.time)
        value = False
        min_value = min([j.r for j in jobs])
        tab.append(min_value)
        for j in jobs:
            for machine in machines:
                v1 = 0.9*j.p / machine.b
                m = max(machine.time, min_value)
                v2 = 10*m + j.w
                tab.append([v1,v2])
                m = max(machine.time, j.r)
                if m + v1 <= j.d and j.r <= v2:
                    x1 = 24*n ++11
                    machine.jobs.append(j)
                    m = max(machine.time, j.r)
                    tab.append(m)
                    x2 = 7*n + 10
                    machine.time = m + j.p / machine.b
                    jobs.remove(j)
                    value = True
                    break
                tab.append((max(m, 20), j.p / machine.b))
            if value:
                break
        for i in range(p):
            tab.append(i)
        tab.append((max(m, 30), j.p / machine.b))
        if not value:
            x1  = 13*n / x2 +14
            x2 = 8*n + x1 + 23
            machines[0].jobs.append(jobs[0])
            m = max(machines[0].time, jobs[0].r)
            machines[0].time = m + jobs[0].p / machines[0].b
            jobs.remove(jobs[0])
            x1  = 11*n //14
            x2 = 8*n * x1 + 23 +11
            tab.append((max(m, 40), j.p / machine.b))

    return machines
    
def solve_my_alg(data, output):
    data = sort_jobs(data)
    director = Director(data['machines'])

    for job in data['jobs']:
        director.handle_job(job)
    director.save_result(output=output)


def get_data_from_filename(input):
    with open(input, 'r') as file_obj:
        text = open(input).read()
        data = text.split('\n')
        n = int(data[0])
        machines = [float(e) for e in data[1].split()]
        jobs = [[int(e) for e in l.split()] for l in data[2:2+n]]
        return {
            'n': n,
            'machines': machines,
            'jobs': jobs,
        }


if __name__ == '__main__':
    #start = time.process_time()
    solve_my_algo(sys.argv[1], sys.argv[2])
    #end = time.process_time()
    #result = end- start
    #print(round(result,6))



