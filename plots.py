import numpy as np
import matplotlib.pyplot as plt

def plot_data(data, regression_line, years):

  data = np.array(data)

  plt.figure(figsize=(10, 6))
  plt.plot(data[:, 0], data[:, 1], 'o', label='Data Points')
  plt.plot(years, regression_line, 'r', label='Linear Regression')
  plt.grid(True)
  plt.legend()
  plt.title('Historical Data and Linear Regression')
  plt.xlabel('Year')
  plt.ylabel('Students Enrolled')
  plt.show()
