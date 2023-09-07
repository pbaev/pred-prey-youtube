from structure import *
from visuals import *


# The predator and prey type are created
# Colour is green, blue, red on a 0-255 scale
predator = BeingType(name='Predator', colour=(56, 0, 224))
prey = BeingType(name='Prey', colour=(242, 10, 12))

# The relationship between the types is defined
predator.add_prey(prey)

# Creates a circle map with a height and width of 25.
store = Store(
    types=set([predator, prey]), 
    map_array=Store.get_map_array(shape=(20, 20), circle=True)
)

# Adds 600 predators and prey to the simulation
store.add_beings_random_position(predator, 600)
store.add_beings_random_position(prey, 600)

# Runs 50 iterations of the simulation and creates the map and plot images in the "imgs" folder.
sim = Sim(store)
sim_to_images(sim, count=50)


"""
# This is an example of how to setup a 3 way model.
# 0 eats 1, 1 eats 2, 2 eats 0.
# Before running, set IS_PRED_PREY in constants.py to false

being_0 = BeingType(name='Being 0', colour=(56, 0, 224))
being_1 = BeingType(name='Being 1', colour=(242, 10, 12))
being_2 = BeingType(name='Being 2', colour=(3, 209, 255))
being_0.add_prey(being_1)
being_1.add_prey(being_2)
being_2.add_prey(being_0)

store = Store((25,25), set([being_0, being_1, being_2]))
store.add_beings_random_position(being_0, 600)
store.add_beings_random_position(being_1, 600)
store.add_beings_random_position(being_2, 600)
"""
