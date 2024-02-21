import variables

def simulation_turn():
    for individual in variables.creature_list:
        individual.health -= individual.energy_consumption() * variables.DIFFICULTY_OF_ENVIRONMENT

        if (individual.x, individual.y) in variables.river_list:
            individual.is_alive = False

        if individual.health <= 0:
            individual.is_alive = False
            variables.DIED_NATURALLY += 1
        elif individual.health > variables.FULL_HEALTH:
            individual.health = variables.FULL_HEALTH

        if not individual.is_alive:
            variables.harita_tutumu[(individual.x, individual.y)] = (0, 0)
            variables.creature_list.remove(individual)

        if individual.fertility_tiredness > variables.FERTILITY_SATURATION:
            individual.fertility_tiredness = variables.FERTILITY_SATURATION
        else:
            individual.fertility_tiredness += (individual.fertility * individual.health)/(variables.FULL_HEALTH*4)