import matplotlib.pyplot as plt
import numpy as np


def plot_data(data, regression_line, years, cood_yr):
  data = np.array(data)

  plt.figure(figsize=(10, 6))
  plt.plot(data[:, 0], data[:, 1], 'o', label='Datos')

  #Punto futuro
  plt.plot(cood_yr[0], cood_yr[1], 'o', label='Estimacion')

  plt.plot(years, regression_line, 'r', label='Regresion Lineal')
  plt.grid(True)
  plt.legend()
  plt.title('Historico de Datos y Regresion Lineal')
  plt.xlabel('Año')
  plt.ylabel('Estudiantes Matriculados')
  plt.savefig('./prediccion.png')
  plt.close()