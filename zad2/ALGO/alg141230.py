import sys

MAX_INT = 2**100
student_id = 141230


if len(sys.argv) >= 3 and sys.argv[1][-4:] == ".txt" and sys.argv[2][-4:] == ".txt":
    # tie_count = 0
    # Load instance
    input_file = open(sys.argv[1], "r")
    n = int(input_file.readline())

    b = []
    b_line = input_file.readline().split()
    if len(b_line) != 4:
        sys.exit(f"ERROR: Wrong format at line 2 in file {sys.argv[1]}")
    for b_str in b_line:
        b.append(float(b_str))

    p = []
    r = []
    d = []
    w = []
    for j in range(0, n):
        line = input_file.readline().split()
        if len(line) != 4:
            sys.exit(f"ERROR: Wrong format at line {j + 3} in file {sys.argv[1]}")
        p.append(int(line[0]))
        r.append(int(line[1]))
        d.append(int(line[2]))
        w.append(int(line[3]))

    input_file.close()

    # Schedule jobs
    # rule: min c*(1/b + w*u)

    c = [-1] * n  # completion times
    schedule = [[], [], [], []]
    sum_wu = 0
    instant = [0, 0, 0, 0]

    while sum([len(s) for s in schedule]) < n:
        schedule_goal = MAX_INT
        schedule_candidate = MAX_INT
        c_candidate = MAX_INT
        wu_candidate = MAX_INT
        machine_candidate = MAX_INT

        for target_machine in range(4):
            for j in range(n):
                if c[j] == -1:  # job wasn't already scheduled
                    tmp_c = max(instant[target_machine], r[j]) + p[j] / b[target_machine]
                    tmp_u = int(tmp_c > d[j])
                    tmp_wu = tmp_u * w[j]

                    goal = tmp_c * (1.0 / b[target_machine] + tmp_wu)
                    if goal < schedule_goal \
                            or (goal == schedule_goal and (w[j] > w[schedule_candidate]
                                                           or (w[j] == w[schedule_candidate] and tmp_c < c_candidate))):
                        schedule_goal = goal
                        schedule_candidate = j
                        c_candidate = tmp_c
                        wu_candidate = tmp_wu
                        machine_candidate = target_machine

        if schedule_candidate != MAX_INT:
            # job chosen - proceed
            c[schedule_candidate] = c_candidate
            instant[machine_candidate] = c_candidate
            sum_wu += wu_candidate
            schedule[machine_candidate].append(schedule_candidate)
        else:
            print("ERROR - no candidate found!")
            break

    # Save output to file
    output_file = open(sys.argv[2], "w")
    output_file.write(f"{sum_wu}\n")
    for m in range(4):
        output_file.write(" ".join(map(str, schedule[m])))
        if m < 3:
            output_file.write("\n")
    output_file.close()

else:
    sys.exit("Please run the algorithm with correctly named input & output files:\n"
             + f"python {sys.argv[0]} [in_123456_n.txt] [out_123456_{student_id}_n.txt")
