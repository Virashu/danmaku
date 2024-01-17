def not_in_border(x, y, direction, width, height):
    if direction == "up" and y <= 0:
        return False
    elif direction == "down" and y >= height:
        return False
    elif direction == "left" and x <= 0:
        return False
    elif direction == "right" and x >= width:
        return False
    else:
        return True
