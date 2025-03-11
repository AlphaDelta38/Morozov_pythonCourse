# Variant 3


MATRIX = [
    [4, 1, 2, 0, 0],
    [1, 1, 2, 2, 2],
    [1, 1, 1, 1, 0],
    [0, 1, 3, 8, 1],
]




def main():
    amount_of_zero_in_colum = get_amount_colum_with_zero()
    row_index = get_row_largest_number_strike()

    print(f"Amount of colum with zero: {amount_of_zero_in_colum}")
    print(f'Index of row with largest number strike: {row_index}')



def get_amount_colum_with_zero():
    amount_of_zero_elements = 0

    for colum_index, _ in enumerate(MATRIX[0]):
        for row_index, _ in enumerate(MATRIX):
            if MATRIX[row_index][colum_index] == 0:
                amount_of_zero_elements += 1
                break

    return amount_of_zero_elements




def get_row_largest_number_strike():
    current_strike = 1
    largest_row = None

    for i, row in enumerate(MATRIX):
        temp_strike = 1

        for index, _ in enumerate(row):
            if index != 0 and row[index] == row[index-1]:
                temp_strike += 1
            else:
                if temp_strike > current_strike:
                    current_strike = temp_strike
                    largest_row = i
                temp_strike = 1

        if temp_strike > current_strike:
            current_strike = temp_strike
            largest_row = i


    return largest_row



if __name__ == '__main__':
    main()
