def find(all_cell, pos):
    closest = None
    distance = 1000000
    if pos != None:
        for cell in all_cell:
            xDif = abs(cell[0] - pos[0])
            yDif = abs(cell[1] - pos[1])
            if (xDif + yDif) > distance:
                distance = (xDif + yDif)
                closest = cell
        return closest
    else:
        return None
