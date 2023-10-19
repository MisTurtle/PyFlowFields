import json
import time
import pyperclip
import numpy as np
import pygame.display
import matplotlib.pyplot as plt
import PyFlowFields.flows.perlin_noise_generator as png

from PyFlowFields.flows.flow_utils import *
from PyFlowFields.flows.flow_settings import *


# TODO : JSON color functions
# TODO : Different noise functions
# TODO : Noise seed research form


class FlowField:

	def __init__(self, settings: FlowFieldSettings):
		self.settings = settings
		if self.settings.seed <= 0:
			self.randomize_seed()

		self.origin = Vector.zero()  # Perlin origin
		self.components = [
			[NormalizedForce(0) for _ in range(settings.size.x)]
			for _ in range(settings.size.y)
		]
		self.noise = np.ndarray((1, 1))
		self.update()

	def randomize_seed(self, _update: bool = False):
		self.set_seed(random.randint(0, 0xFFFFFF), _update)

	def set_seed(self, seed: int, _update: bool = False):
		self.settings.seed = seed
		if _update:
			self.update()

	def add_offset(self, offset: Vector, _update: bool = False):
		self.origin += offset
		if _update:
			self.update()

	def set_offset(self, offset: Vector, _update: bool = False):
		self.origin = offset
		if _update:
			self.update()

	def inc_variation(self, by: float, update: bool = False):
		self.set_variation(max(1., self.settings.variation_level + by), update)

	def dec_variation(self, by: float, update: bool = False):
		self.set_variation(max(1., self.settings.variation_level - by), update)

	def set_variation(self, zoom: float, update: bool = False):
		self.settings.variation_level = zoom
		if update:
			self.update()

	def update(self, dt: float = 0):
		self.origin += self.settings.offset_step * dt
		self.noise = png.create(
			self.settings.size.x, self.settings.size.y,
			self.settings.variation_level,
			self.origin.x, self.origin.y,
			self.settings.seed
		)
		for y, flow_line in enumerate(self.components):
			for x, flow_el in enumerate(flow_line):
				flow_el.set_angle(self.noise[y][x] * self.settings.angle_range * (-1 if self.settings.inverted else 1))

	def invert(self, update: bool):
		self.settings.inverted = not self.settings.inverted
		if update:
			self.update()

	def display(self, unit_size: int):
		"""
		:param unit_size: Length for each flow component
		"""
		tex = np.ones(((self.settings.size.x + 2) * unit_size, (self.settings.size.y + 2) * unit_size), np.int16) * 255
		for y, flow_line in enumerate(self.components):
			for x, flow_el in enumerate(flow_line):
				# Compute points belonging to the vector
				points = np.linspace(
					((x + 1) * unit_size, (y + 1) * unit_size),
					((x + 1 + flow_el.force.x) * unit_size, (y + 1 + flow_el.force.y) * unit_size),
					unit_size
				)
				# Draw vector
				for point in points:
					tex[int(point[1])][int(point[0])] = 0

		_, plots = plt.subplots(1, 2)

		plots[0].title.set_text('Perlin Noise (seed=%d)' % self.settings.seed)
		plots[0].imshow(self.noise, cmap='gray')
		plots[1].title.set_text('Flow Field')
		plots[1].imshow(tex, cmap='gray')

		plt.show()


class Particle(Vector):

	def __init__(self, x, y):
		super().__init__(x, y)
		self.motion = Vector.zero()
		self.prev_pos = Vector.zero()
		self.skip_drawing = False

	def update(self, env_size: tuple[int, int], ff: FlowField, dt: float, sim_time: float, settings: ParticleMovementSettings):
		"""
		:param env_size: Environment size in which the particle is evolving (Required to compute vector coordinates)
		:param ff: Flow field applied to this particle
		:param dt: Delta time for physics calculation
		:param sim_time: Time since the simulation started
		:param settings: Settings for this particle's movement
		"""
		# Save current coordinates
		self.prev_pos.set_components(self.x, self.y)

		# Get closest flow element
		ff_size = ff.settings.size
		flow_coords = Vector(
			int(self.x * ff_size.x / env_size[0]),
			int(self.y * ff_size.y / env_size[1])
		)
		if not 0 <= flow_coords.x < ff_size.x:
			flow_coords.x = 0
		if not 0 <= flow_coords.y < ff_size.y:
			flow_coords.y = 0

		flow_el = ff.components[flow_coords.y][flow_coords.x]

		force_power = settings.flow_force
		if settings.force_variation > 0 and settings.force_period > 0:
			force_power += settings.force_variation * math.cos(math.pi * sim_time / settings.force_period)

		self.motion += flow_el.force * force_power
		if settings.force_max_speed or self.motion.length() > settings.max_speed:
			self.motion.normalize()
			self.motion *= settings.max_speed

		# Actually move the particle
		self.x = (self.x + self.motion.x * dt) % env_size[0]
		self.y = (self.y + self.motion.y * dt) % env_size[1]

		deltaX = abs(self.x - self.prev_pos.x)
		deltaY = abs(self.y - self.prev_pos.y)
		self.skip_drawing = deltaX >= 0.8 * env_size[0] or deltaY >= 0.8 * env_size[1]

	def draw(self, env: pygame.Surface, sim_duration: float, settings: ParticleDrawingSettings):
		if self.skip_drawing:
			return

		color = settings.color
		if isinstance(color, Callable):
			color = color(self, sim_duration)

		if settings.draw_mode == ParticleDrawingSettings.MODE_LINEAR:
			pygame.draw.line(env, color, (self.prev_pos.x, self.prev_pos.y), (self.x, self.y))
		elif settings.draw_mode == ParticleDrawingSettings.MODE_PARTICLE:
			pygame.draw.circle(env, color, (self.x, self.y), settings.width)
		elif settings.draw_mode == ParticleDrawingSettings.MODE_BLOC:
			pygame.draw.rect(env, color, pygame.Rect(self.x - settings.width / 2, self.y - settings.width / 2, settings.width, settings.width))
		elif settings.draw_mode == ParticleDrawingSettings.MODE_HOLLOW:
			pygame.draw.circle(env, color, (self.x, self.y), settings.width, width=1)
		elif settings.draw_mode == ParticleDrawingSettings.MODE_HOLLOW_BLOC:
			pygame.draw.rect(env, color, pygame.Rect(self.x - settings.width / 2, self.y - settings.width / 2, settings.width, settings.width), width=1)



class FlowSimulation:

	@staticmethod
	def from_data(json_data: dict, cmd_data: dict = None):
		"""
		:param json_data: Data extracted from a json file
		:param cmd_data: Data extracted from the command line (will overwrite json data)
		"""
		if cmd_data is None:
			cmd_data = {}
		for k, v in cmd_data.items():
			if v is not None:
				json_data[k] = v

		# Clean up input data
		filtered = dict(filter(lambda pair: pair[1] is not None, json_data.items()))
		filtered = {key.replace("-", "_"): val for key, val in filtered.items()}

		return FlowSimulation(
			SimulationSettings(**filtered),
			FlowFieldSettings(**filtered),
			ParticleSettings(
				ParticleDrawingSettings(**filtered),
				ParticleMovementSettings(**filtered)
			)
		)

	TEMP_DEBUG_TIME = 3  # seconds
	DEBUG_TEXT_SIZE = 11  # px

	# PyGame Elements
	surface: pygame.Surface = None
	font: pygame.font.Font = None

	# Simulation Body
	flow_field: FlowField = None
	particles: list[Particle] = []

	# Simulation State
	start_time, copy_seed_time = -1, -1
	running, paused, debug_info = False, False, False
	fps_history = []

	def __init__(self, settings: SimulationSettings, ff_settings: FlowFieldSettings, particle_settings: ParticleSettings):
		self.settings = settings
		self.flow_field = FlowField(ff_settings)
		self.particle_settings = particle_settings
		self._init()

	def _init(self):
		# Init PyGame window
		pygame.init()
		if self.settings.fullscreen:
			self.surface = pygame.display.set_mode(flags=pygame.FULLSCREEN)
		else:
			self.surface = pygame.display.set_mode(self.settings.screen_size)
		pygame.display.set_caption(self.settings.name)
		self.clear_canvas()

		# Init PyGame fonts
		pygame.font.init()
		self.font = pygame.font.SysFont("couriernew", self.DEBUG_TEXT_SIZE)

		# Instantiate population
		p_rdm = random.Random(self.settings.particle_seed)
		width, height = self.surface.get_size()
		self.particles = [Particle(p_rdm.randint(1, width), p_rdm.randint(1, height)) for _ in range(self.settings.pop_size)]

	def clear_canvas(self):
		self.surface.fill(self.settings.clear_color)

	def start_sim(self):
		self.start_time = time.time()
		self.running = True
		clock = pygame.time.Clock()

		while self.running:
			dt = actual_dt = clock.tick(self.settings.fps) / 1000

			# Poll events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.KEYDOWN:
					self._handle_key_event(event)

			if self.paused:
				dt = 0
				self.start_time += actual_dt

			# Clear canvas
			temp_layer = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
			if self.settings.clear_each_frame:
				temp_layer = self.surface
				self.clear_canvas()

			self.flow_field.update(dt)

			# Update particles
			sim_time = time.time() - self.start_time
			for particle in self.particles:
				particle.update(temp_layer.get_size(), self.flow_field, dt, sim_time, self.particle_settings.physics)
				particle.draw(temp_layer, sim_time, self.particle_settings.design)

			if not self.settings.clear_each_frame:
				# Draw on the actual surface and apply transparency
				self.surface.blit(temp_layer, temp_layer.get_rect())

			if self.debug_info:
				self._debug_all(1 / actual_dt)

			pygame.display.flip()
		pygame.quit()

	def _handle_key_event(self, event: pygame.event.Event):
		if event.key == pygame.K_q:
			self.running = False
		elif event.key == pygame.K_p:
			self.paused = not self.paused
		# elif event.key == pygame.K_s:  TODO : Ask user for a save location
		# 	path = os.getcwd() + "\\output\\"
		# 	pygame.image.save(self.surface, path + ("Flow_%d.png" % len(os.listdir(path))))
		elif event.key == pygame.K_RETURN:
			self.flow_field.randomize_seed(False)
		elif event.key == pygame.K_d:
			self.debug_info = not self.debug_info
		elif event.key == pygame.K_c:
			pyperclip.copy("seeds={'field': %d, 'particles': %d}" % (self.flow_field.settings.seed, self.settings.particle_seed))
			self.copy_seed_time = time.time()
		elif event.key == pygame.K_j:
			save_file("Save flow simulation settings...", json.dumps(self.serialize(), indent=4), "json")
		elif event.key == pygame.K_BACKSPACE:
			self.clear_canvas()

	def _debug_all(self, fps: float):
		self.fps_history.append(fps)
		if len(self.fps_history) > 100:
			self.fps_history = self.fps_history[1:]

		contents = [
			"--> Debug Information <--",

			["FPS : %3.0f" % fps, 1.5],
			"Max : %3.0f" % max(self.fps_history),
			"Min : %3.0f" % min(self.fps_history),
			"Avg : %3.0f" % (sum(self.fps_history) / len(self.fps_history)),

			["Sim Time : %5.2f" % (time.time() - self.start_time), 1.5],
			"Sim Status : %s" % ("paused" if self.paused else "running"),
			"Sim Population : %d" % self.settings.pop_size,
			"Sim Size : %d x %d" % self.surface.get_size(),

			["FlowField Seed : %d" % self.flow_field.settings.seed, 1.5],
			"Particle Seed : %d" % self.settings.particle_seed,

			["Action Key List : ", 3],
			"<ENTER> Randomize seed",
			# "<s> Export current frame as .png file",
			"<q> Quit the simulation",
			"<p> Pause the simulation",
			"<d> Show/Hide debug info",
			"<c> Copy current seeds",
			"<j> Export settings to JSON file"
		]
		if time.time() - self.copy_seed_time < self.TEMP_DEBUG_TIME:
			contents.append("[+] Seeds copied to the clipboard !")

		prev_rect = None
		for content in contents:
			spacing = 1
			if isinstance(content, list):
				if len(content) == 2:
					spacing = content[1]
				content = content[0]

			text = self.font.render(content, True, pygame.Color(255, 255, 255, 255), (0, 0, 0, 20))
			rect = text.get_rect()
			rect.left = 0
			if prev_rect is not None:
				rect.top = prev_rect.top + spacing * rect.height
			prev_rect = rect
			self.surface.blit(text, rect)

	def serialize(self) -> dict:
		data = {}
		targets = [
			self.settings.serialize(),
			self.flow_field.settings.serialize(),
			self.particle_settings.design.serialize(),
			self.particle_settings.physics.serialize()
		]
		for target in targets:
			for k, v in target.items():
				data[k] = v
		return data
