from PyFlowFields.flows import *

# FlowField Settings
ff_settings = FlowFieldSettings(
	fsize=[30, 30],
	fvar=2,
	frange=360,
	fstep=[0.2, 0.2]
)
# Particle Settings
movement_settings = ParticleMovementSettings(
	pforce=8.5,
	pvar=0.8,
	pperiod=2,
	pmaxspeed=300,
	pforcespeed=True
)
drawing_settings = ParticleDrawingSettings(
	pmode=ParticleDrawingSettings.MODE_PARTICLE,
	pwidth=4,
	pcolor=lambda particle, sim_duration: hue(sim_duration * 3, 220, 5)
)
particle_settings = ParticleSettings(drawing_settings, movement_settings)


fs = FlowSimulation(
	SimulationSettings(
		name="FlowField Simulation",
		fullscreen=True,
		population=1000,
		clear=True,
		bg=[10, 10, 10]
	),
	ff_settings,
	particle_settings
)

fs.start_sim()
