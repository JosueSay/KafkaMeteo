import matplotlib.pyplot as plt
from sensors import generateTemperature, generateHumidity

temps = [generateTemperature() for _ in range(500)]
hums = [generateHumidity() for _ in range(500)]

plt.figure(figsize=(12, 5))

# temperatura
plt.subplot(1, 2, 1)
plt.hist(temps, bins=30)
plt.title("Distribución de Temperatura (Histograma)")
plt.xlabel("°C")
plt.ylabel("Frecuencia")

# humedad
plt.subplot(1, 2, 2)
plt.hist(hums, bins=30)
plt.title("Distribución de Humedad (Histograma)")
plt.xlabel("%")
plt.ylabel("Frecuencia")

plt.tight_layout()
plt.show()
