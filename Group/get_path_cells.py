import numpy as np

def get_positions(coordinate1,coordinate2):
    x_diff = coordinate2[0] - coordinate1[0]
    y_diff = coordinate2[1] - coordinate1[1]
    #lst_y = [coordinate1[0] + np.sign(x_diff) * i * (x_diff/y_diff) for i in range(1,abs(x_diff)+1)]
    lst_x = [coordinate1[0] + np.sign(x_diff)* i for i in range(abs(x_diff)+1)]
    lst_y = [coordinate1[1] + np.sign(y_diff) * i for i in range(abs(x_diff)+1)]


    return lst_y



cells = get_positions((5,4),(1,3))
print(cells)