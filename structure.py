import math
import numpy
import random
import typing as t
from collections import defaultdict
from constants import *


class Store:
    # ex: {(3,6): {'pred': [Being], 'prey': [Being]}}
    map_array: numpy.array
    being_positions: t.Dict[Position, t.Dict['BeingType', t.List['Being']]] = dict() 
    possible_positions_set: t.Set[Position]
    possible_positions_list: t.List[Position]
    types: t.Set['BeingType']

    def __init__(self, types: t.Set['BeingType'], map_array: numpy.array):
        self.types = types
        self.map_array = map_array
        self.possible_positions_list = self._generate_possible_positions_list(map_array)
        self.possible_positions_set = set(self.possible_positions_list)
        self.being_positions = self._generate_being_positions(self.possible_positions_list)

    """
    Convenience method to get the map of possible positions a being can move to.
    In the returned array, cells with a value of 1 can be visited by beings, 
    cells with a value of 0 are inaccesible.
    
    shape is (height, width)
    if circle, then the map will be a circle of (height, width) otherwise it will be a rectangle
    """
    @classmethod
    def get_map_array(cls, shape: t.Tuple[int, int], circle: bool) -> numpy.array:
        return cls.create_circle_array(shape) if circle else numpy.ones(shape)
            
    """
    https://stackoverflow.com/questions/10031580/how-to-write-simple-geometric-shapes-into-numpy-arrays
    """
    @staticmethod
    def create_circle_array(shape: t.Tuple) -> numpy.array:
        xx, yy = numpy.mgrid[:shape[0], :shape[1]]
        circle = (xx - shape[0]/2) ** 2 + (yy - shape[1]/2) ** 2
        return circle < (shape[0]/2 * shape[1]/2)

    def _generate_possible_positions_list(self, array: numpy.array) -> t.Set[Position]:
        return [tuple(position) for position in numpy.argwhere(array == 1)]
    
    def _generate_being_positions(self, positions_list: t.List[Position]) -> \
        t.Dict[Position, t.Dict['BeingType', t.List['Being']]]:
        being_positions = {}
        for position in positions_list:
            being_positions[position] = defaultdict(set)
        return being_positions

    def add_being(self, being_type: 'BeingType', position: Position) -> None:
        being = being_type.create_being(position)
        self.being_positions[position][being_type].add(being)

    def add_beings_random_position(self, being_type: 'BeingType', count: int) -> None:
        for _ in range(count):
            position = random.choice(self.possible_positions_list)
            self.add_being(being_type, position)
        
    def remove_being(self, being: 'Being') -> None:
        self.being_positions[being.position][being.type_].remove(being)
    
    def get_all_beings_random_list(self) -> t.List['Being']:
        beings = []
        for position, beings_dict in self.being_positions.items():
            for type_, beings_list in beings_dict.items():
                beings += beings_list
        random.shuffle(beings)
        return beings

    def get_type_position_count(self) -> t.Dict[Position, int]:
        count = {position: defaultdict(lambda: 0) for position in self.possible_positions_list}
        for position, beings_dict in self.being_positions.items():
            for type_, beings_list in beings_dict.items():
                count[position][type_] += len(beings_list)
        return count
    
    def get_type_count(self) -> t.Dict:
        count = defaultdict(lambda: 0)
        for position, beings_dict in self.being_positions.items():
            for type_, beings_list in beings_dict.items():
                count[type_] += len(beings_list)
        return dict(count)

    def move_being(self, being: 'Being', new_position: Position) -> None:
        self.being_positions[being.position][being.type_].remove(being)
        self.being_positions[new_position][being.type_].add(being)
        being.position = new_position

    def get_valid_adjacent_positions(self, position: Position) -> t.List[Position]:
        position_deltas = [(0,0), (1,0), (0,1), (-1,0), (0,-1)]
        valid_positions = []
        for position_delta in position_deltas:
            new_position = (position[0] + position_delta[0], position[1] + position_delta[1])
            if self.is_valid_position(new_position):
                valid_positions.append(new_position)
        return valid_positions
    
    def is_valid_position(self, position: Position) -> bool:
        return position in self.possible_positions_set

    def is_pred_prey(self) -> bool:
        return IS_PRED_PREY


class BeingType:
    name: str
    preds: t.Set['BeingType']
    prey: t.Set['BeingType']
    colour: Colour

    def __init__(self, name: str, colour: t.Tuple):
        self.name = name
        self.colour = colour
        self.preds = set()
        self.prey = set()

    def __str__(self):
        return self.name

    def add_prey(self, prey: 'BeingType') -> None:
        self.prey.add(prey)
        prey.preds.add(self)

    def create_being(self, position: Position) -> 'Being':
        return Being(self, position)

    def is_prey(self) -> bool:
        return len(self.prey) == 0


class Being:
    type_: BeingType
    position: Position
    dead: bool = False
    birth: bool = False
    age: int = 0
    
    def __init__(self, type_: BeingType, position: Position):
        self.type_ = type_
        self.position = position
    
    def move(self, store: Store, type_position_count: t.Dict[Position, int]) -> None:
        valid_new_positions = store.get_valid_adjacent_positions(self.position)
        max_new_position = None
        max_new_position_score = -99
        no_position_score = True
        for new_position in valid_new_positions:
            total_preds = sum([type_position_count[new_position][pred] for pred in self.type_.preds])
            total_prey = sum([type_position_count[new_position][prey] for prey in self.type_.prey])
            total_own = type_position_count[new_position][self.type_]
            if new_position != self.position: total_own += 1
            score = self._position_score(total_preds,total_prey, total_own)
            if score > max_new_position_score:
                max_new_position_score = score
                max_new_position = new_position
            if score != 0:
                no_position_score = False
        
        if no_position_score or random.random() < RANDOM_MOVE_CHANCE:
            max_new_position = random.choice(valid_new_positions)
        
        type_position_count[self.position][self.type_] -= 1
        type_position_count[max_new_position][self.type_]  += 1
        store.move_being(self, max_new_position)

    def _position_score(self, preds: int, prey: int, own: int) -> float:
        chance_to_eat = min(prey/own, 1)
        chance_to_be_eaten = min(preds/own, 1)
        return chance_to_eat - chance_to_be_eaten

    def eat(self, store: Store) -> None:
        if self.dead: return

        if len(self.type_.prey) > 0:
            prey_types = list(self.type_.prey)
            random.shuffle(prey_types)
            for prey_type in prey_types:
                if len(store.being_positions[self.position][prey_type]) > 1 or \
                    (len(store.being_positions[self.position][prey_type]) == 1 and random.random() < LAST_SPECIES_DEATH_CHANCE):
                    prey = list(store.being_positions[self.position][prey_type])
                    eaten_prey = random.choice(prey)
                    eaten_prey.dead = True
                    self.birth = True
                    store.remove_being(eaten_prey)
                    break
        else:
            if random.random() < PREY_BIRTH_CHANCE:
                self.birth = True

    def reproduce(self, store: Store) -> None:
        if self.dead or not self.birth: return

        valid_positions = store.get_valid_adjacent_positions(self.position)
        if RANDOM_BIRTH_LOCATION:
            store.add_being(self.type_, random.choice(valid_positions))
            if not store.is_pred_prey() and random.random() < GENERAL_SECOND_BIRTH_CHANCE:
                store.add_being(self.type_, random.choice(valid_positions))
        else:
            store.add_being(self.type_, self.position)
            if not store.is_pred_prey() and random.random() < GENERAL_SECOND_BIRTH_CHANCE:
                store.add_being(self.type_, self.position)
        self.birth = False
    
    def increase_age(self, store: Store) -> None:
        if self.dead: return
        self.birth = False
        self.age += 1
        if (
            (self.type_.is_prey() and self.age > PREY_MAX_AGE) or \
            (store.is_pred_prey() and self.age > PRED_MAX_AGE) or \
            (not store.is_pred_prey() and self.age > GENERAL_MAX_AGE)
        ):
            store.remove_being(self)
            

class Sim:
    history: t.Dict['BeingType', t.List[int]]
    store: Store

    def __init__(self, store: Store):
        self.store = store
        self.history = {type_: [] for type_ in store.types}

    def sim_one(self) -> None:
        self._log()
        beings = self.store.get_all_beings_random_list()
        type_position_count = self.store.get_type_position_count()
        
        for being in beings:
            being.move(self.store, type_position_count)
        
        for being in beings:
            being.eat(self.store)
        
        should_reproduce = self._should_reproduce_chance()
        for being in beings:
            if not ENABLE_REPRODUCTION_CHANCE:
                being.reproduce(self.store)
            elif random.random() > should_reproduce[being.type_]:
                being.reproduce(self.store)
        
        for being in beings:
            being.increase_age(self.store)

        if ENABLE_CULL:
            for type_ in self.store.types:
                self._type_overpopulation_cull(type_)
    
    def _log(self) -> None:
        type_count = self.store.get_type_count()
        for type_ in self.store.types:
            self.history[type_].append(type_count[type_])
        total_log = f'Total: {sum(type_count.values())}'
        type_count_log = ', '.join([f'{type_.name}: {type_count[type_]}' for type_ in self.store.types])
        print(f'{total_log}, {type_count_log}')

    """
    Returns the chance that a being will give birth, given it has eaten this iteration.
    This scales based on the number of valid squares in the map times the multiplier.
    """
    def _should_reproduce_chance(self) -> t.Dict:
        type_count = self.store.get_type_count()
        should_reproduce = {}
        for type_, count in type_count.items():
            if not self.store.is_pred_prey():
                base = len(self.store.possible_positions_list) * GENERAL_REPRODUCTION_MULTIPLIER 
                should_reproduce[type_] = (count - (base/2)) / base
            elif type_.is_prey():
                base = len(self.store.possible_positions_list) * PREY_REPRODUCTION_MULTIPLIER 
                should_reproduce[type_] = (count - (base/2)) / base
            else:
                base = len(self.store.possible_positions_list) * PRED_REPRODUCTION_MULTIPLIER
                should_reproduce[type_] = (count - (base/2)) / base
        return should_reproduce

    """
    Finds the square with the most beings of the given type.
    If the square exceeds the allowance, beings have a chance of dying based on their exceedance.
    The chance of dying also applies to the squares directly adjacent to the dense one.
    """
    def _type_overpopulation_cull(self, type_: 'BeingType') -> None:
        position_counts = []

        for position, type_beings in self.store.being_positions.items():
            position_type_count = len(type_beings[type_])
            position_counts.append((position_type_count, position))
        
        position_counts.sort(reverse=True)
        most_populated_position = position_counts[0]
        base = len(self.store.possible_positions_list)
        population_allowance = base / (base ** 0.5)
        death_chance = (-math.e ** -(most_populated_position[0] / population_allowance)) + 1
        if self.store.is_pred_prey():
            if type_.is_prey(): death_chance *= PREY_DEATH_CHANCE_MULTIPLIER
            else: death_chance *= PRED_DEATH_CHANCE_MULTIPLIER
        else:
            death_chance *= GENERAL_DEATH_CHANCE_MULTIPLIER

        valid_positions = self.store.get_valid_adjacent_positions(most_populated_position[1])
        
        for position in valid_positions:
            dead_beings = []
            for being in self.store.being_positions[position][type_]:
                if random.random() < death_chance:
                    dead_beings.append(being)
            [self.store.remove_being(being) for being in dead_beings]
