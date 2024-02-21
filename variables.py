SIZE_VARIABLE = 64 #64 or #128
NUM_CREATURES = SIZE_VARIABLE * 4 #4
DIFFICULTY_OF_ENVIRONMENT = 0.075 #0.1
EATING_REWARD = 75
YEME_KOSULU = 1.25
MUTATION_RATE = 20 #20
VEGETABLE_FREQUENCY = 0.001 #0.001
VEGETABLE_REWARD = 50 #50
FERTILITY_SATURATION = 15
FULL_HEALTH = 150

MAX_SPEED = 3
MIN_SPEED = 1

MAX_SENSE = 5
MIN_SENSE = 1

MAX_SIZE = 5
MIN_SIZE = 1

MAX_FERTILITY = 3
MIN_FERTILITY = 1

#---------------Unconstant variables-------------------
harita_tutumu = {(1, 1): (0, 0)}
species_list = [0]
sellected_species_coordinates = []
river_list = [(0,0)]
creature_list = []

TURN_COUNT = 1
BORN_CREATURES = 0
DIED_NATURALLY = 0
TIMER_INTERVAL = 1000