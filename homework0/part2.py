

# Variant 10



matrix = [
    [4, 1, 2, 9, 5, 4, 1, 2, 9, 5],
    [1, 2, 2, 2, 2, 1, 1, 2, 2, 2],
    [8, 2, 2, 2, 2, 8, 2, 2, 2, 2],
    [0, 1, 3, 8, 1, 0, 1, 3, 8, 1],
    [0, 1, 3, 8, 1, 0, 1, 3, 8, 1],
    [4, 1, 2, 9, 5, 4, 1, 2, 9, 5],
    [1, 1, 2, 2, 2, 1, 1, 2, 2, 2],
    [8, 2, 2, 2, 2, 8, 2, 2, 2, 2],
    [0, 1, 3, 8, 1, 0, 1, 3, 8, 2],
    [0, 1, 3, 8, 1, 0, 1, 3, 8, 1],
]




def main():
    local_minimum_indexes = []
    summa_modules_of_elements = 0


    i = 0
    j = 0

    while i < len(matrix):
        while j < len(matrix[i]):
            temp_j = j
            num = matrix[i][temp_j]
            j += 1


            if temp_j > i:
                summa_modules_of_elements += abs(num)

            if i != 0:
                if num >= matrix[i - 1][temp_j]:
                    continue
            if temp_j != 0:
                if num >= matrix[i][temp_j - 1]:
                    continue
            if i != len(matrix)-1:
                if num >= matrix[i + 1][temp_j]:
                    continue
            if temp_j != len(matrix[0]) - 1:
                if num >= matrix[i][temp_j+1]:
                    continue



            local_minimum_indexes.append([i,temp_j])




        j=0
        i+=1

    print("Количество локальних минимумов: " + str(len(local_minimum_indexes)))
    print("Их индексы: ")
    for array_of_indexes in local_minimum_indexes:
        print(array_of_indexes[0], array_of_indexes[1])


    print("Сумма модулей элементов више главное диагонали: " + str(summa_modules_of_elements))













main()