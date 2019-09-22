import time
import datetime
from random import randint, shuffle


def sequential_search(a_list, item):
    start = datetime.datetime.utcnow()
    pos = 0
    found = False

    while pos < len(a_list) and not found:
        if a_list[pos] == item:
            found = True
        else:
            pos = pos + 1
    end = datetime.datetime.utcnow()
    print(end-start, 'end-start')
    return (found, (end - start))


def ordered_sequential_search(a_list, item):
    start = datetime.datetime.utcnow()
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
                pos = pos + 1

    end = datetime.datetime.utcnow()

    return (found, (end - start))


def binary_search_iterative(a_list, item):
    start = datetime.datetime.utcnow()

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

    end = datetime.datetime.utcnow()

    return (found, (end - start))


def binary_search_recursive(a_list, item):
    start = datetime.datetime.utcnow()

    def trampoline_rec_func(a_list, item):
        if len(a_list) == 0:
            return False
        else:
            midpoint = len(a_list) // 2
        if a_list[midpoint] == item:
            return True
        else:
            if item < a_list[midpoint]:
                return trampoline_rec_func(a_list[:midpoint], item)
            else:
                return trampoline_rec_func(a_list[midpoint + 1:], item)

    result = trampoline_rec_func(a_list, item)
    end = datetime.datetime.utcnow()

    return (result, (end - start))


def generate_random_list(range_size=500):
    num_list = list(range(1, range_size + 1))
    shuffle(num_list)

    return num_list


def generate_lists(num):
    random_lists = [generate_random_list(num) for n in range(0, 100)]

    return random_lists


def get_average_time(date_list):
    filter_for_date = [date for (result, date) in date_list]
    sum_dates = sum(filter_for_date, datetime.timedelta())
    average = sum_dates / len(date_list)

    return average


def benchmark(fn, num, search_for, sorted_list=None):
    n_list = generate_lists(num) if sorted_list is None else sorted_list
    benchmark_list = [fn(int_list, search_for) for int_list in n_list]
    average = get_average_time(benchmark_list)

    results_dict = {
        'function_name': fn.__name__,
        'list_size': num,
        'query': search_for,
        'average': average,
        'sorted': True if sorted_list else False 
    }

    return results_dict


def test_benchmark_lists(size_list, fn_list, search_for=None):
    result_list = []

    for i, fn in enumerate(fn_list):
        for size in size_list:
            search_for = randint(0, size) if search_for is None else search_for
            if i > 0:
                n_lists = generate_lists(size)
                n_lists = list(map(sorted, n_lists))
                result_list.append(benchmark(fn, size, search_for, n_lists))
            else:
                result_list.append(benchmark(fn, size, search_for))
    return result_list


def activate():
    sizes = [500, 1000, 10000]

    function_list = [
        sequential_search, ordered_sequential_search, binary_search_iterative,
        binary_search_recursive
    ]

    positive_results = test_benchmark_lists(sizes, function_list)
    worse_case_results = test_benchmark_lists(sizes, function_list, -1)

    print(positive_results)
    print(worse_case_results)


def main():
    activate()


if __name__ == "__main__":
    main()
