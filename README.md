# PyFlowFields - Python Flows Simulation

## Description
**PyFlowFields** is a python module created to provide easy access to the beautiful world of particle flow fields.

## Features

- Fast and easy integration in existing applications
- Reproducibility using predefined random seeds
- Numerous settings to instantiate a simulation from the command line
- Save your favorite settings to a reusable json config file
- Customize your work pieces with the numerous settings available

## Installation

TODO

## Getting Started

### 0. Create your first simulation

To check if the istallation was successfull, open a new python interpreter and type in the following code. If everything works properly, you should see a fullscreen window open a some particles floating around the screen

```python
from PyFlowFields import *

sim = FlowSimulation.from_data({})
sim.start_sim()
```

Everything works fine? Awesome, let's see what we can do now...

### 1. Key binds

When running a simulation, various keys are setup to perform different actions. Those actions are specified in the table below, and can be found at any time by pressing [D] in a simulation

|  Key  | Action                |
|:-----:|-----------------------|
| ENTER | Randomize the seed    |
|   D   | Show debug info       |
|   C   | Copy seeds            |
|   J   | Save settings as JSON |
|   P   | Pause the simulation  |
|   Q   | Quit the simulation   |

### 2. Exhaustive settings list

A list of all the currently available settings can be found in the following table, and examples of how to use them can be found in the ``tests`` folder

<details>

<summary><b><u>i. Global Simulation Settings</u></b></summary>

|   Setting    |     Type     | Description                                         |
|:------------:|:------------:|-----------------------------------------------------|
|     name     |  ``String``  | Simulation window title                             |
|  fullscreen  |   ``Bool``   | Display the simulation fullscreen                   |
|  screensize  | ``Int (x2)`` | Window dimensions with fullscreen off               |
|  population  |   ``Int``    | Particle count for the simulation                   |
| particleseed |   ``Int``    | Seed used for the particles spawn position          |
|    clear     |   ``Bool``   | Clear the simulation each frame                     |
|      bg      | ``Int (x3)`` | Red, Green and Blue values for the background color |
|     fps      |   ``Int``    | Max frame rate for the simulation                   |

</details>

<br>

<details>

<summary><b><u>ii. Flow Field Settings</u></b></summary>

|  Setting  |      Type      | Description                                            |
|:---------:|:--------------:|--------------------------------------------------------|
|   fsize   |  ``Int (x2)``  | Frame subdivisions to place flow field components      |
|   fvar    |   ``Float``    | Variation rate between each flow field component       |
|  frange   |   ``Float``    | Angle range for flow field components                  |
|   fseed   |    ``Int``     | Seed used in the noise generation function             |
| finverted |    ``Bool``    | Invert the noise function                              |
|   fstep   | ``Float (x2)`` | Origin shift each second applied on the noise function |

</details>

<br>

<details>

<summary><b><u>iii. Particle Drawing Settings</u></b></summary>

| Setting |     Type     | Description                                               |
|:-------:|:------------:|-----------------------------------------------------------|
|  pmode  |   ``Int``    | Particle drawing mode (0: Particle Mode, 1 : Linear Mode) |
| pwidth  |   ``Int``    | Particle size (in particle mode only)                     |
| pcolor  | ``Int (x3)`` | Red, Green, Blue [and Alpha] value for the particle color |

</details>

<br>

<details>

<summary><b><u>iv. Particle Physics Settings</u></b></summary>

|   Setting   |   Type    | Description                                                       |
|:-----------:|:---------:|-------------------------------------------------------------------|
|   pforce    | ``Float`` | Force applied by a flow component to a particle                   |
|    pvar     | ``Float`` | Oscillations of the flow components' force over time              |
|   pperiod   | ``Float`` | Period for the previously described oscillations                  |
|  pmaxspeed  | ``Float`` | Particles max speed (in px/sec)                                   |
| pforcespeed | ``Bool``  | Force particles to go at max speed at any point in the simulation |

</details>


### 3. Customize your simulation from a python program

Every setting listed in the previous section has a default value. This way, you can focus on changing only the settings you want. Let's modify the code snippet from section 0 and tweak some settings :

```python
from PyFlowFields import *

sim = FlowSimulation.from_data({
	"name": "My Custom Simulation",  # Simulation name
	"population": 1000,  # Simulate 1000 particles
	"bg": [40, 40, 40],  # Set the background to a grayish color
    "particleseed": 1,  # Constant particle seed to get a reproducible simulation
	"fseed": 1,  # Constant noise seed to get a reproducible simulation
	"fstep": [0.15, 0.15],  # Change the noise origin by 0.15 every second to break boring patterns
	"pcolor": [255, 255, 255],  # Set the particles color to white
	"pforce": 7.2,  # Pump up the flow force to converge more quickly
	"pvar": 0.8,  # Make `pforce` oscillate by ±0.8 every `pperiod` seconds
	"pperiod": 2  # `pforce` will oscillate over the course of 2 seconds
})
sim.start_sim()
```

Please note that this will yield the exact same result as the following code :

```python
from PyFlowFields import *

sim_settings = SimulationSettings(
	name="My Custom Simulation",
	population= 1000,
	bg=[40, 40, 40],
	particleseed=1
)
ff_settings = FlowFieldSettings(
	fseed=1,
	fstep=[0.15, 0.15]
)
pdraw_settings = ParticleDrawingSettings(
	pcolor=[255, 255, 255]
)
pphysics_settings = ParticleMovementSettings(
	pforce=7.2,
	pvar=0.8,
	pperiod=2
)

sim = FlowSimulation(
	sim_settings, ff_settings, ParticleSettings(pdraw_settings, pphysics_settings)
)
sim.start_sim()
```

### 4. Start a simulation from the command line

You might be wanting to taunt your friends and start your beautiful simulation from a single command in your terminal. As with the previous python programs, you can customize every settings listed in section 2 from a command line.

To get a list of all available settings in the command line, type :

```commandline
python -m PyFlowFields -h
```

Here's the command line that will yield the exact same output as both previous python languages :

```commandline
python -m PyFlowFields -name "My Custom Simulation" -population 1000 -bg 40 40 40 -particleseed 1 -fseed 1 -fstep 0.15 0.15 -pcolor 255 255 255 255 -pforce 7.2 -pvar 0.8 -pperiod 2
```

### 5. Save your simulation settings to a JSON file for later use

Commands and programs like the previous ones are fine, but you can also start a simulation from a JSON file.

Let's consider the following config file :

```json
{
    "name": "My Custom Simulation",
    "fullscreen": true,
    "screensize": [
        500,
        500
    ],
    "population": 1000,
    "particleseed": 1,
    "clear": true,
    "bg": [
        40,
        40,
        40
    ],
    "fps": 60,
    "fsize": [
        30,
        30
    ],
    "fvar": 2,
    "frange": 360,
    "fseed": 1,
    "finverted": false,
    "fstep": [
        0.15,
        0.15
    ],
    "pmode": 0,
    "pwidth": 3,
    "pcolor": [
        255,
        255,
        255
    ],
    "pforce": 7.2,
    "pvar": 0.8,
    "pperiod": 2,
    "pmaxspeed": 300,
    "pforcespeed": false
}
```

Once again, we can discard the parameters which should take the default value. Here's a cleaner version of the previous file :

```json
{
    "name": "My Custom Simulation",
    "population": 1000,
    "particleseed": 1,
    "bg": [
        40,
        40,
        40
    ],
    "fseed": 1,
    "fstep": [
        0.15,
        0.15
    ],
    "pcolor": [
        255,
        255,
        255
    ],
    "pforce": 7.2,
    "pvar": 0.8,
    "pperiod": 2
}
```

It is now easier than ever to start a simulation using previously defined settings. All you have to do is...

> ... from the command line
> ```commandline
> python -m PyFlowFields -cfg path/to/config.json

> ... from a python script
> ```python
> from PyFlowFields import *
> import json
>
> with open("path/to/config.json", "r") as data_file:
>   sim = FlowSimulation.from_data(json.loads(data_file.read()))
>
> sim.start_sim()