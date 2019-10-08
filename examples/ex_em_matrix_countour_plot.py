
import numpy as np
import matplotlib.pyplot as plt

from cary_reader import CaryData

data = CaryData.from_csv('test_data/berio_matrix_300_450.csv')

# converts the data to a pandas dataframe, with the excitation wavelengths as 
# columns and the emission wavelengths as rows (index)
df = data.get_ex_em_matrix()

X, Y = np.meshgrid(df.index, df.columns)
Z = df.values.transpose()

levels = np.linspace(0, 150, 50) # creates 20 contours between 0 and 150 intensity
plt.contourf(X, Y, Z, levels, cmap=plt.cm.jet)
plt.colorbar()
plt.xlabel('Emission (nm)')
plt.ylabel('Excitation (nm)')