import random
from utils import sigmoid, tanh, calculate_distance
import creatures 
import variables
import table

def size_fertility_sorgula(x, y):
    if (x, y) in variables.harita_tutumu:
        size, fertility_tiredness = variables.harita_tutumu[(x, y)]
        return size, fertility_tiredness
    else:
        return 0, 0

def detecton_colloision(c1):
    for c2 in variables.creature_list:
        if c1 is not c2 and (c1.x, c1.y) == (c2.x, c2.y):
            if c1.size > variables.YEME_KOSULU * c2.size:
                c2.is_alive = False
                c1.health += c2.size * variables.EATING_REWARD

            elif c2.size > variables.YEME_KOSULU * c1.size:
                c1.is_alive = False
                c2.health += c1.size * variables.EATING_REWARD
                
            else:
                if c1.fertility_tiredness == variables.FERTILITY_SATURATION and c2.fertility_tiredness == variables.FERTILITY_SATURATION:
                    count_new_baby = 0
                    while round(c1.fertility * c2.fertility) > count_new_baby:     
                        c1.fertility_tiredness = 0
                        c2.fertility_tiredness = 0

                        new_x = c1.x + random.randint(-1, 1)
                        new_y = c1.y + random.randint(-1, 1)

                        new_healt = (c1.health + c2.health)/2

                        # Crossover
                        new_speed = random.uniform(c1.speed, c2.speed)
                        new_size = random.uniform(c1.size, c2.size)
                        new_sense = random.uniform(c1.sense, c2.sense)
                        new_fertility = random.uniform(c1.fertility, c2.fertility)

                        new_weigth_0 = random.uniform(c1.weigth_0, c2.weigth_0)
                        new_weigth_1 = random.uniform(c1.weigth_1, c2.weigth_1)
                        new_weigth_2 = random.uniform(c1.weigth_2, c2.weigth_2)

                        # species_ID belirleme
                        if not c1.species_ID == c2.species_ID:
                            new_species_ID = "({}*{})".format(str(c1.species_ID), str(c2.species_ID))
                        else:
                            new_species_ID = c1.species_ID 

                        # Mutation
                        Possibility_for_mutation = random.randint(0,variables.MUTATION_RATE*7)
                        if Possibility_for_mutation == 0:
                            new_size = random.uniform(variables.MIN_SIZE, variables.MAX_SIZE)
                            new_species_ID += str("Msize")
                        elif Possibility_for_mutation == 1:
                            new_sense = random.uniform(variables.MIN_SENSE, variables.MAX_SENSE)
                            new_species_ID += str("Msense")
                        elif Possibility_for_mutation == 2:
                            new_fertility = random.uniform(variables.MIN_FERTILITY, variables.MAX_FERTILITY)
                            new_species_ID += str("Mfert")
                        elif Possibility_for_mutation == 3:    
                            new_speed = random.uniform(variables.MIN_SPEED, variables.MAX_SPEED)
                            new_species_ID += str("Mspeed")
                        elif Possibility_for_mutation == 4:    
                            new_weigth_0 = random.uniform(-1,1)
                            new_species_ID += str("Mweigth0")    
                        elif Possibility_for_mutation == 5:    
                            new_weigth_1 = random.uniform(0,1)
                            new_species_ID += str("Mweigth1")
                        elif Possibility_for_mutation == 6:    
                            new_weigth_2 = random.uniform(0,1)
                            new_species_ID += str("Mweigth2")

                        # Canlı renkleri sahip olduğu özelliklere göre oluşturulur
                        new_red = round(new_speed * (255 / variables.MAX_SPEED))
                        new_green = round(new_fertility * (255 / variables.MAX_FERTILITY))
                        new_blue = round(new_sense * (255 / variables.MAX_SENSE))
                        new_color = f"#{new_red:02x}{new_green:02x}{new_blue:02x}"

                        new_x = c1.x
                        new_y = c1.y

                        variables.harita_tutumu[(new_x, new_y)] = (new_size, -5)

                        variables.creature_list.append(creatures.CreatureInfo(True, new_healt, new_size, new_color, new_sense, new_speed, new_fertility, -5, new_x, new_y, new_weigth_0, new_weigth_1, new_weigth_2, new_species_ID, False))
                        variables.BORN_CREATURES += 1
                        count_new_baby += 1

def calculate_pre_outcomes(perception, individual):
    outcomes = 0
    # problemli: verilen perception tile içeriklerini düzgün bir şekilde sayı değerine dönüştüremiyor (ayrıca var olduğunu düşündüğü yerlerde vegetable yok!)
    for x1, y1 in perception:
        if not (x1, y1) in variables.river_list:
            if 0 <= x1 < variables.SIZE_VARIABLE and 0 <= y1 < variables.SIZE_VARIABLE:
                distance = calculate_distance(x1, y1, individual.x, individual.y)
                size, fertility = size_fertility_sorgula(x1,y1)

                # biri var mı
                if size > 0:
                    # tespit ettiği canlı onu yiyebiliyor mu ya da o diğerini yiyebiliyor mu
                    if 1/variables.YEME_KOSULU > size/individual.size or size/individual.size > variables.YEME_KOSULU:
                        # -45/10 ve 28/10 arasında bir sayı döndürür
                        outcomes += tanh((variables.YEME_KOSULU - (size / individual.size)) * (1/distance) * (variables.FULL_HEALTH/individual.health)) * individual.weigth_0 
                
                    # çiftleşmeye istekli herhangi bir canlı var mı
                    elif fertility > 0:
                        # 0 ve 1 arasında bir sayı döndürür
                        outcomes += sigmoid(((2 * variables.FERTILITY_SATURATION) - (individual.fertility_tiredness + fertility)) * (1/distance) / (2 * variables.FERTILITY_SATURATION)) * individual.weigth_1

                # her hangi bir vegetable var mı
                elif table.existing_table.cell_states[y1][x1]:
                    outcomes +=  sigmoid((1/distance) * (variables.FULL_HEALTH/individual.health * 10)) * individual.weigth_2

    return outcomes

def update_location(final_outcomes, reducer, individual, Total_outcomes):
    sorted_outcomes = sorted(final_outcomes.items(), key=lambda x: x[1], reverse=True)
    variables.harita_tutumu[(individual.x, individual.y)] = (0, 0)

    new_location_x = individual.x
    new_location_y = individual.y

    # canlı çok karasız kaldıysa rastgele hareket ettir
    if final_outcomes[1] == final_outcomes[2] == final_outcomes[3] == final_outcomes[4]:
        if 0.5 > random.random():
            new_location_x += random.choice([-1,1])
        else:
            new_location_y += random.choice([-1,1]) 
        
    else:
        max_direction, max_value = sorted_outcomes[0]
        if max_direction == 1:  # Güney
            new_location_y += 1
        elif max_direction == 2:  # Kuzey
            new_location_y -= 1
        elif max_direction == 3:  # Batı
            new_location_x -= 1
        elif max_direction == 4:  # Doğu
            new_location_x += 1

        final_outcomes[max_direction] -= reducer

    # suya girmelerini engelle
    if (new_location_x, new_location_y) in variables.river_list:
        new_location_x = individual.x
        new_location_y = individual.y
            
    # canlıların sınırdan çıkışını engelle
    new_location_x = max(0, min(new_location_x, variables.SIZE_VARIABLE - 1))
    new_location_y = max(0, min(new_location_y, variables.SIZE_VARIABLE - 1))

    # Canlı sebze alan üzerinde ise
    if table.existing_table.cell_states[new_location_y][new_location_x]:
        individual.health += variables.VEGETABLE_REWARD
        table.existing_table.cell_states[new_location_y][new_location_x] = False

    individual.x, individual.y = new_location_x, new_location_y
    variables.harita_tutumu[(individual.x, individual.y)] = (individual.size, individual.fertility_tiredness)

    detecton_colloision(individual)

def movement_manager():
    for individual in variables.creature_list:    

        North_perception = []
        South_perception = []
        East_perception = []
        West_perception = []

        NWest_perception = []
        SEast_perception = []  
        NEast_perception = []
        SWest_perception = []

        # Çevresini algılamak için kullanacağı nöral ağı oluştur
        if round(individual.sense) >= 1: 
            North_perception.append([individual.x, individual.y + 1])
            South_perception.append([individual.x, individual.y - 1])  
            East_perception.append([individual.x + 1, individual.y])
            West_perception.append([individual.x - 1, individual.y])
            
        if round(individual.sense) >= 2:
            NWest_perception.append([individual.x - 1, individual.y + 1])
            SWest_perception.append([individual.x - 1, individual.y - 1])             
            NEast_perception.append([individual.x + 1, individual.y + 1])
            SEast_perception.append([individual.x + 1, individual.y - 1])

        if round(individual.sense) >= 3:
            North_perception.append([individual.x, individual.y + 2])
            South_perception.append([individual.x, individual.y - 2])             
            East_perception.append([individual.x + 2, individual.y])
            West_perception.append([individual.x - 2, individual.y])
        
        if round(individual.sense) >= 4:
            NWest_perception.append([individual.x - 2, individual.y + 1])
            NWest_perception.append([individual.x - 1, individual.y + 2])

            SWest_perception.append([individual.x - 2, individual.y - 1])
            SWest_perception.append([individual.x - 1, individual.y - 2])  
                         
            NEast_perception.append([individual.x + 1, individual.y + 2])
            NEast_perception.append([individual.x + 2, individual.y + 1])
            
            SEast_perception.append([individual.x + 1, individual.y - 2])
            SEast_perception.append([individual.x + 2, individual.y - 1])

        if round(individual.sense) == 5:
            North_perception.append([individual.x, individual.y + 3])
            South_perception.append([individual.x, individual.y - 3])             
            East_perception.append([individual.x + 3, individual.y])
            West_perception.append([individual.x - 3, individual.y])

            NWest_perception.append([individual.x - 2, individual.y + 2])
            SWest_perception.append([individual.x - 2, individual.y - 2])             
            NEast_perception.append([individual.x + 2, individual.y + 2])
            SEast_perception.append([individual.x + 2, individual.y - 2])
        
        NWpre_outcomes = calculate_pre_outcomes(NWest_perception, individual)
        NEpre_outcomes = calculate_pre_outcomes(NEast_perception, individual)
        SWpre_outcomes = calculate_pre_outcomes(SWest_perception, individual)
        SEpre_outcomes = calculate_pre_outcomes(SEast_perception, individual)

        Npre_outcomes = calculate_pre_outcomes(North_perception, individual) + NWpre_outcomes/2 + NEpre_outcomes/2
        Spre_outcomes = calculate_pre_outcomes(South_perception, individual) + SEpre_outcomes/2 + SWpre_outcomes/2
        Wpre_outcomes = calculate_pre_outcomes(West_perception, individual) + NWpre_outcomes/2 + SWpre_outcomes/2
        Epre_outcomes = calculate_pre_outcomes(East_perception, individual) + NEpre_outcomes/2 + SEpre_outcomes/2

        final_outcomes = {1: Npre_outcomes, 2: Spre_outcomes, 3: Wpre_outcomes, 4: Epre_outcomes}

        # how badly does he wanna go or run from these tiles
        Total_outcomes = abs(Npre_outcomes) + abs(Spre_outcomes) + abs(Wpre_outcomes) + abs(Epre_outcomes)

        reducer = Total_outcomes/individual.speed

        for _ in range(round(individual.speed)):
            update_location(final_outcomes, reducer, individual, Total_outcomes)