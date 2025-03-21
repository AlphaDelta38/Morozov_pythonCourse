

# Variant 10

MATRIX = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
    [2, 2, 2, 2, 2, 1, 1, 2, 2, 2],
    [2, 2, 2, 2, 2, 8, 2, 2, 2, 2],
    [2, 1, 3, 8, 1, 0, 1, 3, 8, 2],
    [2, 1, 3, 8, 1, 1, 1, 3, 8, 2],
    [2, 1, 2, 9, 5, 4, 1, 2, 9, 5],
    [2, 1, 2, 2, 2, 1, 1, 2, 2, 2],
    [2, 2, 2, 2, 2, 0, 2, 2, 2, 2],
    [2, 1, 3, 8, 1, 1, 1, 3, 8, 2],
    [2, 0, 3, 8, 2, 2, 2, 3, 8, 1],
]




def main():

    summa_elements = sum(x for row_index, row in enumerate(MATRIX) for colum_num_index, x in enumerate(row) if colum_num_index > row_index)
    amount_of_local_minimum_number_full_way = get_local_minimum_full_way()
    amount_of_local_minimum_number_nearby_way = get_local_minimum_nearby_way()

    print(f'summa elements that above the general diagonal: {summa_elements}')
    print(f'Amount of local minimum number in row and colum full way : {amount_of_local_minimum_number_full_way}')
    print(f'Amount of local minimum number in row and colum nearby way : {amount_of_local_minimum_number_nearby_way}')
    print(f'Amount of local minimum number in row and colum nearby way (extend) : {len(get_local_minimum_nearby_extend_way())}')



def get_local_minimum_full_way():
    local_minimum_number_indexes = []

    for row_index, row in enumerate(MATRIX):
        temp_smallest_number = row[0]
        temp_smallest_colum_index = 0
        continue_flag = True

        for colum_num_index, colum_number in enumerate(row):
            if colum_num_index > 0:
                if colum_number < temp_smallest_number:
                    temp_smallest_colum_index = colum_num_index
                    temp_smallest_number = colum_number
                    continue_flag = True
                elif colum_number == temp_smallest_number:
                    continue_flag = False

        if not continue_flag:
            continue

        temp_smallest_number = MATRIX[row_index][temp_smallest_colum_index]
        append_flag = True

        for row_2 in MATRIX:
            if row_2[temp_smallest_colum_index] < temp_smallest_number:
                append_flag = False
                break

        if append_flag:
            local_minimum_number_indexes.append((row_index, temp_smallest_colum_index))

    return len(local_minimum_number_indexes)



def get_local_minimum_nearby_way():
    local_minimum_number_indexes = []

    for row_index , row in enumerate(MATRIX):
       for colum_num_index, colum_number in enumerate(row):
           if (row_index > 0 and colum_number >= MATRIX[row_index-1][colum_num_index]) or \
              (row_index < len(MATRIX)-1 and colum_number >= MATRIX[row_index + 1][colum_num_index]) or \
              (colum_num_index > 0 and colum_number >= MATRIX[row_index][colum_num_index-1]) or \
              (colum_num_index > len(MATRIX[0])-1 and colum_number >= MATRIX[row_index][colum_num_index+1]):
               continue

           local_minimum_number_indexes.append((row_index, colum_num_index))

    return  len(local_minimum_number_indexes)



def find_element_in_matrix(matrix, row_i, colum_i):
    if (len(matrix) - 1 < row_i or row_i <= 0) or \
       (len(matrix[0]) - 1 < colum_i or colum_i <= 0):
        return None

    return matrix[row_i][colum_i]



def get_local_minimum_nearby_extend_way():
    list_of_local_minimum_indexes = []
    list_of_excluded_indexes = []

    for row_index, row in enumerate(MATRIX):
        for colum_index, colum_number in enumerate(row):
            if not [row_index, colum_index] in list_of_excluded_indexes:
                number = MATRIX[row_index][colum_index]
                indexes_check_list = []

                for i in range(row_index - 1, row_index + 2):
                    for j in range(colum_index - 1, colum_index + 2):
                        if i != row_index or j != colum_index:
                            indexes_check_list.append([i, j])

                access_flag = True
                for indexes_i in range(len(indexes_check_list)):
                    check_number = find_element_in_matrix(MATRIX, indexes_check_list[indexes_i][0], indexes_check_list[indexes_i][1])
                    if check_number is None or number >= check_number:
                        access_flag = False
                        break

                if access_flag:
                    list_of_local_minimum_indexes.append([row_index, colum_index])
                    list_of_excluded_indexes.extend(indexes_check_list)

    return list_of_local_minimum_indexes


if __name__ == '__main__':
    main()
