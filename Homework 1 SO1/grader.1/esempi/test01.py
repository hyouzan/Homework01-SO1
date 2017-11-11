import program01

examples = []
#https://en.wikipedia.org/wiki/Round-robin_scheduling#/media/File:Round_Robin_Schedule_Example.jpg
examples += [{}]
examples[-1]["quantum"] = 3
examples[-1]["max_procs"] = 10
examples[-1]["procs"] = [[0, 1], [0, 2], [0, 4], [0, 6], [0, 8], [11, 8], [11, 6], [11, 4], [11, 2], [11, 1]]
examples[-1]["max_sim"] = sum([proc[1] for proc in examples[-1]["procs"]]) + 1
#https://en.wikipedia.org/wiki/Round-robin_scheduling
examples += [{}]
examples[-1]["quantum"] = 100
examples[-1]["max_procs"] = 10
examples[-1]["procs"] = [[0, 250], [50, 170], [130, 75], [190, 100], [210, 130], [350, 50]]
examples[-1]["max_sim"] = sum([proc[1] for proc in examples[-1]["procs"]]) + 1
#textbook
examples += [{}]
examples[-1]["quantum"] = 1
examples[-1]["max_procs"] = 10
examples[-1]["procs"] = [[0, 3], [2, 6], [4, 4], [6, 5], [8, 2]]
examples[-1]["max_sim"] = sum([proc[1] for proc in examples[-1]["procs"]]) + 1
examples += [{}]
examples[-1]["quantum"] = 4
examples[-1]["max_procs"] = 10
examples[-1]["procs"] = [[0, 3], [2, 6], [4, 4], [6, 5], [8, 2]]
examples[-1]["max_sim"] = sum([proc[1] for proc in examples[-1]["procs"]]) + 1
#max_sim = 
#textbook plus (random) I/O and one extra process (to be rejected)
examples += [{}]
examples[-1]["quantum"] = 1
examples[-1]["max_procs"] = 5
examples[-1]["procs"] = [[0, 3, 2, 3, 1, 1], [2, 6, 1, 2, 1, 5], [4, 4, 4, 4, 4, 1], [6, 5, 1, 2], [8, 2, 3, 2, 4, 6, 1, 2, 1, 2, 5, 2], [8, 2, 3, 4]]
examples[-1]["max_sim"] = 64
#quantum = 1

import json

for example in examples:
    print(json.dumps(json.loads(json.dumps(example), parse_float=lambda x: round(float(x), 3)), sort_keys=True))
    ss = program01.SchedulerSimulator(example["quantum"], example["max_procs"])
    proc_i = 0
    already_cons = 0
    total_part = 0
    while proc_i < len(example["procs"]):
        while proc_i + 1 < len(example["procs"]) and example["procs"][proc_i][0] == example["procs"][proc_i + 1][0]:
            print("Added ", end="")
            print(json.dumps(json.loads(json.dumps(example["procs"][proc_i][1:]), parse_float=lambda x: round(float(x), 3)), sort_keys=True), end="")
            print(" with pid: %s" %(str(ss.add_proc(example["procs"][proc_i][1:]))))
            proc_i += 1
        print("Added ", end="")
        print(json.dumps(json.loads(json.dumps(example["procs"][proc_i][1:]), parse_float=lambda x: round(float(x), 3)), sort_keys=True), end="")
        print(" with pid: %s" %(str(ss.add_proc(example["procs"][proc_i][1:]))))
        total = example["procs"][proc_i + 1][0] if proc_i + 1 < len(example["procs"]) else example["max_sim"]
        proc_i += 1
        while total_part + example["quantum"] - already_cons <= total:
            ss.advance_time(example["quantum"] - already_cons)
            total_part += example["quantum"] - already_cons
            already_cons = 0
            print("After %.1lf units: " %total_part, end="")
            print(json.dumps(json.loads(json.dumps(ss.get_ready()), parse_float=lambda x: round(float(x), 3)), sort_keys=True), end="")
            print(" ", end="")
            print(json.dumps(json.loads(json.dumps(ss.get_blocked()), parse_float=lambda x: round(float(x), 3)), sort_keys=True), end="")
            print(" ", end="")
            print(json.dumps(json.loads(json.dumps(ss.get_running()), parse_float=lambda x: round(float(x), 3)), sort_keys=True))
        if total > total_part:
            ss.advance_time(total - total_part)
            already_cons += total - total_part
            total_part = total
            print("After %.1lf units: " %total_part, end="")
            print(json.dumps(json.loads(json.dumps(ss.get_ready()), parse_float=lambda x: round(float(x), 3)), sort_keys=True), end="")
            print(" ", end="")
            print(json.dumps(json.loads(json.dumps(ss.get_blocked()), parse_float=lambda x: round(float(x), 3)), sort_keys=True), end="")
            print(" ", end="")
            print(json.dumps(json.loads(json.dumps(ss.get_running()), parse_float=lambda x: round(float(x), 3)), sort_keys=True))
        else:
            already_cons = 0
    print("\n")
