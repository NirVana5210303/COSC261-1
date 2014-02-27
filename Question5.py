import itertools
def all_strings(s, k):
    total=[]
    final=[]
    alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    alphabet_upper_case = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    
    for i in range(0,200):  # If the number inside of list
        if i in s:
            total.append(i)
            
    for i in alphabet_upper_case: #If the Upper case letter inside of the list
        if i in s:
            total.append(i)
            
    for i in alphabet:  # If the lower case letter inside of the list
        if i in s:
            total.append(i)
    result = list(itertools.product(total,repeat=k))
    ff = []        #make the string become list and showing on the final result
    for p in result:
        ff = ff + [list(p)]
    return ff


print(all_strings({'a','b','c'}, 2))
print(all_strings({'a','b','c'}, 1))
print(all_strings({'a','b','c'}, 0))