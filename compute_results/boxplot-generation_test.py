import matplotlib.pyplot as plt
import numpy as np

data1 = np.random.rand(10)
data2 = np.random.rand(10)

fig, axs = plt.subplots(1, 2)

axs[0].boxplot(data1)
axs[0].set_title('Boxplot 1')

axs[1].boxplot(data2)
axs[1].set_title('Boxplot 2')

plt.tight_layout()

plt.show()
