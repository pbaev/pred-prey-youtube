### Background

This repository creates a simple predator prey simulation as seen in
[this youtube video](https://youtu.be/_RyJszeszNQ)    

The code may be hacky, it isn't optimized for speed or readability,
it's posted for anyone who is curious about how the simulation works 
and wants to branch off of it.

### Running the simulation

main.py contains an example simulation setup, run it with:
```
python main.py
```

### How it works

* `BeingType` identifies the groups of predator or prey.
* `Being` represents individual predators or prey.    
* `Store` stores info like all the beings, their positions, and the map which they can move on.    
* `Sim` runs the simulation using the above classes.

Read through the example in main.py for info about how to set up each class.

`sim_to_images()` runs the simulation loop that creates images in the `imgs` folder.
The actual simulation runs in `Sim.sim_one()`, here the beings:
move, eat, reproduce, age, and are culled.

### Simulation paramaters

Paramaters that can be changed to configure the simulation are in `constants.py`.

### Converting images to video

The simulation outputs a folder of images but it does not automatically convert them into a video.

On Ubuntu, I installed ffmpeg and used the command below to convert all the .png files
in a folder to a video.

```
ffmpeg -framerate 10 -pattern_type glob -i '*.png' -c:v ffv1 out.avi
```
