from sensor import Sensor
from pubsub import PubSub
from datetime import datetime
import logging


if __name__ == "__main__":
    sensor = Sensor()
    pubsub = PubSub()
    isPass = False
    while True:
        try:
            data, addr = sensor.get_data()
            if data:
                x, y, z = map(float, data)
                if z > 5 and not isPass:
                    isPass = True
                    payload = {
                        "timestamp": datetime.now().strftime("%d_%m_%Y-%H_%M_%S"),
                        "sensor_id": f"{addr[0]}:{addr[1]}",
                        "x": x,
                        "y": y,
                        "z": z
                    }
                    pubsub.publish(payload)
                else:
                    isPass = False

        except ValueError as error:
            logging.error(error)
