import random
import variables

class CreatureInfo:
    def __init__(self, is_alive, health, size, color, sense, speed, fertility, fertility_tiredness, x, y, weigth_0, weigth_1, weigth_2, species_ID, is_sellected):
        self.is_alive = is_alive
        self.health = health
        self.size = size
        self.color = color
        self.sense = sense
        self.speed = speed
        self.fertility = fertility
        self.fertility_tiredness = fertility_tiredness
        self.x = x
        self.y = y
        self.weigth_0 = weigth_0
        self.weigth_1 = weigth_1
        self.weigth_2 = weigth_2
        self.species_ID = species_ID
        self.is_sellected = is_sellected

    def energy_consumption(self):
        #Canlının enerji tüketimini hesaplayan formül
        return (self.speed) * (self.size**3) * self.fertility + self.sense 

def creating_creatures(num_creatures):
    species_ID = 1
    for _ in range(num_creatures):
        random_size = random.uniform(variables.MIN_SIZE, variables.MAX_SIZE)
        random_sense = random.uniform(variables.MIN_SENSE, variables.MAX_SENSE)
        random_fertility = random.uniform(variables.MIN_FERTILITY, variables.MAX_FERTILITY)
        random_speed = random.uniform(variables.MIN_SPEED, variables.MAX_SPEED)

        red = round(random_speed * (255 / variables.MAX_SPEED))
        green = round(random_fertility * (255 / variables.MAX_FERTILITY))
        blue = round(random_sense * (255 / variables.MAX_SENSE))
        new_color = f"#{red:02x}{green:02x}{blue:02x}"

        random_location_x = random.randint(2, variables.SIZE_VARIABLE - 2)
        random_location_y = random.randint(2, variables.SIZE_VARIABLE - 2)

        while any(((s.x, s.y) == (random_location_x, random_location_y)) for s in variables.creature_list):
            random_location_x = random.randint(2, variables.SIZE_VARIABLE - 2)
            random_location_y = random.randint(2, variables.SIZE_VARIABLE - 2)

        new_weigth_0 = random.uniform(-1,1)
        new_weigth_1 = random.uniform(0,1)
        new_weigth_2 = random.uniform(0,1) 

        variables.harita_tutumu[(random_location_x, random_location_y)] = (random_size, 10)
        variables.creature_list.append(CreatureInfo(True, 100, random_size, new_color, random_sense, random_speed, random_fertility, 10, random_location_x, random_location_y, new_weigth_0, new_weigth_1, new_weigth_2, str(species_ID), False))
        species_ID += 1