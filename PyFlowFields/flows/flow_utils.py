import math
import tkinter.filedialog


class Vector:

	@staticmethod
	def zero():
		return Vector(0, 0)

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def normalize(self):
		_length = self.length()
		self.x /= _length
		self.y /= _length

	def length(self) -> float:
		return math.sqrt(self.x ** 2 + self.y ** 2)

	def set_components(self, x, y):
		self.x = x
		self.y = y

	def get_components(self):
		return [self.x, self.y]

	def subtract(self, other):
		if isinstance(other, Vector):
			self.x -= other.x
			self.y -= other.y
			return self

	def __iadd__(self, other):
		if isinstance(other, Vector):
			self.x += other.x
			self.y += other.y
			return self

	def __isub__(self, other):
		if isinstance(other, Vector):
			self.x -= other.x
			self.y -= other.y
			return self

	def __imul__(self, other):
		if isinstance(other, (int, float)):
			self.x *= other
			self.y *= other
			return self

	def __mul__(self, other):
		if isinstance(other, (int, float)):
			return Vector(self.x * other, self.y * other)


class NormalizedForce:
	"""
	Unitary vector, part of a flow field whose force will be applied to nearby particles
	"""

	def __init__(self, deg_angle: float):
		self.alpha = 0
		self.force = Vector.zero()
		self.set_angle(deg_angle)

	def compute_components(self):
		self.force.x = math.cos(self.alpha)
		self.force.y = math.sin(self.alpha)

	def set_angle(self, deg_angle: float):
		self.alpha = math.radians(deg_angle)
		self.compute_components()


def hue(value, _saturation, alpha: int = -1) -> list[int]:
	"""
	Credits : Tartiflow
	"""
	r, g, b = 0, 0, 0
	value %= 360
	if value < 60:
		r = 255
		g = int(value * 255 / 60)
	elif value < 120:
		r = int(value * -255 / 60) + 510
		g = 255
	elif value < 180:
		g = 255
		b = int(value * 255 / 60) - 510
	elif value < 240:
		g = int(-value * 255 / 60) + 1020
		b = 255
	elif value < 300:
		r = int(value * 255/60) - 1020
		b = 255
	else:
		r = 255
		b = int(-value * 255 / 60) + 1530

	_saturation /= 255

	return [r * _saturation, g * _saturation, b * _saturation, 255 if alpha < 0 else alpha]


def save_file(title: str, contents: str, extension: str) -> bool:
	try:
		with tkinter.filedialog.asksaveasfile(
				title=title,
				mode='w',
				defaultextension=extension,
				filetypes=[(extension.upper(),  ".%s" % extension)]
		) as file:
			file.write(contents)
		return True
	except Exception as e:
		print("An error occurred : %s" % e)
