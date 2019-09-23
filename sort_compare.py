import time
import datetime
from random import randint, shuffle


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

def python_sort(list):
    start_time = datetime.datetime.utcnow()
    list.sort()
    end_time = datetime.datetime.utcnow()

    return end_time - start_time


def format_fn_name(fn_str):
    remove_underscore = fn_str.split('_')
    capitalize_str = [fn_str.capitalize() for fn_str in remove_underscore]
    format_result = ' '.join(capitalize_str)

    return format_result


def generate_random_list(range_size=500):
    num_list = list(range(1, range_size + 1))
    shuffle(num_list)

    return num_list


def generate_lists(num):
    random_lists = [generate_random_list(num) for n in range(0, 100)]

    return random_lists


def get_average_time(date_list):
    filter_for_date = [date for date in date_list]
    sum_dates = sum(filter_for_date, datetime.timedelta())
    average = sum_dates / len(date_list)

    return average


def benchmark(fn, num):
    n_list = generate_lists(num)
    benchmark_list = [fn(int_list) for int_list in n_list]
    average = get_average_time(benchmark_list)

    results_dict = {
        'function_name': fn.__name__,
        'list_size': num,
        'average': average,
    }

    return results_dict

def test_benchmark_lists(size_list, fn_list, search_for=None):
    result_list = []

    for fn in fn_list:
        for size in size_list:
            result_list.append(benchmark(fn, size))

    return result_list


def get_keys(avg_dict):
    average = avg_dict.get('average')
    list_size = avg_dict.get('list_size')
    function_name = avg_dict.get('function_name')

    return (average, list_size, format_fn_name(function_name))


def print_results(results_list):

    for avg in results_list:
        (avg, list_size, fn_name) = get_keys(avg)

        print(
            '<%s> took %10.7f seconds to run,\non average on a list size of %s'
            % (fn_name, avg.total_seconds(), list_size))
        print('-' * 70)


def main():
    sizes = [500, 1000, 10000]

    function_list = [
        insertion_sort,
        shell_sort,
        python_sort
    ]

    sort_results = test_benchmark_lists(sizes, function_list)

    print_results(sort_results)


if __name__ == '__main__':
    main()
