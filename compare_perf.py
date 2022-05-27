import csv
from time import time
import tracemalloc
from typing import Callable, List
import random
import string
from os.path import exists
import hashlib

# Profile comparison
def profiler(funs: List[Callable], arg, goal:str, file):
    print(f"{goal} with {arg}")
    for fun in funs:
        start_time = time()
        tracemalloc.start()
        fun(arg)
        mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time()
        elapsed = end_time - start_time

        # Create id for this run
        hash = hashlib.sha1()
        hash.update(str(start_time).encode('utf-8'))
        id = str(hash.hexdigest()[:12])
        file.writerow([f'{id}', f'{goal}', f'{fun.__name__}', f'{arg}', f'{elapsed}', f'{mem[1]}'])
        print(f"{fun.__name__:24} Time: {elapsed:.4f} seconds.\tPeak memory: {mem[1]} bytes")

# Generate sample documents for pattern match testing
def gen_sample_data(n):
    the_string = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=n))
    with open(f'input/sample_{n}_chars.txt', 'w') as f:
        f.write(the_string)

# Comparing methods for List[int] generation
class intArrayCosts:
    def range_append(n):
        l = []
        for i in range(n):
                l.append(i)
        
    def zero_array(n):
        l = [0] * n
        for i in range(n):
                l[i] = i

    def comprehension(n):
        [i for i in range(n)]

    def generator(n):
        list(i for i in range(n))


# Comparing methods for string generation
class stringCreateCosts():
    def string_append(n):
        the_string = ''
        for _ in range(n):
            the_string += random.choice(string.ascii_letters + string.digits + string.punctuation)

    def array_append(n):
        temp = []
        for _ in range(n):
            temp.append(random.choice(string.ascii_letters + string.digits + string.punctuation))
        the_string = ''.join(temp)

    def comprehension(document):
        the_string = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(n))

    def random_choices(n):
        the_string = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=n))

# Comparing methods for string pattern matching
class stringMatch:
    def read_file(n) -> str:
        with open(f'input/sample_{n}_chars.txt') as f:
            the_string = f.read()
        return the_string

    def string_append(n):
        the_string = stringMatch.read_file(n)
        letters = ''
        for l in the_string:
            if l.isalpha():
                letters += l

    def array_append(n):
        the_string = stringMatch.read_file(n)
        temp = []
        for l in the_string:
            if l.isalpha():
                temp.append(l)
        letters = ''.join(temp)

    def comprehension(n):
        the_string = stringMatch.read_file(n)
        letters = ''.join([l for l in the_string if l.isalpha()])

    def generator(n):
        the_string = stringMatch.read_file(n)
        letters = ''.join(l for l in the_string if l.isalpha())

if __name__ == '__main__':
    run_log = "perf_log.csv"
    if not exists(run_log):
        run_log_file = csv.writer(open(run_log, 'w'))
        run_log_file.writerow(['id', 'goal', 'function', 'arg', 'time_elapsed', 'max_memory'])
    else:
        run_log_file = csv.writer(open(run_log, 'a'))
    
    for n in [100, 1000, 10000, 100000, 1000000, 10000000, 100000000]:
        print(f"----------------------------RUNNING WITH {n}----------------------------\n")
        for c in [intArrayCosts, stringCreateCosts, stringMatch]:
            profiler([getattr(c,attribute) for attribute in dir(c) if callable(getattr(c, attribute)) and attribute.startswith('__') is False], n, f'{c.__name__}', run_log_file)
            print("")