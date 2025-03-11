

# Variant 10

MATRIX = [
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 1, 1, 2, 2, 2],
    [2, 2, 2, 2, 2, 8, 2, 2, 2, 2],
    [2, 1, 3, 8, 1, 0, 1, 3, 8, 1],
    [2, 1, 3, 8, 1, 0, 1, 3, 8, 1],
    [2, 1, 2, 9, 5, 4, 1, 2, 9, 5],
    [2, 1, 2, 2, 2, 1, 1, 2, 2, 2],
    [2, 2, 2, 2, 2, 8, 2, 2, 2, 2],
    [2, 1, 3, 8, 1, 0, 1, 3, 8, 2],
    [2, 1, 3, 8, 1, 0, 0, 3, 8, 1],
]




def main():

    summa_elements = sum(x for row_index, row in enumerate(MATRIX) for colum_num_index, x in enumerate(row) if colum_num_index > row_index)
    amount_of_local_minimum_number_full_way = get_local_minimum_full_way()
    amount_of_local_minimum_number_nearby_way = get_local_minimum_nearby_way()

    print(f'summa elements that above the general diagonal: {summa_elements}')
    print(f'Amount of local minimum number in row and colum full way : {amount_of_local_minimum_number_full_way}')
    print(f'Amount of local minimum number in row and colum nearby way : {amount_of_local_minimum_number_nearby_way}')



def get_local_minimum_full_way():
    local_minimum_number_indexes = []

    for row_index, row in enumerate(MATRIX):
        temp_smallest_number = row[0]
        temp_smallest_number_index = tuple((row_index, 0))
        continue_flag = False

        for colum_num_index, colum_number in enumerate(row):
            if colum_num_index > 0 and colum_number < temp_smallest_number:
                temp_smallest_number_index = (row_index, colum_num_index)
                temp_smallest_number = colum_number
            elif colum_num_index > 0 and colum_number == temp_smallest_number:
                continue_flag = True
                break

        if continue_flag:
            continue

        temp_smallest_number = MATRIX[temp_smallest_number_index[0]][temp_smallest_number_index[1]]
        access_to_append_flag = True

        for row_2 in MATRIX:
            if row_2[temp_smallest_number_index[1]] < temp_smallest_number:
                access_to_append_flag = False
                break

        if access_to_append_flag:
            local_minimum_number_indexes.append(temp_smallest_number_index)

    return len(local_minimum_number_indexes)




def get_local_minimum_nearby_way():
    local_minimum_number_indexes = []

    for row_index , row in enumerate(MATRIX):
       for colum_num_index, colum_number in enumerate(row):
           if row_index > 0 and colum_number >= MATRIX[row_index-1][colum_num_index]:
               continue
           if row_index < len(MATRIX)-1 and colum_number >= MATRIX[row_index + 1][colum_num_index]:
               continue
           if colum_num_index > 0 and colum_number >= MATRIX[row_index][colum_num_index-1]:
               continue
           if colum_num_index > len(MATRIX[0])-1 and colum_number >= MATRIX[row_index][colum_num_index+1]:
               continue

           local_minimum_number_indexes.append((row_index, colum_num_index))

    return  len(local_minimum_number_indexes)



if __name__ == '__main__':
    main()
