TEMPERATURE_SCALE_FACTOR = 100
TEMPERATURE_MAX_REAL = 110.0
TEMPERATURE_MAX_SCALED = int(TEMPERATURE_MAX_REAL * TEMPERATURE_SCALE_FACTOR)  # 11000
TEMPERATURE_BITS = 14
HUMIDITY_BITS = 7
WIND_BITS = 3

WIND_DIRECTIONS = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]


def mapWindDirectionToBits(direction):
    # convierte la dirección de viento a un valor entero de 0-7
    if direction not in WIND_DIRECTIONS:
        # si viene algo raro, lo mandamos a N
        direction = "N"

    index = WIND_DIRECTIONS.index(direction)
    return index


def mapBitsToWindDirection(bits_value):
    # convierte el entero 0-7 a la dirección de viento
    if bits_value < 0 or bits_value >= len(WIND_DIRECTIONS):
        # fallback simple si se corrompe algo
        return "N"

    return WIND_DIRECTIONS[bits_value]


def scaleTemperatureToBits(temperature_value):
    # convierte temperatura float con 2 decimales a entero escalado que cabe en 14 bits
    if temperature_value < 0.0:
        temperature_value = 0.0
    if temperature_value > TEMPERATURE_MAX_REAL:
        temperature_value = TEMPERATURE_MAX_REAL

    scaled = int(round(temperature_value * TEMPERATURE_SCALE_FACTOR))

    # asegurarse que cabe en 14 bits
    max_value = (1 << TEMPERATURE_BITS) - 1
    if scaled > max_value:
        scaled = max_value

    return scaled


def scaleBitsToTemperature(temp_bits_value):
    # convierte entero escalado de 14 bits a float con 2 decimales
    if temp_bits_value < 0:
        temp_bits_value = 0

    max_value = (1 << TEMPERATURE_BITS) - 1
    if temp_bits_value > max_value:
        temp_bits_value = max_value

    temperature = temp_bits_value / TEMPERATURE_SCALE_FACTOR
    return round(temperature, 2)


def encodeMeasurementToBytes(measurement):
    # measurement: {"temperatura": float, "humedad": int, "direccion_viento": str}
    temperature_value = measurement.get("temperatura", 0.0)
    humidity_value = measurement.get("humedad", 0)
    wind_direction = measurement.get("direccion_viento", "N")

    temp_bits = scaleTemperatureToBits(temperature_value)

    if humidity_value < 0:
        humidity_value = 0
    if humidity_value > 100:
        humidity_value = 100

    hum_bits = int(humidity_value)
    wind_bits = mapWindDirectionToBits(wind_direction)

    # empaquetar: [ temp(14) | hum(7) | wind(3) ]
    packed = (temp_bits << (HUMIDITY_BITS + WIND_BITS)) | (hum_bits << WIND_BITS) | wind_bits

    # convertir a 3 bytes big-endian
    payload_bytes = packed.to_bytes(3, byteorder="big")
    return payload_bytes


def decodeBytesToMeasurement(payload_bytes):
    # convierte 3 bytes a dict con temperatura, humedad y direccion_viento
    if len(payload_bytes) != 3:
        # si no viene de 3 bytes, no se puede decodificar bien
        raise ValueError("payload debe tener exactamente 3 bytes")

    packed = int.from_bytes(payload_bytes, byteorder="big")

    wind_mask = (1 << WIND_BITS) - 1
    hum_mask = (1 << HUMIDITY_BITS) - 1
    temp_mask = (1 << TEMPERATURE_BITS) - 1

    wind_bits = packed & wind_mask
    hum_bits = (packed >> WIND_BITS) & hum_mask
    temp_bits = (packed >> (WIND_BITS + HUMIDITY_BITS)) & temp_mask

    temperature_value = scaleBitsToTemperature(temp_bits)
    humidity_value = int(hum_bits)
    wind_direction = mapBitsToWindDirection(wind_bits)

    measurement = {
        "temperatura": temperature_value,
        "humedad": humidity_value,
        "direccion_viento": wind_direction,
    }

    return measurement
