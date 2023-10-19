from PyFlowFields import *

linear_settings = {
	"bg": [30, 30, 30],
	"clear": False,
	"population": 1000,
	"pmode": 1,
	"pcolor": [255, 255, 10, 1],
	"pforce": 20,
	"pvar": 0.8,
	"fstep": [0.075, 0.075],
	"particleseed": 2,
	"fseed": 4
}
particle_settings = {
	"bg": [30, 30, 30],
	"population": 2500,
	"pcolor": [255, 255, 10],
	"pforce": 7,
	"pvar": 0.8,
	"pmode": ParticleDrawingSettings.MODE_LINEAR,
	"fstep": [0.2, 0.2],
	"particleseed": 2,
	"fseed": 4,
	"pwidth": 10
}

sim = FlowSimulation.from_data(particle_settings)
sim.start_sim()
