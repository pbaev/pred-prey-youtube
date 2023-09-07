import numpy
import typing as t

BgraArray = numpy.array
Colour = t.Tuple # (green, blue, red) 0-255 scale
Position = t.Tuple # (y, x)
TypeId = str

# Folder where the images will be created
IMAGE_FOLDER = 'imgs'

# Number of iterations to display in the plot
PLOT_ITERATIONS = 100

# Is the simulation predatore/prey instead of 3 way?
# If true, parameters prefixed by PRED_ and PREY_ will be used
# otherwise, those prefixed by GENERAL_ will be used.
IS_PRED_PREY = True

# Enables the limiting of reproduction based on population size
ENABLE_REPRODUCTION_CHANCE = True
# If the above is true, how much should they be limited?
# See Sim.should_reproduce_chance() for more details
PRED_REPRODUCTION_MULTIPLIER = 10
PREY_REPRODUCTION_MULTIPLIER = 3
GENERAL_REPRODUCTION_MULTIPLIER = 3.5

# Each iteration the square with the highest count of each being type is chosen.
# If true, that square will have beings removed if they exceed the square's population's threshold.
# See Sim.type_overpopulation_cull() for more details.
ENABLE_CULL = True
PRED_DEATH_CHANCE_MULTIPLIER = 2
PREY_DEATH_CHANCE_MULTIPLIER = 2
GENERAL_DEATH_CHANCE_MULTIPLIER = 0.33

# Number of iterations that beings can live for
PRED_MAX_AGE = 6
PREY_MAX_AGE = 10
GENERAL_MAX_AGE = 20

# Chance that prey give birth
PREY_BIRTH_CHANCE = 0.50

# In 3 way models, what chance should predators have of birthing 2 beings instead of 1.
# This is needed so the populaitons don't dwindle.
GENERAL_SECOND_BIRTH_CHANCE = 0.18

# If a predator attempts to eat the last prey on a square, this is the chance that it will be eaten
LAST_SPECIES_DEATH_CHANCE = 0.10

# Chance that a being will make a random move instead of the "optimal" one
RANDOM_MOVE_CHANCE = 0.10

# If false, beings will be born in the sam square as their parent.
# If true, they will be born in a random square.
RANDOM_BIRTH_LOCATION = True
