import cv2
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy
import os
import shutil
import typing as t
from constants import *
from structure import *

"""
Converts the being's positions from store into an array where each cell is a bgr colour.
If there are 6 red beings and 3 blue in a cell, the cell will be 66% red and 33% blue.
The cell transparency is set based on the cell with the most beings on the map
"""
def store_to_bgra_array(store: 'Store') -> BgraArray:
    shape = tuple(list(store.map_array.shape) + [4])
    image_array = numpy.zeros(shape)
    max_being_position_total = 0

    # BGR
    for position, beings_dict in store.being_positions.items():
        being_total = 0
        being_type_count = {}
        for type_, beings_list in beings_dict.items():
            being_type_count[type_] = len(beings_list)
            being_total += being_type_count[type_]

        max_being_position_total = max(being_total, max_being_position_total)
        colour = [0, 0, 0, 0]
        for type_, value in being_type_count.items():
            proprotion = value / being_total if being_total > 0 else 0
            colour[0] += type_.colour[0] * proprotion
            colour[1] += type_.colour[1] * proprotion
            colour[2] += type_.colour[2] * proprotion

        image_array[position] = colour

    # Trasnparency/Alpha
    for position, beings_dict in store.being_positions.items():
        being_total = 0
        for type_, beings_list in beings_dict.items():
            being_total += len(beings_list)
        proprotion = being_total / max_being_position_total
        alpha = (-math.e ** (-6 * proprotion)) + 1
        if being_total > 0:
            image_array[position][3] = alpha * 100 + 155
        else:
            image_array[position][3] = 0
    
    return image_array

"""
Creates the plot image.
"""
def history_to_image(history: t.Dict['BeingType', t.List[int]], save_name: str=None) -> None:
    if save_name:
        # Turn off the gui popping up https://stackoverflow.com/questions/65691079/how-to-call-plt-subplots-without-opening-gui
        matplotlib.use('Agg')
    
    fig, ax = plt.subplots()
    for type_, data in history.items():
        time = list(range(1, len(data)+1))
        hex_colour = '#' + ''.join(f'{i:02X}' for i in tuple(reversed(type_.colour)))
        ax.plot(time[-PLOT_ITERATIONS:], data[-PLOT_ITERATIONS:], color=hex_colour, linewidth=5, antialiased=False)
    
    ax.set_ylabel('Population', weight='bold', size=18, color='#262729')
    ax.set_xlabel('Time', weight='bold', size=18, color='#262729')

    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    if save_name:
        plt.savefig(f'{save_name}', transparent=True, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    else:
        plt.show()

def bgra_array_to_image(array: BgraArray, path: str) -> None:
    cv2.imwrite(path, array)

def delete_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)

def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def sim_to_images(sim: 'Sim', count: int) -> None:
    delete_folder(IMAGE_FOLDER)
    create_folder(IMAGE_FOLDER)
    create_folder(f'{IMAGE_FOLDER}/map')
    create_folder(f'{IMAGE_FOLDER}/plot')
    for n in range(count):
        bgr_array = store_to_bgra_array(sim.store)
        zero_padded_n = str(n).zfill(3)
        bgra_array_to_image(bgr_array, f'{IMAGE_FOLDER}/map/test-{zero_padded_n}.png')
        history_to_image(sim.history, f'{IMAGE_FOLDER}/plot/test-{zero_padded_n}.png')
        sim.sim_one()
