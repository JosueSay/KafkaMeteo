import json
import time
import random
import sys

from kafka import KafkaProducer
from sensors import configureRandom, buildMeasurement


def createProducer(bootstrap_servers):
    # crea y devuelve un kafka producer básico para enviar bytes
    producer = KafkaProducer(
        bootstrap_servers=[bootstrap_servers]
    )
    return producer


def serializeMeasurement(measurement):
    # convierte el dict de medición a bytes usando json
    json_text = json.dumps(measurement)
    return json_text.encode("utf-8")


def getRandomInterval():
    # intervalo aleatorio entre 15 y 30 segundos
    return random.uniform(15.0, 30.0)


def sendLoop(topic_name, bootstrap_servers):
    configureRandom()
    producer = createProducer(bootstrap_servers)

    while True:
        measurement = buildMeasurement()
        payload = serializeMeasurement(measurement)

        producer.send(topic_name, value=payload)
        producer.flush()

        print(f"[producer] topic={topic_name} data={measurement}")

        wait_seconds = getRandomInterval()
        time.sleep(wait_seconds)


def main():
    # uso: python producer_json.py <carnet>
    if len(sys.argv) < 2:
        print("uso: python producer_json.py <carnet>")
        sys.exit(1)

    topic_name = sys.argv[1]
    bootstrap_servers = "iot.redesuvg.cloud:9092"

    sendLoop(topic_name, bootstrap_servers)


if __name__ == "__main__":
    main()
