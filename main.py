import movement 
import river
import variables
import creatures
import table
import turn_mechanism
import widgets

def timer():    
    if len(variables.river_list) < variables.SIZE_VARIABLE*4: #5
        river.river_maker()

    turn_mechanism.simulation_turn()
    widgets.species_list_menu()
    table.existing_table.delete_circles()
    table.existing_table.update_vegetables()
    table.existing_table.draw_table()
    table.existing_table.update_circles(variables.creature_list)
    movement.movement_manager()
    variables.TURN_COUNT += 1
    widgets.update_info_labels()
    widgets.update_graph()  
    table.root.after(variables.TIMER_INTERVAL, timer)

table.existing_table.draw_table()
table.existing_table.generate_vegetables()
creatures.creating_creatures(variables.NUM_CREATURES)

widgets.update_graph()

timer()

table.root.mainloop()