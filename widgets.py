import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import variables
import table

creature_list = variables.creature_list
root = table.root


def increase_timer():
    variables.TIMER_INTERVAL += 100
    update_timer_label()

def pause_timer():
    variables.TIMER_INTERVAL += 100000
    update_timer_label()

def continue_timer():
    variables.TIMER_INTERVAL = 1000
    update_timer_label()

def decrease_timer():
    variables.TIMER_INTERVAL = max(100, variables.TIMER_INTERVAL - 100)
    update_timer_label()

def update_timer_label():
    timer_label.config(text=f"FPS: {1000/variables.TIMER_INTERVAL:.1f}")

def species_list_menu():
    variables.species_list = []
    for creature in creature_list:
        if creature.species_ID not in variables.species_list:
            variables.species_list.append(creature.species_ID)  

    açılır_liste['menu'].delete(0, 'end')  # Clear existing menu options

    for tür in variables.species_list:
        açılır_liste['menu'].add_command(label=tür, command=lambda value=tür: species_indicator(value))

def species_indicator(selected_value):
    variables.sellected_species_coordinates = []

    individual_count = 0
    sum_size = 0
    sum_fertility = 0
    sum_sense = 0
    sum_speed = 0
    sum_weigth_0 = 0
    sum_weigth_1 = 0
    sum_weigth_2 = 0

    w0 = ""
    w1 = ""
    w2 = ""

    for creature in creature_list:
        creature.is_sellected = False

        if selected_value == creature.species_ID:
            variables.sellected_species_coordinates.append((creature.x, creature.y))
            creature.is_sellected = True

            individual_count += 1
            sum_size += creature.size 
            sum_fertility += creature.fertility
            sum_sense += creature.sense
            sum_speed += creature.speed
            sum_weigth_0 += creature.weigth_0
            sum_weigth_1 += creature.weigth_1
            sum_weigth_2 += creature.weigth_2

    avr_size = sum_size / individual_count
    avr_fertility = sum_fertility / individual_count
    avr_sense = sum_sense / individual_count
    avr_speed = sum_speed / individual_count
    avr_w_0 = sum_weigth_0 / individual_count
    avr_w_1 = sum_weigth_1 / individual_count
    avr_w_2 = sum_weigth_2 / individual_count

    if 0.33 > avr_w_0:
        w0 = "çekingen"
    if 0.33 < avr_w_0 < 0.66:
        w0 = "ılımlı"
    if 0.66 < avr_w_0:
        w0 = "istekli"
    if 0.33 > avr_w_1:
        w1 = "çekingen"
    if 0.33 < avr_w_1 < 0.66:
        w1 = "ılımlı"
    if 0.66 < avr_w_1:
        w1 = "istekli"
    if 0.33 > avr_w_2:
        w2 = "çekingen"
    if 0.33 < avr_w_2 < 0.66:
        w2 = "ılımlı"
    if 0.66 < avr_w_2:
        w2 = "istekli"

    species_inf_label.config(text=f'''Bu türün ortalama büyüklüğü: {avr_size:.2f},
                                 \n ortalama doğurganlığı: {avr_fertility:.2f},
                                 \n ortalama görüşü: {avr_sense:.2f},
                                 \n ortalama hızı: {avr_speed:.2f} kadardır.
                                 \n Türe ait olan canlı sayısı: {individual_count} kadardır.
                                 \n etçilliğe karşı olan tavırları: {w0}, 
                                 \n çifteşmeye karşı olan tavırları: {w1},
                                 \n otçulluğa karşı olan tavırları: {w2} durumdadır.
                                 ''')

def update_info_labels():
    global average_size, average_speed, average_sense, average_fertility_rate
    alive_count = sum(individual.is_alive for individual in creature_list)
    alive_label.config(text=f"Mevcut Canlı Sayısı: {alive_count}")

    average_size = sum(individual.size for individual in creature_list) / len(creature_list)
    size_label.config(text=f"Ortalama Büyüklük: {average_size:.2f}")

    average_speed = sum(individual.speed for individual in creature_list) / len(creature_list)
    speed_label.config(text=f"Ortalama Hız: {average_speed:.2f}")

    average_sense = sum(individual.sense for individual in creature_list) / len(creature_list)
    sense_label.config(text=f"Ortalama Algı: {average_sense:.2f}")

    average_health = sum(individual.health for individual in creature_list) / len(creature_list)
    health_label.config(text=f"Ortalama Sağlık: {average_health:.2f}")

    average_fertility_rate = sum(individual.fertility for individual in creature_list) / len(creature_list)
    fertility_label.config(text=f"Ortalama Doğurganlık: {average_fertility_rate:.2f}")

    average_fertility_tiredness = sum(individual.fertility_tiredness for individual in creature_list) / len(creature_list)
    tiredness_label.config(text=f"Ortalama Doğum Yorgunluğu: {average_fertility_tiredness:.2f}")

    turn_label.config(text=f"Tur sayısı: {variables.TURN_COUNT}")
    born_label.config(text=f"Doğan birey sayısı: {variables.BORN_CREATURES}")
    died_naturally_label.config(text=f"Eceliyle ölen birey sayısı: {variables.DIED_NATURALLY}")

info_frame = tk.Frame(root)
info_frame.grid(column=2, row=0)

alive_label = tk.Label(info_frame, text="Mevcut Canlı Sayısı: 0")

size_label = tk.Label(info_frame, text="Ortalama Büyüklük: 0.00")
speed_label = tk.Label(info_frame, text="Ortalama Hız: 0.00")
sense_label = tk.Label(info_frame, text="Ortalama Algı: 0.00")
fertility_label = tk.Label(info_frame, text="Ortalama Doğurganlık Oranı: 0.00")

health_label = tk.Label(info_frame, text="Ortalama Sağlık: 0.00")
tiredness_label = tk.Label(info_frame, text="Ortalama Doğum Yorgunluğu: 0.00")
turn_label = tk.Label(info_frame, text="Tur sayısı: 0")
born_label = tk.Label(info_frame, text="Doğan birey sayısı: 0")
died_naturally_label = tk.Label(info_frame, text="Eceliyle ölen birey sayısı: 0")

timer_increase_button = tk.Button(info_frame, text="Timer +", command=increase_timer)
timer_decrease_button = tk.Button(info_frame, text="Timer -", command=decrease_timer)
timer_pause_button = tk.Button(info_frame, text="Pause Timer", command=pause_timer)
timer_continue_button = tk.Button(info_frame, text="Continue Timer", command=continue_timer)
timer_label = tk.Label(info_frame, text=f"FPS: {1000/variables.TIMER_INTERVAL:.1f}")

species_inf_label = tk.Label(info_frame, text="Seçtiğiniz türe ait bilgiler burada bulunur")

size_label.grid(row=0, column=1)
speed_label.grid(row=1, column=1)
sense_label.grid(row=2, column=1)
fertility_label.grid(row=3, column=1)

health_label.grid(row=5, column=1)
tiredness_label.grid(row=6, column=1)

turn_label.grid(row=8, column=1)
alive_label.grid(row=9, column=1)
born_label.grid(row=10, column=1)
died_naturally_label.grid(row=11, column=1)

timer_increase_button.grid(row=13, column=1)
timer_decrease_button.grid(row=14, column=1)
timer_pause_button.grid(row=15, column=1)
timer_continue_button.grid(row=16, column=1)
timer_label.grid(row=17, column=1)

açılır_liste_var = tk.StringVar(root)
açılır_liste = tk.OptionMenu(root, açılır_liste_var, "")
açılır_liste.grid(row=18, column=1)

species_inf_label.grid(row=19, column=1)

# Matplotlib için bir figür oluştur
fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(6, 9))

# Canvas için bir Matplotlib figürü oluştur
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=1, rowspan=10, padx=10, pady=10, sticky="nsew")

avarage_size_list = []
avarage_speed_list = []
avarage_sense_list = []
average_fertility_rates = []
average_fertility_tiredness_list = []
average_health_list = []
alive_counts = []

def update_graph():
    #BORN_CREATURES_list = [list(range(variables.BORN_CREATURES))]
    #DIED_NATURALLY_list = [list(range(variables.DIED_NATURALLY))]

    alive_counts.append(sum(individual.is_alive for individual in creature_list))
    avarage_size_list.append(sum(individual.size for individual in creature_list) / len(creature_list))
    avarage_speed_list.append(sum(individual.speed for individual in creature_list) / len(creature_list))
    avarage_sense_list.append(sum(individual.sense for individual in creature_list) / len(creature_list))
    average_health_list.append(sum(individual.health for individual in creature_list) / len(creature_list))
    average_fertility_rates.append(sum(individual.fertility for individual in creature_list) / len(creature_list))
    average_fertility_tiredness_list.append(sum(individual.fertility_tiredness for individual in creature_list) / len(creature_list))

    x_values = list(range(variables.TURN_COUNT))
    axes[0].clear()
    axes[0].plot(x_values, avarage_size_list, label='Ortalama Büyüklük')
    axes[0].set(xlabel='Tur Sayısı')
    axes[0].legend()

    axes[1].clear()
    axes[1].plot(x_values, avarage_speed_list, label='Ortalama Hız')
    axes[1].set(xlabel='Tur Sayısı')
    axes[1].legend()
        
    axes[2].clear()
    axes[2].plot(x_values, avarage_sense_list, label='Ortalama Görüş')
    axes[2].set(xlabel='Tur Sayısı')
    axes[2].legend()

    axes[3].clear()
    axes[3].plot(x_values, average_fertility_rates, label='Ortalama Doğurganlık')
    axes[3].set(xlabel='Tur Sayısı')
    axes[3].legend()

    axes[4].clear()
    #axes[4].plot(x_values, DIED_NATURALLY_list, label='Eceliyle Ölen Sayısı')
    #axes[4].plot(x_values, BORN_CREATURES_list, label='Doğan Canlı Sayısı')
    axes[4].plot(x_values, alive_counts, label='Canlı Sayısı')
    axes[4].set(xlabel='Tur Sayısı')
    axes[4].legend()
    
    canvas.draw()