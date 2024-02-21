import random
import tkinter as tk

import variables

class Table:
    def __init__(self, canvas, size_variable, cell_size):
        self.canvas = canvas
        self.size_variable = size_variable
        self.cell_size = cell_size
        self.cell_states = [[False for _ in range(size_variable)] for _ in range(size_variable)]

    def draw_table(self):
        for row in range(self.size_variable):
            for col in range(self.size_variable):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "white" if not self.cell_states[row][col] else "lightgray"
                
                if (col, row) in variables.river_list:
                    color = "blue"

                for creature in variables.creature_list:
                    if creature.is_sellected:
                        if creature.x == col and creature.y == row:
                            color = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="lightgray", fill=color)

    def update_circles(self, creature_list):
        #Canlıların her birine atanan yeni konum bilgileriyle daireleri güncelle
        for creature in creature_list:
            center_x = creature.x * self.cell_size + self.cell_size // 2
            center_y = creature.y * self.cell_size + self.cell_size // 2
            radius = creature.size * self.cell_size // 8
            self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=creature.color)

    def delete_circles(self):
        self.canvas.delete("all")

    def update_vegetables(self):
        for row in range(self.size_variable):
            for col in range(self.size_variable):
                if not self.cell_states[row][col]:
                    if random.random() < variables.VEGETABLE_FREQUENCY:
                        if 0.5 > random.random():
                            new_row = row + random.choice([-1, 1])
                            if 0 <= new_row < self.size_variable:
                                if not (col, new_row) in variables.river_list:
                                    row = new_row
                        else:
                            new_col = col + random.choice([-1, 1])
                            if 0 <= new_col < self.size_variable:
                                if not (new_col, row) in variables.river_list:
                                    col = new_col
                                        
                        if not self.cell_states[row][col]:
                            self.cell_states[row][col] = True
                    
    def generate_vegetables(self):
        for _ in range(int(self.size_variable * self.size_variable)):
            new_row = random.choice(range(self.size_variable))
            new_col = random.choice(range(self.size_variable))
            # Eğer belirtilen koordinatta bir sebze ya da su yoksa 
            if not (new_row,new_col) in variables.river_list:
                if not self.cell_states[new_row][new_col]:
                    self.cell_states[new_row][new_col] = True

root = tk.Tk()
root.title("Genetic Algorithm")

canvas_size = 950
cell_size = canvas_size / variables.SIZE_VARIABLE
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
canvas.grid(column=0)

root.geometry(f"{canvas_size*2}x{canvas_size}")

existing_table = Table(canvas, variables.SIZE_VARIABLE, cell_size)