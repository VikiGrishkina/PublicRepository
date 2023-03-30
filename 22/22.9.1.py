s=input('Введите числа через пробел: ')
element=int(input('Введите число: '))
array=list(map(int, list(s.split())))

def sort_bubble(array):
    for i in range(len(array)):
        for j in range(len(array)-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
    return(array)

def binary_search(array, element, left, right):
    if left > right:  # если левая граница превысила правую,
                        # значит элемент отсутствует
        if ((right + left) // 2) >= 0:
            return ((right + left) // 2)
        return False

    middle = (right + left) // 2  # находим середину
    if array[middle] == element:  # если элемент в середине,
        return middle-1  # возвращаем этот индекс
    elif element < array[middle]:  # если элемент меньше элемента в середине
    # рекурсивно ищем в левой половине
        return binary_search(array, element, left, middle - 1)
    else:  # иначе в правой
        return binary_search(array, element, middle + 1, right)
    #else:
    #    return 'элемент не входит в диапазон значений списка'

print("Отсортированный список:",sort_bubble(array))
if element>max(array) or element<min(array):
    print("Элемент выходит за диапазон списка")
else:
    print("Номер позиции искомого элемента:",binary_search(array, element, 0, len(array)))
