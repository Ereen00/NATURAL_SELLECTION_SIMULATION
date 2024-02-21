import random
import variables

start_point = (0,0)
start_point_2 = None
start_point_3 = None

def create_branch(continue_point, kayırma_değişkeni):
    while True:
        water_x, water_y = continue_point
        new_water_x, new_water_y = water_x, water_y
        random_count = random.random()

        if (water_x + 1, water_y) in variables.river_list and (water_x - 1, water_y) in variables.river_list and (water_x, water_y + 1) in variables.river_list and (water_x, water_y - 1) in variables.river_list:
            break 

        if 0.25 + kayırma_değişkeni >= random_count >= 0:
            new_water_x += 1
        elif 0.50 >= random_count > 0.25 + kayırma_değişkeni:
            new_water_y -= 1
        elif 0.75 - kayırma_değişkeni >= random_count > 0.50:
            new_water_x -= 1
        elif 1 >= random_count > 0.75 - kayırma_değişkeni:
            new_water_y += 1

        # Eğer belirtilen koordinatta bir sebze ya da su yoksa
        if not (new_water_x, new_water_y) in variables.river_list:
            if variables.SIZE_VARIABLE > new_water_x >= 0 and variables.SIZE_VARIABLE > new_water_y >= 0:
                break

    continue_point = (new_water_x, new_water_y)
    variables.river_list.append((new_water_x, new_water_y))

    return continue_point

def river_maker():
    global start_point, start_point_2, start_point_3

    continue_point = create_branch(start_point, 0.15)
    start_point = continue_point

    if len(variables.river_list) == variables.SIZE_VARIABLE:
        x, y = continue_point
        start_point_2 = (x, y)

    continue_point_2 = None
    
    if len(variables.river_list) >= variables.SIZE_VARIABLE:
        if start_point_2 is None:
            start_point_2 = (0, 0)  # Varsayılan bir değer atanıyor
        continue_point_2 = create_branch(start_point_2, 0.10)
        start_point_2 = continue_point_2

    if continue_point_2:
        if len(variables.river_list) == 2*variables.SIZE_VARIABLE + 1:
            x, y = continue_point_2
            start_point_3 = (x, y)

    if len(variables.river_list) >= 2*variables.SIZE_VARIABLE:
        if start_point_3 is None:
            start_point_3 = (0, 0)
        continue_point_3 = create_branch(start_point_3, 0.05)
        start_point_3 = continue_point_3