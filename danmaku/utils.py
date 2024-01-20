def not_in_border(x, y, vx, vy, width, height):
    if vy < 0 and y <= 0:
        return False
    elif vy > 0 and y >= height:
        return False
    elif vx > 0 and x <= 0:
        return False
    elif vx < 0 and x >= width:
        return False
    else:
        return True
