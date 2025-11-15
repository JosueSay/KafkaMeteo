import sys

from kafka import KafkaConsumer
import matplotlib.pyplot as plt

from encoding import decodeBytesToMeasurement


def createEncodedConsumer(topic_name, bootstrap_servers, group_id):
    # crea y devuelve un kafka consumer para leer payload de 3 bytes
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[bootstrap_servers],
        group_id=group_id,
        auto_offset_reset="latest",
        enable_auto_commit=True,
    )
    return consumer


def parseEncodedPayload(raw_value):
    # decodifica los 3 bytes al dict de medición
    measurement = decodeBytesToMeasurement(raw_value)
    return measurement


def updateTimeSeries(all_temp, all_hume, all_wind, measurement):
    all_temp.append(measurement.get("temperatura"))
    all_hume.append(measurement.get("humedad"))
    all_wind.append(measurement.get("direccion_viento"))


def updatePlots(all_temp, all_hume, all_wind):
    # graficar temperatura y humedad a partir de los datos decodificados
    plt.clf()

    plt.subplot(2, 1, 1)
    plt.plot(all_temp)
    plt.ylabel("temperatura (°c)")

    plt.subplot(2, 1, 2)
    plt.plot(all_hume)
    plt.ylabel("humedad (%)")
    plt.xlabel("muestras")

    plt.tight_layout()
    plt.pause(0.01)


def consumeEncodedLoop(topic_name, bootstrap_servers, group_id):
    consumer = createEncodedConsumer(topic_name, bootstrap_servers, group_id)

    all_temp = []
    all_hume = []
    all_wind = []

    plt.ion()
    plt.figure()

    for message in consumer:
        measurement = parseEncodedPayload(message.value)
        updateTimeSeries(all_temp, all_hume, all_wind, measurement)

        print(f"[consumer-encoded] topic={topic_name} data={measurement} raw={message.value.hex()}")

        updatePlots(all_temp, all_hume, all_wind)


def main():
    if len(sys.argv) < 3:
        print("uso: python consumer_encoded.py <carnet> <group_id>")
        sys.exit(1)

    topic_name = sys.argv[1]
    group_id = sys.argv[2]
    bootstrap_servers = "iot.redesuvg.cloud:9092"

    consumeEncodedLoop(topic_name, bootstrap_servers, group_id)


if __name__ == "__main__":
    main()
