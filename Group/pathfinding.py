import numpy as np

def get_positions(coordinate1,coordinate2):
    '''
    :param coordinate1: tuple of current position
    :param coordinate2: tuple of destination position
    :return: list of cells in chron. order an Agent visits in its travel
            (including destination position, excluding current position)
            (diagonal travel is possible)
    '''

    
    x_diff = coordinate2[0] - coordinate1[0]
    y_diff = coordinate2[1] - coordinate1[1]

    #lst_y = [coordinate1[0] + np.sign(x_diff) * i * (x_diff/y_diff) for i in range(1,abs(x_diff)+1)]
    lst_x = [coordinate1[0] + np.sign(x_diff)* i for i in range(0,abs(x_diff)+1)]
    if x_diff != 0:
        lst_y = [round(coordinate1[1] +  np.sign(y_diff)* (abs(y_diff)/abs(x_diff)) * i) for i in range(0,abs(x_diff)+1)]
    else:
        lst_y = [coordinate1[1]+ np.sign(y_diff)*i for i in range(0,abs(x_diff)+1)]

    cells = [(x,y) for x,y in zip(lst_x,lst_y)][1:]

    return cells

def find_closest_cell(all_cell, pos):
    '''
    Given a list of all cells and a current positon it wil find the cell that is closest to it's current position

    :param all_cell: list of tuples 
    :param pos: tuple of current position
    :return: tuple out of all_cell which is the closest to pos
    '''


    closest = None
    distance = 1000000
    if pos == None:
        return None

    else:
        for cell in all_cell:
            xDif = abs(cell[0] - pos[0])
            yDif = abs(cell[1] - pos[1])
            if (xDif + yDif) < distance:
                distance = (xDif + yDif)
                closest = cell
        return closest