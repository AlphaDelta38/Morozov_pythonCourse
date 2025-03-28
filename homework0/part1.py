# Variant 3


MATRIX = [
    [4, 1, 0, 0, 0],
    [1, 1, 1, 1, 2],
    [1, 1, 1, 0, 0],
    [0, 1, 3, 8, 1],
]



def main():
    amount_of_zero_in_colum = get_amount_colum_with_zero()
    row_index = get_row_largest_number_strike()

    print(f'Amount of colum with zero: {amount_of_zero_in_colum}')
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

    def change_strike(strike, row_i):
        nonlocal largest_row, current_strike, temp_strike
        if strike > current_strike:
            current_strike = strike
            largest_row = row_i
        temp_strike = 1

    for i, row in enumerate(MATRIX):
        temp_strike = 1

        for index in range(1, len(row)):
            temp_strike += 1
            access_flag = row[index] != row[index - 1] or index == len(row) - 1
            if access_flag:
                change_strike(temp_strike, i)

    return largest_row


if __name__ == '__main__':
    main()
