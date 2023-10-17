from PyFlowFields import *

settings = {
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

sim = FlowSimulation.from_data(settings)
sim.start_sim()
