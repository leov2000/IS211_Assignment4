import time
import datetime
from random import randint, shuffle
import json


def insertion_sort(a_list):
    start_time = datetime.datetime.utcnow()
    for index in range(1, len(a_list)):

        current_value = a_list[index]
        position = index

    while position > 0 and a_list[position - 1] > current_value:
        a_list[position] = a_list[position - 1]
        position = position - 1

    a_list[position] = current_value

    end_time = datetime.datetime.utcnow()

    return (end_time - start_time)


def shell_sort(a_list):
    start_time = datetime.datetime.utcnow()
    sublist_count = len(a_list) // 2

    while sublist_count > 0:

        for start_position in range(sublist_count):
            gap_insertion_sort(a_list, start_position, sublist_count)

        sublist_count = sublist_count // 2

    end_time = datetime.datetime.utcnow()

    return (end_time - start_time)


def gap_insertion_sort(a_list, start, gap):
    start_time = datetime.datetime.utcnow()

    for i in range(start + gap, len(a_list), gap):

        current_value = a_list[i]
        position = i

        while position >= gap and a_list[position - gap] > current_value:
            a_list[position] = a_list[position - gap]
            position = position - gap

        a_list[position] = current_value

    end_time = datetime.datetime.utcnow()

    return (end_time - start_time)


def python_sort(a_list):
    start_time = datetime.datetime.utcnow()
    a_list.sort()
    end_time = datetime.datetime.utcnow()

    return end_time - start_time


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

    sum_dates = sum(date_list, datetime.timedelta())
    average = sum_dates / len(date_list)

    return average


def call_fn_with_list(fn, num):
    """
    A utility function used to trigger the benchmark-ing mechanism 
        Parameters:
            fn(function)
            num(int)

        Returns:
            A dictionary with the results.  
    """

    n_list = get_lists_of_100(num)
    benchmark_list = [fn(int_list) for int_list in n_list]
    average = get_average_time(benchmark_list)

    results_dict = {
        'function_name': fn.__name__,
        'list_size': num,
        'average': average,
    }

    return results_dict


def run_benchmark(size_list, fn_list):
    """
    The primary benchmark function

        Parameters:
            size_list(list[int])
            fn_list(list[function])

        Returns:
            A list of average benchmarks.
    """

    result_list = []

    for fn in fn_list:
        for size in size_list:
            result_list.append(call_fn_with_list(fn, size))

    return result_list


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
    function_name = avg_dict.get('function_name')

    return (average, list_size, format_fn_name(function_name))


def print_results(results_list):
    """
    A utility function used to print out the results of the benchmark. 

        Parameters:
            results_list(list)

        Prints:
            A formatted message with the details of the benchmark.
    """

    for avg in results_list:
        (avg, list_size, fn_name) = get_keys(avg)

        print(
            '<%s> took %10.7f seconds to run,\non average on a list size of %s'
            % (fn_name, avg.total_seconds(), list_size))
        print('-' * 70)


def write_to_json(results_dict):
    """
    A utility function used to store the benchmark results into JSON format file.

        Parameters:
            results_dict(dict)

        Writes:
            A JSON file with the results.     
    """

    with open('benchmark-sort-meta.json', 'w') as json_file:
        json.dump(results_dict, json_file, indent=4, default=str)


def main():
    """
    The main function that bootstraps the app.

        Parameters: None

        Returns: None
    """

    sizes = [500, 1000, 10000]

    function_list = [
        insertion_sort,
        shell_sort,
        python_sort
    ]

    sort_results = run_benchmark(sizes, function_list)

    print_results(sort_results)

    write_to_json({
        'sort_results': sort_results
    })


if __name__ == '__main__':
    main()
