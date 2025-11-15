import time
import random
import sys

from kafka import KafkaProducer
from sensors import configureRandom, buildMeasurement
from encoding import encodeMeasurementToBytes


def createEncodedProducer(bootstrap_servers):
    # crea y devuelve un kafka producer básico para enviar bytes codificados
    producer = KafkaProducer(
        bootstrap_servers=[bootstrap_servers]
    )
    return producer


def serializeEncodedPayload(payload_bytes):
    # ya viene en bytes, pero se deja la función por simetría con la versión json
    return payload_bytes


def getRandomInterval():
    # intervalo aleatorio entre 15 y 30 segundos
    return random.uniform(15.0, 30.0)


def sendEncodedLoop(topic_name, bootstrap_servers):
    configureRandom()
    producer = createEncodedProducer(bootstrap_servers)

    while True:
        measurement = buildMeasurement()
        payload_bytes = encodeMeasurementToBytes(measurement)
        payload = serializeEncodedPayload(payload_bytes)

        producer.send(topic_name, value=payload)
        producer.flush()

        print(f"[producer-encoded] topic={topic_name} data={measurement} bytes={payload.hex()}")

        wait_seconds = getRandomInterval()
        time.sleep(wait_seconds)


def main():
    # uso: python producer_encoded.py <carnet>
    if len(sys.argv) < 2:
        print("uso: python producer_encoded.py <carnet>")
        sys.exit(1)

    topic_name = sys.argv[1]
    bootstrap_servers = "iot.redesuvg.cloud:9092"

    sendEncodedLoop(topic_name, bootstrap_servers)


if __name__ == "__main__":
    main()
