import json
import sys

from kafka import KafkaConsumer
import matplotlib.pyplot as plt


def createConsumer(topic_name, bootstrap_servers, group_id):
    # crea y devuelve un kafka consumer suscrito al topic
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[bootstrap_servers],
        group_id=group_id,
        auto_offset_reset="latest",
        enable_auto_commit=True,
    )
    return consumer


def parseMeasurement(raw_value):
    # convierte bytes a dict usando json
    text = raw_value.decode("utf-8")
    measurement = json.loads(text)
    return measurement


def updateTimeSeries(all_temp, all_hume, all_wind, measurement):
    all_temp.append(measurement.get("temperatura"))
    all_hume.append(measurement.get("humedad"))
    all_wind.append(measurement.get("direccion_viento"))


def updatePlots(all_temp, all_hume):
    # graficar temperatura y humedad en una misma figura
    plt.clf()

    # temperatura
    plt.subplot(2, 1, 1)
    plt.plot(all_temp)
    plt.ylabel("temperatura (°c)")

    # humedad
    plt.subplot(2, 1, 2)
    plt.plot(all_hume)
    plt.ylabel("humedad (%)")
    plt.xlabel("muestras")

    plt.tight_layout()
    plt.pause(0.01)


def consumeLoop(topic_name, bootstrap_servers, group_id):
    consumer = createConsumer(topic_name, bootstrap_servers, group_id)

    all_temp = []
    all_hume = []
    all_wind = []

    plt.ion()
    plt.figure()

    for message in consumer:
        measurement = parseMeasurement(message.value)
        updateTimeSeries(all_temp, all_hume, all_wind, measurement)

        print(f"[consumer] topic={topic_name} data={measurement}")

        updatePlots(all_temp, all_hume)


def main():
    if len(sys.argv) < 3:
        print("uso: python consumer_json.py <carnet> <group_id>")
        sys.exit(1)

    topic_name = sys.argv[1]
    group_id = sys.argv[2]
    bootstrap_servers = "iot.redesuvg.cloud:9092"

    consumeLoop(topic_name, bootstrap_servers, group_id)


if __name__ == "__main__":
    main()
