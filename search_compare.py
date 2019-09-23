import time
import datetime
from random import randint, shuffle
import json


def sequential_search(a_list, item):
    start_time = datetime.datetime.utcnow()
    pos = 0
    found = False

    while pos < len(a_list) and not found:
        if a_list[pos] == item:
            found = True
        else:
            pos = pos + 1
    end_time = datetime.datetime.utcnow()

    return (found, (end_time - start_time))


def ordered_sequential_search(a_list, item):
    start_time = datetime.datetime.utcnow()
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

    end_time = datetime.datetime.utcnow()

    return (found, (end_time - start_time))


def binary_search_iterative(a_list, item):
    start_time = datetime.datetime.utcnow()

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

    end_time = datetime.datetime.utcnow()

    return (found, (end_time - start_time))


def binary_search_recursive(a_list, item):
    start_time = datetime.datetime.utcnow()

    # placed the recursive call within a trampoline recursive
    # fn to get a better handle on the start - end time.
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
    end_time = datetime.datetime.utcnow()

    return (result, (end_time - start_time))


def get_random_list(range_size=500):
    """
    A utility function that creates a list given a range size
    and randomizes it using the shuffle method

        Parameters:
            range_size(int)

        Returns:
            A list of shuffled ints 
    """

    num_list = list(range(1, range_size + 1))
    shuffle(num_list)

    return num_list


def get_lists_of_100(num):
    """
    A utility function that creates a list of 100 and invokes the the generate_random_list fn 

        Parameters:
            num(int)

        Returns:
            A list of ints 
    """

    random_lists = [get_random_list(num) for n in range(0, 100)]

    return random_lists


def get_average_time(date_list):
    """
    A utility function which gives the average time by summing the 
    time deltas and dividing it by the length of the list 

        Parameters:
            date_lists(list[<time-delta>])

        Returns:
            An average. 
    """

    filter_for_date = [date for (result, date) in date_list]
    sum_dates = sum(filter_for_date, datetime.timedelta())
    average = sum_dates / len(date_list)

    return average


def call_fn_with_list(fn, num, search_for, sorted_list=None):
    """
    A utility function used to trigger the benchmark-ing mechanism 
        Parameters:
            fn(function)
            num(int)
            search_for(int)
            sorted_list(list[int])

        Returns:
            A dictionary with the results.  
    """

    n_list = get_lists_of_100(num) if sorted_list is None else sorted_list
    benchmark_list = [fn(int_list, search_for) for int_list in n_list]
    average = get_average_time(benchmark_list)

    results_dict = {
        'function_name': fn.__name__,
        'list_size': num,
        'query': search_for,
        'average': average,
        'is_sorted': True if sorted_list else False
    }

    return results_dict


def run_benchmark(size_list, fn_list, search_for=None):
    """
    The primary benchmark function

        Parameters:
            size_list(list[int])
            fn_list(list[function])

        Returns:
            A list of average benchmarks.
    """

    result_list = []

    for i, fn in enumerate(fn_list):
        for size in size_list:
            search_for = randint(0, size) if search_for is None else search_for
            if i > 0:
                n_lists = get_lists_of_100(size)
                n_lists = list(map(sorted, n_lists))
                result_list.append(call_fn_with_list(
                    fn, size, search_for, n_lists))
            else:
                result_list.append(call_fn_with_list(fn, size, search_for))
    return result_list


def format_fn_name(fn_str):
    """
    A utility function used to sentence case function names with underscores
        Parameters:
            fn_str(str)

        Returns:
            A sentence cased string     
    """

    remove_underscore = fn_str.split('_')
    capitalize_str = [fn_str.capitalize() for fn_str in remove_underscore]
    format_result = ' '.join(capitalize_str)

    return format_result


def get_keys(avg_dict):
    """
    A utility function used to get keys and values and format the function name

        Parameters:
            avg_dict(dict)

        Returns:
            A tuple with the values expected.
    """

    average = avg_dict.get('average')
    list_size = avg_dict.get('list_size')
    query = avg_dict.get('query')
    function_name = avg_dict.get('function_name')
    is_sorted = avg_dict.get('is_sorted')

    return (average, list_size, query, format_fn_name(function_name),
            is_sorted)


def print_results(results_list):
    """
    A utility function used to print out the results of the benchmark. 

        Parameters:
            results_list(list)

        Prints:
            A formatted message with the details of the benchmark.
    """

    for avg in results_list:
        (avg, list_size, query, fn_name, is_sorted) = get_keys(avg)

        sort_str = 'pre-sorted' if is_sorted else 'not-sorted'
        query_type = 'positive' if query > 0 else 'negative'

        print(
            '<%s> took %10.7f seconds to run,\non average on a list size of %s that was %s using\nthe following %s query: %s'
            % (fn_name, avg.total_seconds(), list_size, sort_str, query_type,
               query))
        print('-' * 70)


def write_to_json(results_dict):
    """
    A utility function used to store the benchmark results into JSON format file.

        Parameters:
            results_dict(dict)

        Writes:
            A JSON file with the results.   
    """

    with open('benchmark-search-meta.json', 'w') as json_file:
        json.dump(results_dict, json_file, indent=4, default=str)


def main():
    """
    The main function that bootstraps the app.

        Parameters: None

        Returns: None
    """

    sizes = [500, 1000, 10000]

    function_list = [
        sequential_search, ordered_sequential_search, binary_search_iterative,
        binary_search_recursive
    ]

    regular_case_results = run_benchmark(sizes, function_list)
    worse_case_results = run_benchmark(sizes, function_list, -1)

    print_results(regular_case_results)
    print_results(worse_case_results)

    write_to_json({
        'regular_case_results': regular_case_results,
        'worse_case_results': worse_case_results
    })


if __name__ == '__main__':
    main()
