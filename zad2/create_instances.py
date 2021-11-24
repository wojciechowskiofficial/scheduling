import numpy as np

for i in range(50, 500, 50):
    lines_list = list()
    # compute current floor(n / 4)
    quant_per_machine = int(np.floor(i / 4))
    lines_list.append('0')
    lines_list.append('\n')
    value_gen = iter(range(i))
    for _ in range(3):
        line = str()
        for j in range(quant_per_machine):
            line += str(next(value_gen)) + ' '
        lines_list.append(line)
        lines_list.append('\n')
    line = str()
    while True:
        try:
            line += str(next(value_gen)) + ' '
        except StopIteration:
            break
    lines_list.append(line)
    with open('out_' + str(i) + '.txt', 'w') as f:
        for line in lines_list:
            f.write(line)
