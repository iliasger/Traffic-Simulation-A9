import json
import traci

from colorama import Fore
from app.logging import info
from app import Config
from app.streaming import KafkaForword, KafkaConnector

class Simulation(object):

    # the current tick of the simulation
    tick = 0

    hard_shoulder_on = False

    @classmethod
    def applyFileConfig(cls):
        """ reads configs from a json and applies it at realtime to the simulation """
        try:
            config = json.load(open('./knobs.json'))
            if config['hard_shoulder'] == "0":
                cls.hard_shoulder_on = False
            else:
                cls.hard_shoulder_on = True
        except:
            pass

    @classmethod
    def applyKafkaConfig(cls):
        """ Gets a new configuration value from Kafka"""
        new_conf = KafkaConnector.checkForNewConfiguration()
        if new_conf is not None:
            if "hard_shoulder" in new_conf:
                if new_conf['hard_shoulder'] == "0":
                    cls.hard_shoulder_on = False
                else:
                    cls.hard_shoulder_on = True

    @classmethod
    def start(cls):

        # start listening to all cars that arrived at their target
        # traci.simulation.subscribe((tc.VAR_ARRIVED_VEHICLES_IDS,))
        while 1:
            # Do one simulation step
            cls.tick += 1
            traci.simulationStep()


            if cls.hard_shoulder_on:
                if 'passenger' not in traci.lane.getAllowed('Shoulder01_0'):
                    print("Opening hard shoulder")
                    traci.lane.setAllowed('Shoulder01_0', ['passenger'])
            else:
                if 'passenger' in traci.lane.getAllowed('Shoulder01_0'):
                    print("Closing hard shoulder")
                    traci.lane.setDisallowed('Shoulder01_0', ['passenger'])

            print(cls.tick)
            msg = dict()
            msg["tick"] = 1
            KafkaForword.publish(msg, Config.kafkaTopicTrips)

            if (cls.tick % 10) == 0:
                if Config.kafkaUpdates is False:
                    cls.applyFileConfig()
                else:
                    cls.applyKafkaConfig()

