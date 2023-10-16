from PyFlowFields import *

json_data = '{"bg": [150, 0, 0], "pcolor": [255, 255, 255], "force": 150, "fstep": [0.2, 0.2]}'

sim = FlowSimulation.from_data(json.loads(json_data))
sim.start_sim()
