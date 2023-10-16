import argparse
import random
from typing import Callable

from PyFlowFields.flows.flow_utils import Vector


class SimulationSettings:

	ARG_NAME = "name"
	ARG_SCREEN_SIZE = "screensize"
	ARG_POPULATION = "population"
	ARG_PARTICLE_SEED = "particleseed"
	ARG_BACKGROUND = "bg"
	ARG_FPS = "fps"
	ARG_FULLSCREEN = "fullscreen"
	ARG_CLEAR_FRAME = "clear"

	@staticmethod
	def add_arguments(parser: argparse.ArgumentParser):
		group = parser.add_argument_group("Simulation Settings")
		group.add_argument("-%s" % SimulationSettings.ARG_NAME, help="Simulation name", type=str, metavar=("name"))
		group.add_argument("-%s" % SimulationSettings.ARG_SCREEN_SIZE, help="Simulation environment size", type=int, action="extend", nargs=2, metavar=("x", "y"))
		group.add_argument("-%s" % SimulationSettings.ARG_POPULATION, help="Particle count to simulate", type=int, metavar=("count"))
		group.add_argument("-%s" % SimulationSettings.ARG_PARTICLE_SEED, help="Seed used to compute particles starting position", type=int, metavar=("seed"))
		group.add_argument("-%s" % SimulationSettings.ARG_BACKGROUND, help="Canvas background color (0-255)", type=int, action="extend", nargs=3, metavar=("R", "G", "B"))
		group.add_argument("-%s" % SimulationSettings.ARG_FPS, help="Max FPS for the simulation", type=int, metavar=("fps"))
		group.add_argument("--%s" % SimulationSettings.ARG_FULLSCREEN, help="Display the simulation fullscreen", action=argparse.BooleanOptionalAction)
		group.add_argument("--%s" % SimulationSettings.ARG_CLEAR_FRAME, help="Clear the canvas on each frame", action=argparse.BooleanOptionalAction)

	def __init__(self, **kwargs):
		self.name = kwargs.get(self.ARG_NAME, "FlowField Simulation")  # Name for the sim window
		self.fullscreen = kwargs.get(self.ARG_FULLSCREEN, True)  # Display the simulation fullscreen
		self.screen_size = tuple(kwargs.get(self.ARG_SCREEN_SIZE, (500, 500)))  # Simulation screen size
		self.pop_size = kwargs.get(self.ARG_POPULATION, 300)  # Particle count
		# Seed used to get random starting pos
		self.particle_seed = kwargs.get(self.ARG_PARTICLE_SEED, random.randint(0, 0xFFFFFFFF))
		self.clear_each_frame = kwargs.get(self.ARG_CLEAR_FRAME, True)  # Clear the frame on each frame
		self.clear_color = kwargs.get(self.ARG_BACKGROUND, [0, 0, 0])  # Background color
		self.fps = kwargs.get(self.ARG_FPS, 60)

	def serialize(self):
		return {
			self.ARG_NAME: self.name,
			self.ARG_FULLSCREEN: self.fullscreen,
			self.ARG_SCREEN_SIZE: self.screen_size,
			self.ARG_POPULATION: self.pop_size,
			self.ARG_PARTICLE_SEED: self.particle_seed,
			self.ARG_CLEAR_FRAME: self.clear_each_frame,
			self.ARG_BACKGROUND: self.clear_color,
			self.ARG_FPS: self.fps
		}


class FlowFieldSettings:

	ARG_SIZE = "fsize"
	ARG_VARIATION = "fvar"
	ARG_RANGE = "frange"
	ARG_SEED = "fseed"
	ARG_STEP = "fstep"
	ARG_INVERTED = "finverted"

	@staticmethod
	def add_arguments(parser: argparse.ArgumentParser):
		group = parser.add_argument_group("FlowField Settings")
		group.add_argument("-%s" % FlowFieldSettings.ARG_SIZE, help="Environment vectorial subdivisions", type=int, action="extend", nargs=2, metavar=("width", "height"))
		group.add_argument("-%s" % FlowFieldSettings.ARG_VARIATION, help="Variation level between each flow field component", type=float, metavar=("level"))
		group.add_argument("-%s" % FlowFieldSettings.ARG_RANGE, help="Angle range for each flow field component (in degrees)", type=float, metavar=("max_angle"))
		group.add_argument("-%s" % FlowFieldSettings.ARG_SEED, help="Seed used to compute vector directions", type=int, metavar=("seed"))
		group.add_argument("-%s" % FlowFieldSettings.ARG_STEP, help="Noise offset to walk each second", type=float, action="extend", nargs=2, metavar=("x", "y"))
		group.add_argument("--%s" % FlowFieldSettings.ARG_INVERTED, help="Invert vector directions", action=argparse.BooleanOptionalAction)

	def __init__(self, **kwargs):
		self.size = Vector(*kwargs.get(self.ARG_SIZE, [30, 30]))
		self.variation_level = kwargs.get(self.ARG_VARIATION, 2)
		self.angle_range = kwargs.get(self.ARG_RANGE, 360)
		self.seed = kwargs.get(self.ARG_SEED, -1)
		self.inverted = kwargs.get(self.ARG_INVERTED, False)
		self.offset_step = Vector(*kwargs.get(self.ARG_STEP, [0, 0]))

	def serialize(self):
		return {
			self.ARG_SIZE: self.size.get_components(),
			self.ARG_VARIATION: self.variation_level,
			self.ARG_RANGE: self.angle_range,
			self.ARG_SEED: self.seed,
			self.ARG_INVERTED: self.inverted,
			self.ARG_STEP: self.offset_step.get_components()
		}


class ParticleMovementSettings:

	ARG_FORCE = "pforce"
	ARG_VARIATION = "pvar"
	ARG_PERIOD = "pperiod"
	ARG_MAX_SPEED = "pmaxspeed"
	ARG_FORCE_SPEED = "pforcespeed"

	@staticmethod
	def add_arguments(parser: argparse.ArgumentParser):
		group = parser.add_argument_group("Physics Settings")
		group.add_argument("-%s" % ParticleMovementSettings.ARG_FORCE, help="Flow field influence on particles", type=float, metavar=("force"))
		group.add_argument("-%s" % ParticleMovementSettings.ARG_VARIATION, help="Flow field force oscillations amplitude", type=float, metavar=("amplitude"))
		group.add_argument("-%s" % ParticleMovementSettings.ARG_PERIOD, help="Time period for flow field oscillations (in seconds)", type=float, metavar=("duration"))
		group.add_argument("-%s" % ParticleMovementSettings.ARG_MAX_SPEED, help="Max speed for particles (in px/s)", type=float, metavar=("speed"))
		group.add_argument("--%s" % ParticleMovementSettings.ARG_FORCE_SPEED, help="Force particles to go at max speed", action=argparse.BooleanOptionalAction)

	def __init__(self, **kwargs):
		# How much a flow's force is impactful at any point on this particle
		self.flow_force = kwargs.get(self.ARG_FORCE, 6)
		# df : Make the flow force oscillate between [flow_force - df ; flow_force + df]
		self.force_variation = kwargs.get(self.ARG_VARIATION, 0)
		# Flow force variation period (Time in seconds to go from the lowest force to the highest and back again)
		self.force_period = kwargs.get(self.ARG_PERIOD, 1)
		# Max speed for each particle
		self.max_speed = kwargs.get(self.ARG_MAX_SPEED, 300)
		# Force particles to go at max speed at any time during the simulation
		self.force_max_speed = kwargs.get(self.ARG_FORCE_SPEED, False)

	def serialize(self):
		return {
			self.ARG_FORCE: self.flow_force,
			self.ARG_VARIATION: self.force_variation,
			self.ARG_PERIOD: self.force_period,
			self.ARG_MAX_SPEED: self.max_speed,
			self.ARG_FORCE_SPEED: self.force_max_speed
		}


class ParticleDrawingSettings:

	MODE_PARTICLE = 0
	MODE_LINEAR = 1

	ARG_MODE = "pmode"
	ARG_WIDTH = "pwidth"
	ARG_COLOR = "pcolor"

	@staticmethod
	def add_arguments(parser: argparse.ArgumentParser):
		group = parser.add_argument_group("Drawing Settings")
		group.add_argument("-%s" % ParticleDrawingSettings.ARG_MODE, help="Particle drawing method (0: Circular, 1: Linear)", choices=[0, 1], type=int, metavar=("mode"))
		group.add_argument("-%s" % ParticleDrawingSettings.ARG_WIDTH, help="Particle size (in pixels)", type=int, metavar=("width"))
		group.add_argument("-%s" % ParticleDrawingSettings.ARG_COLOR, help="Particle color (0-255)", action="extend", nargs=4, type=int, metavar=('R', 'G', 'B', 'A'))

	def __init__(self, **kwargs):
		# How to draw each particle
		self.draw_mode = kwargs.get(self.ARG_MODE, self.MODE_PARTICLE)
		# Width (in linear mode, of the line, in particle mode, of the circle)
		self.width = kwargs.get(self.ARG_WIDTH, 3)
		# Constant color, or callback function to get the color of this particle
		# If it is a callback, it should receive a Particle object and the time since the simulation began
		self.color = kwargs.get(self.ARG_COLOR, [255, 0, 0, 255])

	def serialize(self):
		return {
			self.ARG_MODE: self.draw_mode,
			self.ARG_WIDTH: self.width,
			self.ARG_COLOR: [255, 0, 0] if isinstance(self.color, Callable) else self.color
		}


class ParticleSettings:

	def __init__(self, design: ParticleDrawingSettings, physics: ParticleMovementSettings):
		self.design = design
		self.physics = physics
