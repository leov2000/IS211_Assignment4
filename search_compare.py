import time

def sequential_search(a_list, item):
    start = time.time()
    pos = 0
    found = False

    while pos < len(a_list) and not found:
        if a_list[pos] == item:
            found = True
        else:
            pos = pos+1

    end = time.time()

    return (found, end- start)

def ordered_sequential_search(a_list, item):
    start = time.time()
    pos = 0
    found = False
    stop = False

    while pos < len(a_list) and not found and not stop:
        if a_list[pos] == item:
            found = True
        else:
            if a_list[pos] > item:
                stop = True
            else:
                pos = pos+1
    end = time.time()
                
    return (found, end - start)

def binary_search_iterative(a_list, item):
    start = time.time()

    first = 0
    last = len(a_list) - 1
    found = False

    while first <= last and not found:
        midpoint = (first + last) // 2
        if a_list[midpoint] == item:
            found = True
        else:
            if item < a_list[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1
    end = time.time()            

    return (found, end - start) 

def binary_search_recursive(a_list, item, add_time = 0):
    start = time.time() + add_time
    if len(a_list) == 0:
        end = time.time()
        return (False, start - end)
    else:
        midpoint = len(a_list) // 2
    if a_list[midpoint] == item:
        end = time.time()
        return (True, start - end)
    else:
        if item < a_list[midpoint]:
            end = time.time()
            return binary_search_recursive(a_list[:midpoint], item, start)
        else:
            end = time.time()
            return binary_search_recursive(a_list[midpoint + 1:], item, start) 


