import sys

MAX_INT = 2**100
student_id = 141230

if len(sys.argv) >= 3 and sys.argv[1][-4:] == ".txt" and sys.argv[2][-4:] == ".txt":
    # Load instance
    input_file = open(sys.argv[1], "r")
    n = int(input_file.readline())

    p = []
    r = []
    d = []
    for j in range(0, n):
        line = input_file.readline().split()
        if len(line) != 3:
            sys.exit(f"ERROR: Wrong format at line {j + 2} in file {sys.argv[1]}")
        p.append(int(line[0]))
        r.append(int(line[1]))
        d.append(int(line[2]))

    s = []
    for i in range(0, n):
        line = input_file.readline().split()
        if len(line) != n:
            sys.exit(f"ERROR: Wrong format at line {i + n + 2} in file {sys.argv[1]}")
        s.append([int(num) for num in line])

    input_file.close()

    # Schedule tasks
    # rule: choose the smallest weighted sum of d, (c-p), setup in every iteration to minimize the Lmax
    # weights of the weighted sum wre chosen empirically and are dependant on n
    c = [-1] * n    # completion times
    schedule = []
    lmax = -MAX_INT
    instant = 0
    cp_weight = n**0.22
    setup_weight = n**0.6

    while len(schedule) < n:
        schedule_goal = MAX_INT
        schedule_candidate = -1
        c_candidate = MAX_INT
        lateness_candidate = -MAX_INT

        for j in range(0, n):
            if c[j] == -1:      # task wasn't already scheduled
                setup = (0 if len(schedule) == 0 else s[schedule[-1]][j])
                tmp_c = max(instant + setup, r[j]) + p[j]     # completion time

                tmp_lateness = tmp_c - d[j]
                goal = d[j] / 3 + (tmp_c - p[j]) * cp_weight + setup * setup_weight
                if goal < schedule_goal \
                        or (goal == schedule_goal and tmp_c - r[j] < c_candidate - r[schedule_candidate]) \
                        or (goal == schedule_goal and tmp_c - r[j] == c_candidate - r[schedule_candidate] and tmp_c < c_candidate) \
                        or (goal == schedule_goal and tmp_c - r[j] == c_candidate - r[schedule_candidate] and tmp_c == c_candidate and tmp_lateness < lateness_candidate) \
                        or (goal == schedule_goal and tmp_c - r[j] == c_candidate - r[schedule_candidate] and tmp_c == c_candidate and tmp_lateness == lateness_candidate and j < schedule_candidate):
                    schedule_goal = goal
                    schedule_candidate = j
                    c_candidate = tmp_c
                    lateness_candidate = tmp_lateness

        if schedule_candidate != -1:
            c[schedule_candidate] = c_candidate
            instant = c_candidate
            lmax = max(lmax, c_candidate - d[schedule_candidate])
            schedule.append(schedule_candidate)
        else:
            # SOMETHING WENT WRONG - JUMP BY 1
            instant += 1

    # Save output to file
    output_file = open(sys.argv[2], "w")
    output_file.write(f"{lmax}\n")
    for task in schedule:
        output_file.write(f"{task} ")
    output_file.close()

else:
    sys.exit("Please run the algorithm with correctly named input & output files:\n"
             + f"python {sys.argv[0]} [in_123456_n.txt] [out_123456_{student_id}_n.txt")
