

#Variant 20


matrix = [
    [2,3,5,2],
    [2,4,6,2],
    [-2,7,2,0]
]



def main():



    row_index_negative_number = []
    list_min_in_row = []
    list_max_in_colum = []


    i = 0


    while i < len(matrix):
        temp_amount_negative_number = 0
        check = False

        for element in matrix[i]:
            if element < 0:
                temp_amount_negative_number += 1
            if element == 0:
                check = True


        if check:
            check = False
            row_index_negative_number.append([i, temp_amount_negative_number])
            temp_amount_negative_number = 0


        i+= 1





    for for_I in range(len(matrix)+1):
        temp_min_num = None
        temp_max_num = 0
        temp_min_num_indexes = []
        temp_max_num_indexes = []

        for for_J in range(len(matrix[0])):
            if for_I < len(matrix):
                if temp_min_num is None or matrix[for_I][for_J] < temp_min_num:
                    temp_min_num = matrix[for_I][for_J]
                    temp_min_num_indexes = [for_I, for_J]
                elif temp_min_num is None or matrix[for_I][for_J] == temp_min_num:
                    list_min_in_row.append([for_I, for_J])


            if not for_J > len(matrix)-1:

                if matrix[for_J][for_I] > temp_max_num:
                    temp_max_num = matrix[for_J][for_I]
                    temp_max_num_indexes = [for_J,for_I]
                elif matrix[for_J][for_I] == temp_max_num:
                    list_max_in_colum.append([for_J, for_I])

        if for_I < len(matrix):
            list_min_in_row.append(temp_min_num_indexes)

        list_max_in_colum.append(temp_max_num_indexes)



    result = []


    for element_indexes in list_min_in_row:
        for second_element_indexes in list_max_in_colum:
            if element_indexes[0] == second_element_indexes[0] and element_indexes[1] == second_element_indexes[1]:
                result.append(element_indexes)




    for element in result:
        print("Седловое число матрици с i и j: " + str(element[0]) + " " + str(element[1]))











    for element in row_index_negative_number:
        print("index ряда:" + str(element[0]))
        print("количество элементов меньше 0: " + str(element[1]))


main()