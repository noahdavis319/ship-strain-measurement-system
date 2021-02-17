
import numpy as np
import time
import functools

_timings = {}

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        if not func.__name__ in _timings.keys():
            _timings[func.__name__] = [0, []] 
            
        start_time = time.perf_counter()    
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      
        run_time = (end_time - start_time) * 1000
        
        _timings[func.__name__][0] += 1
        _timings[func.__name__][1].append(run_time)
        
        return value
    return wrapper_timer


def print_timing_results():
    #print(chr(27) + "[2J")
    print('\n')
    print('                           function name |   avg time |   min time |   max time |   total time |  total |')
    print('  ---------------------------------------|------------|------------|------------|--------------|--------|')
    averages = []
    tavg = 0
    tmin = 0
    tmax = 0
    for key in _timings.keys():
        count = _timings[key][0]
    
        avg = np.average(_timings[key][1])
        tavg += avg
        
        mint = np.min(_timings[key][1])
        tmin += mint
        
        maxt = np.max(_timings[key][1])
        tmax += maxt
        
        tot = (_timings[key][0] * avg) / 1000
        averages.append(avg)

        print(f'{key:>40} | {avg:>7.4f} ms | {mint:>7.4f} ms | {maxt:>7.4f} ms | {tot:>10.4f} s | {count:>6d} |')

    print('\n')
    print(f'Total avg time: {tavg}')
    print(f'Total min time: {tmin}')
    print(f'Total max time: {tmax}')
    
