import json

from PyFlowFields.flows import FlowSimulation
from PyFlowFields.flows.flow_settings import *


if __name__ == "__main__":
	parser = argparse.ArgumentParser("PyFlowFields", description="Create a flow simulation from a command interpreter")
	parser.add_argument("-cfg", help="Parse config from a .json file", metavar="filename")

	SimulationSettings.add_arguments(parser)
	FlowFieldSettings.add_arguments(parser)
	ParticleMovementSettings.add_arguments(parser)
	ParticleDrawingSettings.add_arguments(parser)

	# Parse cmd line args
	args: dict = parser.parse_args().__dict__

	# Parse json args
	json_args: dict = {}
	if args.get("cfg") is not None:
		try:
			with open(args.get("cfg"), 'r') as sim_json:
				json_args = json.loads(sim_json.read())
			args.pop("cfg")
		except FileNotFoundError as e:
			print("[Error] Target file `%s` could not be found" % e.filename)
			quit()
		except PermissionError as e:
			print("[Error] No permission to access file `%s`" % e.filename)
			quit()
		except json.decoder.JSONDecodeError as e:
			print("[Error] JSON config is not valid... Message : %s" % e)
			quit()
		except Exception as e:
			print("[Error] An unknown error occurred... Message : %s" % e)
			quit()

	sim = FlowSimulation.from_data(json_args, args)
	sim.start_sim()