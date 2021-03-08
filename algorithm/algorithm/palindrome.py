import collections
from typing import Deque
import timeit

def isPalindrome(s:str) -> bool:
    start_time = timeit.default_timer()
    strs = []

    for char in s:
        if char.isalpha():
            strs.append(char.lower())

    while len(strs) > 1:
        if strs.pop(0) != strs.pop():
            return False
    
    terminate_time = timeit.default_timer()
    print("strs %f seconde" % (terminate_time - start_time))
    return True

def isPalindrome_deque(s: str) -> bool:
    start_time = timeit.default_timer()
    strs:Deque = collections.deque()

    for char in s:
        if char.isalpha():
            strs.append(char.lower())

    while len(strs) > 1:
        if strs.popleft() != strs.pop():
            return False

    terminate_time = timeit.default_timer()
    print("deque %f seconde" % (terminate_time - start_time))
    return True

st = "A man, a plan, a canal: Panama"
print("{0}".format(isPalindrome(st)))
print("{0}".format(isPalindrome_deque(st)))
