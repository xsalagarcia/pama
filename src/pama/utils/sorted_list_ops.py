from bisect import insort, bisect_left
from typing import TypeVar

T = TypeVar('T')

def insert(sorted_list: list[T], element: T):
    insort(sorted_list, element)

def binary_search(sorted_list: list[T], element: T) -> int:
    """
    Find the index of element in sorted_list.
    :param sorted_list:
    :param element: Element to search for.
    :return: The index of the element in the sorted list. -1 if not found.
    """
    index = bisect_left(sorted_list, element)
    if index < len(sorted_list) and sorted_list[index] == element:
        return index
    else:
        return -1

def delete(sorted_list: list[T], element: T) -> T | None:
    """
    Delete element from sorted_list.
    :param sorted_list:
    :param element:
    :return: The element to be deleted or None if not found.
    """
    position = bisect_left(sorted_list, element)
    if position != -1:
        sorted_list.pop(position)
        return element
    else:
        return None

def find_predecessor(sorted_list: list[T], element: T) -> T | None:
    """
    Return the predecessor of element from sorted_list. If there is no predecessor, return None.
    :param sorted_list:
    :param element:
    :return:
    """
    index = bisect_left(sorted_list, element)
    if index > 0:
        return sorted_list[index - 1]
    else:
        return None