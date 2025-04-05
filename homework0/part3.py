from collections import Counter


#Variant 20


MATRIX = [
    [ 1, 3, 1, 1],
    [ 0, 4, 0, 0],
    [ 0, 7, 0, 0],
    [ 0,-2, -3, 0],
    [ 0, 7, 0, 0],
]


def main():
    amount_negative_number_tuple_list = get_amount_negative_number_indexes()
    saddle_amount = get_saddle_number_amount()

    print(f'Negative numbers in row Counter : {amount_negative_number_tuple_list}')
    print(f'Saddle amount: {saddle_amount}')


def get_saddle_number_amount():
    saddle_number_indexes = []

    for index_row , row in enumerate(MATRIX):
        minimum_number_indexes_in_row = []
        temp_smallest_number = row[0]

        for index_column_number, column_number in enumerate(row):
            if column_number < temp_smallest_number:
                minimum_number_indexes_in_row.clear()
                minimum_number_indexes_in_row.append((index_row, index_column_number))
                temp_smallest_number = column_number
            elif column_number == temp_smallest_number:
                minimum_number_indexes_in_row.append((index_row, index_column_number))

        for indexes in minimum_number_indexes_in_row:
            flag_to_push = True

            for i in range(len(MATRIX)):
                if MATRIX[indexes[0]][indexes[1]] < MATRIX[i][indexes[1]]:
                    flag_to_push = False
                    break

            if flag_to_push:
                saddle_number_indexes.append(indexes)

    return len(saddle_number_indexes)


def get_amount_negative_number_indexes():
    return Counter(
        list(element[0] for element in
            (
                (row_index, colum_index, num)
                for row_index, row in enumerate(MATRIX)
                if 0 in row
                for colum_index, num in enumerate(row)
                if num < 0
            )
        )
    )


if __name__ == '__main__':
    main()
