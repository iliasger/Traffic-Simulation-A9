# import os,subprocess, sys
# sumo_path=os.getenv("SUMO_HOME")
# traci_path=os.path.join(sumo_path,'tools')
# sys.path.append(traci_path)
# import traci
# import Config
# from app.logging import info
# from sumolib import checkBinary
# from sumo import SUMOConnector, SUMODependency
# from streaming import KafkaForword
# from app.streaming import KafkaConnector
# from colorama import Fore
# from app.simulation.Simulation import Simulation

import os, sys

from app.streaming import KafkaConnector

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))

from app.logging import info
from app.simulation.Simulation import Simulation
from app.streaming import KafkaForword
from colorama import Fore
from app.sumo import SUMOConnector, SUMODependency
import app.Config
import traci, sys

info('#####################################', Fore.CYAN)
info('#      Starting CrowdNav v0.1       #', Fore.CYAN)
info('#####################################', Fore.CYAN)
info('# Configuration:', Fore.YELLOW)
info('# Kafka-Host   -> ' + app.Config.kafkaHost, Fore.YELLOW)
info('# Kafka-Topic1 -> ' + app.Config.kafkaTopicTrips, Fore.YELLOW)
# init sending updates to kafka and getting commands from there
if app.Config.kafkaUpdates:
    KafkaForword.connect()
    KafkaConnector.connect()

# Check if sumo is installed and available
SUMODependency.checkDeps()
info('# SUMO-Dependency check OK!', Fore.GREEN)

# Start sumo in the background
SUMOConnector.start()
info("\n# SUMO-Application started OK!", Fore.GREEN)
# Start the simulation
Simulation.start()
# Simulation ended, so we shutdown
info(Fore.RED + '# Shutdown' + Fore.RESET)
traci.close()
sys.stdout.flush()

# sumoConfig = "A9_conf.sumocfg"
#traci.start([sumoBinary, "-c", Config.sumoConfig,"--no-step-log", "true","--no-warnings","true"])
#PORT=1122
#sumoProcess = subprocess.Popen([sumoBinary, "-c", Config.sumoConfig, "--remote-port", str(PORT), "--random", "t"])
#traci.init(PORT)

# for run in range(0,3600):
#     traci.simulationStep()
#     traci.lane.setDisallowed('Shoulder01_0', ['passenger'])
# traci.close()
