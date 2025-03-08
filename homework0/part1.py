
# Variant 3



# В задании не указано какая именна должна быть матрица , если нужно можно сделать динамически заполняемой
matrix = [
    [4,1,2,9,5],
    [1,1,2,2,2],
    [8,2,2,2,2],
    [0,1,3,8,1],
]



def main():

    amount_largest_number_line = 0
    index_largest_row_number = None
    amount_colum_with_zero = 0
    checked_colum = []


    i = 0
    index_of_row = 0

    for row in matrix:
        last_number = None
        temp_largest_number_line = 0


        while i < len(row):
            if row[i] == 0 and i not in checked_colum:
                checked_colum.append(i)
                amount_colum_with_zero += 1
            if last_number is not None and row[i] == last_number:
                temp_largest_number_line+=1
            else:
                temp_largest_number_line = 0

            last_number = row[i]
            i+=1


        if amount_largest_number_line < temp_largest_number_line:
            amount_largest_number_line = temp_largest_number_line
            index_largest_row_number = index_of_row

        index_of_row += 1
        i = 0

    print("Количество столбцов содержащих 0: " + str(amount_colum_with_zero) )
    print("Index строки с самым длинным повторением одного и того же числа: " +str(index_largest_row_number))


main()





