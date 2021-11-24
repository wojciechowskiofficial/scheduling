__author__='141271'

data = []
switches = []

lateness_weight= 0.005
delay_weight= 0.003
switch_weight= 1
potential_weight= 0.5
length_value= 10000
length_weight= 2

import sys, math

class Task_State:
        priority = 0
        def __init__(self, n, p, r, d):
            self.n = n
            self._p = p
            self._r = r
            self._d = d

        def _get_lateness(self, time):
            value = self._d - time
            return value * lateness_weight
        def _get_delay(self, time):
            delay = (self._r - time)
            if delay > 0:
                return delay_weight * -delay
            else:
                return 0
        def _get_conversion(self, switch):
            if not switch:
                return 0
            return switch_weight * switches[switch][self.n]
        def _get_prospects(self, potential_switch):
            if potential_switch is None:
                return 0
            value = 0
            li = []
            for i in potential_switch:
                value = value + switches[self.n][i.n]
                li.append(i.n)
            if self.n in li and len(data) >= 11:
                value = value + switches[self.n][data[10].n]
            return potential_weight * value
        def _get_duration(self):
            return length_value / self._p * length_weight

        def calculate_priority(self, time, switch=None, potential_switch:list =None):
            lateness = self._get_lateness(time)
            delay = self._get_delay(time)
            conversion = self._get_conversion(switch)
            prospects = self._get_prospects(potential_switch)
            duration = self._get_duration()
            self.priority = lateness + delay + conversion + prospects + duration

        def get_new_time(self, time, switch=None):
            if switch is None:
                new_time = time
            else:
                new_time = time + switches[switch][self.n]
            if new_time < self._r :
                new_time = self._r
            new_time = new_time + self._p
            lateness = new_time - self._d
            return new_time, lateness

        def __lt__(self, other):
            return self.priority < other.priority
        def __repr__(self):
            return self.__str__()
        def __str__(self):
            return f"{self.n}"

def alg_fun(
    name_in,
    vlateness_weight= -11.028,
    vdelay_weight= 441.659,
    vswitch_weight= -1165.099,
    vpotential_weight= -25.456,
    vlength_value= 1447.307,
    vlength_weight= 41.716,
    file_data = None,
    switches_data = None
):
    global lateness_weight, delay_weight, switch_weight, potential_weight, length_value, length_weight, data, switches
    
    lateness_weight= vlateness_weight
    delay_weight= vdelay_weight
    switch_weight= vswitch_weight
    potential_weight= vpotential_weight
    length_value= vlength_value
    length_weight= vlength_weight

    data = []
    switches = []
    time = 0

    def get_data(data_file):
        with open(data_file, 'r') as file:
            number = int(file.readline())
            for i in range(number):
                p, r, d = list(map(int, file.readline().rstrip().split(' ')))
                data.append(Task_State(i, p, r, d))
            for i in range(number):
                switches.append(list(map(int, file.readline().rstrip().split(' '))))
            

    def sort_data(time, switch=None, potential_switch:list =None):
        for i in data:
            i.calculate_priority(time, switch, potential_switch)
        data.sort(reverse=True)

    order = []

    if file_data is None:
        data = []
        get_data(name_in)
    else:
        data = file_data.copy()
        switches = switches_data
    sort_data(0)
    predict = data[:10]
    sort_data(0, potential_switch=predict)

    max_late = -math.inf
    switch=None
    while len(data) > 0:
        order.append(data.pop(0))
        time, late = order[-1].get_new_time(time, switch)
        switch = order[-1].n
        if len(data) >= 10:
            predict = data[:10].copy()
        else:
            predict = data.copy()
        sort_data(time, switch, predict)
        if late > max_late: 
            max_late = late
    return max_late, order

if __name__ == "__main__": 
    max_late, order = alg_fun(name_in=sys.argv[1])
    name_out = sys.argv[1].replace('in', 'out')
    split_str = name_out.replace('in', 'out').split('_')
    split_str.insert(2, '141271')
    name_out = '_'.join(split_str)
    if len(sys.argv) > 2:
        name_out = sys.argv[2]
    with open(name_out, 'w') as file:
        print(max_late, file=file)
        print(*order, file=file)
        #print(f"done for {sys.argv[1]}")
