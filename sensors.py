import random

# rangos para sensores
TEMPERATURE_MIN = 0.0
TEMPERATURE_MAX = 110.0
HUMIDITY_MIN = 0
HUMIDITY_MAX = 100

WIND_DIRECTIONS = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]


def configureRandom(seed=None):
    # permitir reproducir resultados si se pasa seed
    if seed is None:
        random.seed()
    else:
        random.seed(seed)


def generateTemperature():
    mean_temp = 27.0
    std_temp = 8.0

    value = random.gauss(mean_temp, std_temp)
    # limitar al rango real del sensor
    value = max(TEMPERATURE_MIN, min(TEMPERATURE_MAX, value))

    return round(value, 2)


def generateHumidity():
    mean_hume = 50.0
    std_hume = 20.0

    value = random.gauss(mean_hume, std_hume)
    # limitar al rango 0-100 y dejarlo entero
    value = max(HUMIDITY_MIN, min(HUMIDITY_MAX, value))

    return int(round(value))


def generateWindDirection():
    return random.choice(WIND_DIRECTIONS)


def buildMeasurement():
    temperature = generateTemperature()
    humidity = generateHumidity()
    wind_direction = generateWindDirection()

    measurement = {
        "temperatura": temperature,
        "humedad": humidity,
        "direccion_viento": wind_direction,
    }

    return measurement
