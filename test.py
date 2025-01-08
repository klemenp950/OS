def count(array):
    counter = 0
    for i in array:
        if i != 0:
            counter += 1
    return counter

array = [0, 5, 5, 5, 3, 0]

print(sum(array)/count(array))