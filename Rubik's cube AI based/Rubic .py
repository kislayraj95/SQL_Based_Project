from enum import Enum

import numpy as np
import tensorflow as tf


# colors
class Rubic(Enum):
    ORANGE = 1  # Left
    GREEN = 2  # Front
    RED = 3  # Right
    BLUE = 4  # Back
    WHITE = 5  # Up
    YELLOW = 6  # Down


def initialise_new_rubic():
    # create a rubic
    return [np.full((3, 3), e.value) for e in Rubic]


def number_to_char(x):
    return Rubic(x).name[0]


def numpy_to_string(arr):
    return '|' + ' '.join(list(map(number_to_char, arr))) + '|'


def print_rubic(rubic):
    # 0 - 3 = left to back
    # 4, 5 = up, down
    # print tab
    # print value
    for i in range(3):
        print(' ' * 8, end='')
        print(numpy_to_string(rubic[4][i]))
    # print tab
    # print value
    for i in range(3):
        for j in range(4):
            print(numpy_to_string(rubic[j][i]), end=' ')
        print()
    for i in range(3):
        print(' ' * 8, end='')
        print(numpy_to_string(rubic[5][i]))


if __name__ == '__main__':
    rubic = initialise_new_rubic()
    # loop and get things done
    while True:
        print('REPLACE ME WITH THE MENU')
        _rubic = np.copy(rubic)
        try:
            num = int(input('Enter number[1-10]: '))
            if not (num >= 1 and num <= 10):
                raise Exception()
        except:
            print('invalid number')
            continue
        if num == 1:
            print('rotating the right side forward')
            rubic[1][:, 2], rubic[4][:, 2], rubic[5][:, 2], rubic[3][:, 0] = \
                _rubic[5][:, 2], _rubic[1][:, 2], np.flip(
                    _rubic[3][:, 0], 0), np.flip(_rubic[4][:, 2], 0)
            rubic[2] = np.rot90(rubic[2], 3)
        elif num == 2:
            print('rotating the right side backward')
            rubic[1][:, 2], rubic[5][:, 2], rubic[4][:, 2], rubic[3][:, 0] = \
                _rubic[4][:, 2], _rubic[1][:, 2], np.flip(
                    _rubic[3][:, 0], 0), np.flip(_rubic[5][:, 2], 0)
            rubic[2] = np.rot90(rubic[2], 1)
        if num == 3:
            print('rotating the left side forward')
            rubic[1][:, 0], rubic[4][:, 0], rubic[5][:, 0], rubic[3][:, 2] = \
                _rubic[5][:, 0], _rubic[1][:, 0], np.flip(
                    _rubic[3][:, 2], 0), np.flip(_rubic[4][:, 0], 0)
            rubic[0] = np.rot90(rubic[0], 1)
        elif num == 4:
            print('rotating the left side backward')
            rubic[1][:, 0], rubic[5][:, 0], rubic[4][:, 0], rubic[3][:, 2] = \
                _rubic[4][:, 0], _rubic[1][:, 0], np.flip(
                    _rubic[3][:, 2], 0), np.flip(_rubic[5][:, 0], 0)
            rubic[0] = np.rot90(rubic[0], 3)
        elif num == 5:
            print('rotating the top side counterclockwise')
            rubic[0][0], rubic[1][0], rubic[2][0], rubic[3][0] = _rubic[3][0], _rubic[0][0], _rubic[1][0], _rubic[2][0]
            rubic[4] = np.rot90(rubic[4], 1)
        elif num == 6:
            print('rotating the top side clockwise')
            rubic[0][0], rubic[1][0], rubic[2][0], rubic[3][0] = _rubic[1][0], _rubic[2][0], _rubic[3][0], _rubic[0][0]
            rubic[4] = np.rot90(rubic[4], 3)
        elif num == 7:
            print('rotating the bottom side clockwise')
            rubic[0][2], rubic[1][2], rubic[2][2], rubic[3][2] = _rubic[1][2], _rubic[2][2], _rubic[3][2], _rubic[0][2]
            rubic[5] = np.rot90(rubic[5], 1)
        elif num == 8:
            print('rotating the bottom side counterclockwise')
            rubic[0][2], rubic[1][2], rubic[2][2], rubic[3][2] = _rubic[3][2], _rubic[0][2], _rubic[1][2], _rubic[2][2]
            rubic[5] = np.rot90(rubic[5], 3)
        elif num == 9:
            print_rubic(rubic)
        elif num == 10:
            print('Thanks')
            break
