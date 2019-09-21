def insertion_sort(a_list):
    for index in range(1, len(a_list)):

        current_value = a_list[index]
        position = index
    
    while position > 0 and a_list[position - 1] > current_value:
        a_list[position] = a_list[position - 1]
        position = position - 1

    a_list[position] = current_value

def shell_sort(a_list):
    sublist_count = len(a_list)//2
    while sublist_count > 0:

        for start_position in range(sublist_count):
            gap_insertion_sort(a_list, start_position, sublist_count)

        print("After increments of size", sublist_count,
                                    "The list is", a_list)

        sublist_count = sublist_count // 2

def gap_insertion_sort(a_list,start,gap):
    for i in range(start + gap, len(a_list), gap):

        current_value = a_list[i]
        position = i

        while position >= gap and a_list[position - gap] > current_value:
            a_list[position] = a_list[position - gap]
            position = position - gap

        a_list[position] = current_value


def python_sort(list);
    list.sort()

