import program02

examples = []
#textbook
examples += [{"P" : 2**10, "M": 5*(2**10), "Mp": 3*(2**10), "S": 2**20, "l" : [3]}]
examples[-1]["reqs"] = [(2*examples[-1]["P"] + 2**5, 0), (3*examples[-1]["P"] + 2**4, 0), (2*examples[-1]["P"] + 2**3, 0), (1*examples[-1]["P"] + 2**1, 0), (5*examples[-1]["P"] + 2**2, 0), (2*examples[-1]["P"] + 2**0, 0), (4*examples[-1]["P"] + 2**1, 0), (5*examples[-1]["P"] + 2**4, 0), (3*examples[-1]["P"] + 2**5, 0), (2*examples[-1]["P"] + 2**3, 0), (5*examples[-1]["P"] + 2**7, 0), (2*examples[-1]["P"] + 2**8, 0)]
#https://cs.stackexchange.com/questions/24011/clock-page-replacement-algorithm-already-existing-pages
examples += [{"P" : 2**10, "M": 8*(2**10), "Mp": 5*(2**10), "S": 2**20, "l" : [5]}]
examples[-1]["reqs"] = [(3*examples[-1]["P"] + 2**5, 0), (2*examples[-1]["P"] + 2**4, 0), (3*examples[-1]["P"] + 2**3, 0), (0*examples[-1]["P"] + 2**1, 0), (8*examples[-1]["P"] + 2**2, 0), (4*examples[-1]["P"] + 2**0, 0), (2*examples[-1]["P"] + 2**1, 0), (5*examples[-1]["P"] + 2**4, 0), (0*examples[-1]["P"] + 2**5, 0), (9*examples[-1]["P"] + 2**3, 0), (8*examples[-1]["P"] + 2**7, 0), (3*examples[-1]["P"] + 2**8, 0), (2*examples[-1]["P"] + 2**8, 0)]
#a mix
examples += [{"P" : 2**10, "M": 10*(2**10), "Mp": 8*(2**10), "S": 2**20, "l" : [5, 3]}]
examples[-1]["reqs"] = [(3*examples[-1]["P"] + 2**5, 0), (2*examples[-1]["P"] + 2**4, 0), (3*examples[-1]["P"] + 2**3, 0), (0*examples[-1]["P"] + 2**1, 0), (8*examples[-1]["P"] + 2**2, 0), (4*examples[-1]["P"] + 2**0, 0), (2*examples[-1]["P"] + 2**1, 0), (5*examples[-1]["P"] + 2**4, 0), (0*examples[-1]["P"] + 2**5, 0), (9*examples[-1]["P"] + 2**3, 0), (8*examples[-1]["P"] + 2**7, 0), (3*examples[-1]["P"] + 2**8, 0), (2*examples[-1]["P"] + 2**8, 0), (2*examples[-1]["P"] + 2**5, 1), (3*examples[-1]["P"] + 2**4, 1), (2*examples[-1]["P"] + 2**3, 1), (1*examples[-1]["P"] + 2**1, 1), (5*examples[-1]["P"] + 2**2, 1), (2*examples[-1]["P"] + 2**0, 1), (4*examples[-1]["P"] + 2**1, 1), (5*examples[-1]["P"] + 2**4, 1), (3*examples[-1]["P"] + 2**5, 1), (2*examples[-1]["P"] + 2**3, 1), (5*examples[-1]["P"] + 2**7, 1), (2*examples[-1]["P"] + 2**8, 1)]

import json

for example in examples:
    print(json.dumps(example, sort_keys=True))
    ms = program02.MemorySimulator(example["M"], example["Mp"], example["S"], example["P"], example["l"])
    for req in example["reqs"]:
        print("Handling request %d for proc %d" %(req[0], req[1]))
        print(str(ms.handle_request(req[0], req[1])))
        print("Page miss: " + str(ms.get_stats()[1]))
        print(str(ms.get_memory()))
    print("\n")
